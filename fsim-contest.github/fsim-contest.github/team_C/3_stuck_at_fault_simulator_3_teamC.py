import argparse
import time
from pathlib import Path
from collections import Counter

t0 = time.perf_counter()
def log(msg: str):
    dt = time.perf_counter() - t0

    print(f"# {dt:09.3f} - {msg}")

def parse_bench(path: Path):
    inputs, outputs, gates = [], [], []
    def clean(s): return s.split('#',1)[0].strip()
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = clean(raw)
        if not line: continue
        if line.startswith('INPUT(') and line.endswith(')'):
            inputs.append(line[6:-1].strip())
        elif line.startswith('OUTPUT(') and line.endswith(')'):
            outputs.append(line[7:-1].strip())
        elif '=' in line:
            left, right = [t.strip() for t in line.split('=',1)]
            gate, args = right.split('(',1)
            ins = [t.strip() for t in args[:-1].split(',')] if args[:-1] else []
            gates.append((left, gate.upper(), ins))
    return inputs, outputs, gates

def topo_order(inputs, gates):
    known, order, seen = set(inputs), [], set()
    while len(seen) < len(gates):
        progressed = False
        for out, gt, ins in gates:
            if out in seen: continue
            if all(u in known for u in ins):
                order.append((out, gt, ins))
                seen.add(out); known.add(out); progressed = True
        if not progressed:
            rem = [o for o,_,_ in gates if o not in seen]
            raise RuntimeError(f"有環或未定義 net：{rem}")
    return order

def eval_gate(gt, xs):
    if gt in ('BUF', 'BUFF'):  return xs[0]
    if gt=='NOT':  return 0 if xs[0] else 1
    if gt=='AND':  v=1;  [v:=v&x for x in xs]; return v
    if gt=='NAND': v=1;  [v:=v&x for x in xs]; return 0 if v else 1
    if gt=='OR':   v=0;  [v:=v|x for x in xs]; return v
    if gt=='NOR':  v=0;  [v:=v|x for x in xs]; return 0 if v else 1
    if gt=='XOR':  v=0;  [v:=v^x for x in xs]; return v
    if gt=='XNOR': v=0;  [v:=v^x for x in xs]; return 0 if v else 1
    raise RuntimeError(f"不支援的 gate：{gt}")

def simulate_baseline(inputs, outputs, order, tests):
    base = []
    for vec in tests:
        if len(vec) != len(inputs):
            raise ValueError(f"Vector len={len(vec)} != #inputs={len(inputs)}")
        nets = {name:(1 if vec[i]=='1' else 0) for i,name in enumerate(inputs)}
        for out, gt, ins in order:
            nets[out] = eval_gate(gt, [nets[u] for u in ins])
        base.append([nets.get(o,0) for o in outputs])
    return base

def detect_fault(inputs, outputs, order, tests, base, net, sa):
    for i, vec in enumerate(tests):
        nets = {name:(1 if vec[j]=='1' else 0) for j,name in enumerate(inputs)}
        if net in nets: nets[net] = sa
        for out, gt, ins in order:
            v = eval_gate(gt, [nets[u] for u in ins])
            if out == net: v = sa
            nets[out] = v
        if [nets.get(o,0) for o in outputs] != base[i]:
            return True
    return False

def circuit_stats(name, inputs, outputs, gates):
    # cells
    cells = len(gates)
    # 所有 nets（包含 gate 輸入與輸出、I/O）
    out_nets = [o for o,_,_ in gates]
    in_nets = [n for _,_,ins in gates for n in ins]
    all_nets = set(inputs) | set(outputs) | set(out_nets) | set(in_nets)
    lines = len(all_nets)
    # forks: 被作為輸入使用超過一次的 net 數
    fanin_count = Counter(in_nets)
    forks = sum(1 for _,cnt in fanin_count.items() if cnt > 1)
    io_nodes = len(inputs) + len(outputs)
    return {
        "name": name,
        "cells": cells,
        "forks": forks,
        "lines": lines,
        "io_nodes": io_nodes
    }

def main():
    ap = argparse.ArgumentParser(description="Stuck-at fault simulator (純 Python)")
    ap.add_argument("bench"), ap.add_argument("tests")
    args = ap.parse_args()
    bench_p, tests_p = Path(args.bench), Path(args.tests)

    log("Loading bench & tests...")
    inputs, outputs, gates = parse_bench(bench_p)
    tests = [l.strip() for l in tests_p.read_text(encoding='utf-8').splitlines() if l.strip()]

    stats = circuit_stats(bench_p.name, inputs, outputs, gates)
    log(f'Circuit {{name: "{stats["name"]}", cells: {stats["cells"]}, forks: {stats["forks"]}, '
        f'lines: {stats["lines"]}, io_nodes: {stats["io_nodes"]}}}')
    log(f'TestDataShape ({len(tests)}, {len(inputs)})')

    order  = topo_order(inputs, gates)

    # 可能 fault 的 net ＝ 所有 nets（I/O + gate out + gate in）
    out_nets = [o for o,_,_ in gates]
    in_nets = [n for _,_,ins in gates for n in ins]
    all_nets = sorted(set(inputs) | set(outputs) | set(out_nets) | set(in_nets))
    total_possible_faults = 2 * len(all_nets)
    log(f"Total possible faults: {total_possible_faults}")

    log("Performing fault simulation...")
    base   = simulate_baseline(inputs, outputs, order, tests)

    detected = []
    # I/O + gate outputs 作為 fault 加入點
    nets_for_faults = sorted(set(inputs) | set(outputs) | set(out_nets))
    faults = [(n,0) for n in nets_for_faults] + [(n,1) for n in nets_for_faults]

    for n,sa in faults:
        if detect_fault(inputs, outputs, order, tests, base, n, sa):
            detected.append((n,sa))

    total = len(faults)
    log(f"TotalFaults {total}")
    log(f"DetectedFaults {len(detected)}")
    log(f"FaultCoverage {len(detected)/total*100:.2f}%")

    out = bench_p.with_suffix('.detected.txt')
    with open(out, 'w', encoding='utf-8') as f:
        for n, sa in detected:
            f.write(f"{n}/SA{sa}\n")
    log(f"Detected list -> {out}")

if __name__ == "__main__":
    main()
