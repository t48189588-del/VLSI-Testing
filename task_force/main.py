#!/usr/bin/env -S uv run
import argparse
import subprocess
from pathlib import Path
import time

import numpy as np

from kyupy import verilog, bench, log, logic, batchrange
from kyupy.techlib import techlib_by_name, KYUPY
from kyupy.logic_sim import LogicSim2V

from fsim.static import LineRoles, FaultSet

def main():

    parser = argparse.ArgumentParser(description='A basic stuck-at fault simulator.')
    parser.add_argument('-t', '--tlib', default='SKY130', help=f'Techlib for verilog circuit. Default: SKY130, available: {sorted(techlib_by_name.keys())}.')
    parser.add_argument('-p', '--patterns', default=1024, help='Number of random patterns to simulate. Default: 1024.')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility. Default: 42.')
    parser.add_argument('circuit', help='Gate-level verilog, bench, or nix package to import. See available packages: "nix flake show github:s-holst/benchmark-circuits".')
    args = parser.parse_args()
    args.patterns = int(args.patterns)
    args.tlib = techlib_by_name[args.tlib]

    if not (circuit_path := Path(args.circuit)).exists(): # fallback to published nix package.
        nix_cmd = f"nix build github:s-holst/benchmark-circuits#{args.circuit} --print-out-paths --no-link"
        benchmark_path = Path(subprocess.check_output(nix_cmd.split(), text=True).strip())
        circuit_path = next(benchmark_path.glob("*/nl/*.nl.v"))

    log.info(f'loading {circuit_path} ...')
    if circuit_path.name.endswith('.bench'):
        c = bench.load(circuit_path)
        args.tlib = techlib_by_name['KYUPY']
    else:
        c = verilog.load(circuit_path, tlib=args.tlib)
    stats = {k.replace('__',''): v for k, v in c.stats(args.tlib).items() if k.startswith('__') or k.endswith('put')}
    log.info(f'circuit {stats=}')

    lr = LineRoles(c, args.tlib)
    log.info(f'line role stats={lr.stats}')

    fs = FaultSet(c, args.tlib)
    log.info(f'fault sites: {len(fs.fault_sites)}')
    log.info(f'collapsed stuck-at fault count: {len(fs.saf_equiv_classes)}')

    c.resolve_tlib_cells(args.tlib)

    ffr_stems = []
    for stem, _ in c.fanout_free_regions(KYUPY):
        if len(stem.outs) > 0 and stem.outs[0] is not None:
            ffr_stems.append(stem.outs[0])
    ffr_stems = np.array(ffr_stems, dtype=np.uint32)

    log.info(f'FFR count: {len(ffr_stems)}')

    sim = LogicSim2V(c, sims=min(args.patterns, 10240))

    rng = np.random.default_rng(args.seed)
    patterns = rng.choice(
                [logic.ZERO, logic.ONE],
                size=(sim.s_len, args.patterns),
            ).astype(np.uint8)

    golden = np.zeros_like(patterns)
    log.info(f'{sim=}')

    sim.simulate(patterns, golden)
    log.info(f'golden sim finished.')

    syndrome = np.zeros_like(patterns)

    injection_faults = np.array(list(fs.saf_equiv_classes.keys()), dtype=np.uint32)
    rng.shuffle(injection_faults)

    undetected = set()
    detected = set()

    start_time = time.perf_counter()

    with log.progress() as p:
        for fidx, fault in enumerate(injection_faults):
            fault_site = fault//2
            fault_polarity = fault&1
            p.update((fidx+1) / len(injection_faults), f'd:{len(detected)} u:{len(undetected)}')
            for bo, bs in batchrange(patterns.shape[1], sim.sims):
                sim.s_assign[:, :bs] = patterns[:, bo:bo+bs]
                sim.s_to_c()
                sim.c_prop(fault_line=fault_site, fault_model=fault_polarity)
                sim.c_to_s()
                syndrome[:, bo:bo+bs] = sim.s_result[:,:bs]
            if np.allclose(golden, syndrome):
                undetected.add(fault)
            else:
                detected.add(fault)

    sim_time = time.perf_counter() - start_time
    log.info(f'fsim time: {sim_time:.2f}s')
    sim_performance = stats['comb'] * len(injection_faults) * patterns.shape[1] / sim_time
    log.info(f'fsim performance: {sim_performance:.2e} gfp/s')
    log.info(f'detected by simulation: {len(detected)}/{len(injection_faults)}  -  {len(detected)/len(injection_faults)*100:.2f}%')

if __name__ == "__main__":
    main()