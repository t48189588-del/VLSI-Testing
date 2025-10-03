#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stuck-at Fault Simulator (supports c.ndim=3)
- Reads PO directly from c (no longer depends on c_to_s)
- Automatically detects c axis order; automatically or heuristically finds the c-line indices for POs
"""

import argparse
import re
import numpy as np
from kyupy import bench, log, logic
from kyupy.logic_sim import LogicSim


# ---------- Read I/O names from .bench (for printing) ----------
def parse_bench_io_names(bench_path: str):
    text = open(bench_path, 'r', encoding='utf-8', errors='ignore').read()
    def grab(pattern):
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if not m: return []
        items = re.split(r'[,\s]+', m.group(1).strip())
        return [s for s in items if s]
    return grab(r'\.inputs\s*\(([^)]*)\)'), grab(r'\.outputs\s*\(([^)]*)\)')


# ---------- mv ↔ char ----------
def mv_val_to_char(v):
    vv = int(v) & 0b11  # 00->0, 11->1, 01/10->X
    return '0' if vv == 0 else ('1' if vv == 3 else 'X')

def mv_row_to_str(mv_row_1d):
    return ''.join(mv_val_to_char(x) for x in mv_row_1d)


# ---------- Infer "which c-lines correspond to POs" ----------
def guess_po_c_indices(lsim, circuit, num_po):
    # 1) Try to use attributes from lsim (if available)
    for attr in ('po_c_locs', 'po_locs', 'po_lines', 'po_idxs'):
        if hasattr(lsim, attr):
            idx = getattr(lsim, attr)
            try:
                arr = np.asarray(idx, dtype=int)
                if arr.size == num_po:
                    log.info(f'[dbg] PO indices from lsim.{attr} = {arr.tolist()}')
                    return arr
            except Exception:
                pass

    # 2) Try to infer from circuit object
    #    Common: circuit.pos may be a list of output nodes; node objects may have .line or .fanin etc.
    try:
        pos = getattr(circuit, 'pos', None)
        if pos:
            cand = []
            for n in pos:
                # Try to find associated line index
                for k in ('line', 'l', 'source', 'fanin', 'in_'):
                    if hasattr(n, k):
                        v = getattr(n, k)
                        # fanin might be a list
                        if isinstance(v, (list, tuple)) and v:
                            v = v[0]
                        if hasattr(v, 'index'):
                            cand.append(int(getattr(v, 'index')))
                            break
            if len(cand) == num_po:
                arr = np.array(cand, dtype=int)
                log.info(f'[dbg] PO indices from circuit.pos = {arr.tolist()}')
                return arr
    except Exception:
        pass

    # 3) Fallback: take the last num_po lines
    total_lines = len(getattr(circuit, 'lines', []))
    if total_lines >= num_po:
        arr = np.arange(total_lines - num_po, total_lines, dtype=int)
        log.info(f'[warn] fallback PO indices (last {num_po} lines): {arr.tolist()}')
        return arr

    raise RuntimeError('Could not infer PO indices in c, and circuit.lines is too short for fallback.')


# ---------- Extract PO’s two data planes from c (num_po, 2, W) ----------
def extract_po_bp2_from_c(lsim, po_c_indices):
    c = lsim.c
    

    if c.ndim == 3:
        # Your environment: (lines?, planes?, words)
        lines, p, w = c.shape
        # Detect plane axis: look for axis with size=2; if none (yours is 1), treat as "only 1 data plane"
        plane_axis = 1 if p in (1, 2) else 0
        words_axis = 2
        # Select PO lines
        take_nodes = np.take(c, indices=po_c_indices, axis=0)  # -> (num_po, plane?, words)
        # Select first two planes (if only 1, duplicate to avoid bp_to_mv errors)
        if plane_axis == 1:
            if take_nodes.shape[1] >= 2:
                arr = take_nodes[:, :2, :]
            else:
                one = take_nodes[:, 0:1, :]
                arr = np.concatenate([one, one], axis=1)
        else:
            arr = np.moveaxis(take_nodes, plane_axis, 1)
            if arr.shape[1] >= 2:
                arr = arr[:, :2, :]
            else:
                one = arr[:, 0:1, :]
                arr = np.concatenate([one, one], axis=1)
        return arr

    else:
        raise RuntimeError(f'Unsupported lsim.c shape: {c.shape}')


def main():
    ap = argparse.ArgumentParser(description='Stuck-at fault simulator (reads PO from c, supports c.ndim=3).')
    ap.add_argument('bench', help='BENCH netlist file (e.g., c17.bench)')
    ap.add_argument('tests', help='Test vectors: one line per PI, each a bitstring of length=#vectors')
    args = ap.parse_args()

    # Load circuit and test data
    circuit = bench.load(args.bench)
    log.info(f'Circuit {circuit}')
    with open(args.tests, 'r', encoding='utf-8', errors='ignore') as f:
        tests = logic.mvarray(*f.read().splitlines())
    log.info(f'TestDataShape {tests.shape}')

    # I/O names (for printing)
    pi_names, po_names = parse_bench_io_names(args.bench)

    sims = tests.shape[1]
    lsim = LogicSim(circuit, sims=sims, m=2)
    num_pi = len(lsim.pi_s_locs)
    num_po = len(lsim.po_s_locs)

    if len(pi_names) < num_pi:
        pi_names += [f'PI{i}' for i in range(len(pi_names), num_pi)]
    if len(po_names) < num_po:
        po_names += [f'PO{i}' for i in range(len(po_names), num_po)]
    pi_names = pi_names[:num_pi]
    po_names = po_names[:num_po]
    log.info(f'#PI={num_pi} #PO={num_po} sims={sims} m=2')

    # PI rows → bp
    input_mv = tests[:num_pi]
    input_bp = logic.mv_to_bp(input_mv)  # (num_pi, 2, W)

    # Try to get PO indices in c
    po_c_indices = guess_po_c_indices(lsim, circuit, num_po)

    # ===== Golden =====
    log.info('--- Running Golden (Fault-Free) Simulation ---')
    try:
        lsim.s[...] = 0
        # Your environment: c is 3D, no slot; just zero it out
        lsim.c[...] = 0
    except Exception:
        pass

    # Inject PI into first two planes of s (slot 0)
    lsim.s[0, lsim.pi_s_locs, :2] = input_bp[:, :2]
    lsim.s_to_c()
    lsim.c_prop()

    log.info(f'[dbg] lsim.s.shape={getattr(lsim.s,"shape",None)} lsim.c.shape={getattr(lsim.c,"shape",None)}')

    # Extract PO planes from c
    golden_c_bp2 = extract_po_bp2_from_c(lsim, po_c_indices)  # (num_po, 2, W)
    log.info(f'[dbg] golden_c_bp2.shape={golden_c_bp2.shape}')

    # Convert to mv and print I/O table
    golden_mv_rows = [logic.bp_to_mv(golden_c_bp2[i]) for i in range(num_po)]
    golden_mv = np.vstack(golden_mv_rows)  # (num_po, sims)
    golden_bin = np.array([logic.mv_final(golden_mv[i]) for i in range(num_po)], dtype=np.uint8)
    ones_count = golden_bin.sum(axis=1).tolist()
    log.info(f'[dbg] PO ones_count (first {min(10,num_po)}): {ones_count[:min(10,num_po)]}')

    log.info('--- Fault-Free I/O per Test Vector ---')
    header = ['vec'] + pi_names + ['->'] + po_names
    log.info('  ' + ' | '.join(header))
    pi_mv_strings = [mv_row_to_str(input_mv[i]) for i in range(num_pi)]
    po_mv_strings = [mv_row_to_str(golden_mv[i]) for i in range(num_po)]
    for t in range(sims):
        row = [f'{t:04d}'] + [s[t] for s in pi_mv_strings] + ['->'] + [s[t] for s in po_mv_strings]
        log.info('  ' + ' | '.join(row))
    log.info('--- End of I/O dump ---')

    # ===== Fault Simulation (compare directly in c) =====
    all_faults = [(line.index, sa) for line in circuit.lines for sa in (0, 1)]
    total_faults = len(all_faults)
    detected_faults = set()

    log.info(f'\n--- Full Fault List ({total_faults} faults) ---')
    for i, (loc, sa) in enumerate(all_faults):
        log.info(f'  {i}: Line {loc} stuck-at {sa}')
    log.info('--- End of Fault List ---\n')

    log.info('--- Running Full Fault Simulation with Individual Fault Checks ---')
    for fault_location, stuck_at_value in all_faults:
        try:
            lsim.s[1, :, :] = 0
            lsim.c[...] = 0
        except Exception:
            pass

        lsim.s[1, lsim.pi_s_locs, :2] = input_bp[:, :2]
        lsim.s_to_c()
        lsim.c_prop(fault_line=fault_location, fault_model=stuck_at_value)

        golden_bp2 = extract_po_bp2_from_c(lsim, po_c_indices)
        faulty_bp2 = extract_po_bp2_from_c(lsim, po_c_indices)

        # Note: When c has no slot dimension, c_prop overwrites the same c buffer,
        # so we must run golden and faulty separately to compare.
        # Here we explicitly run golden first (no fault), then faulty.
        lsim.c[...] = 0
        lsim.s[1, lsim.pi_s_locs, :2] = input_bp[:, :2]
        lsim.s_to_c()
        lsim.c_prop()  # no fault
        golden_bp2 = extract_po_bp2_from_c(lsim, po_c_indices)

        lsim.c[...] = 0
        lsim.s[1, lsim.pi_s_locs, :2] = input_bp[:, :2]
        lsim.s_to_c()
        lsim.c_prop(fault_line=fault_location, fault_model=stuck_at_value)
        faulty_bp2 = extract_po_bp2_from_c(lsim, po_c_indices)

        if np.any(golden_bp2 != faulty_bp2):
            detected_faults.add((fault_location, stuck_at_value))
            log.info(f'  [DETECTED] Fault on Line {fault_location} stuck-at {stuck_at_value}')
        else:
            log.info(f'  [NOT DETECTED] Fault on Line {fault_location} stuck-at {stuck_at_value}')

    detected_count = len(detected_faults)
    coverage = (detected_count / total_faults) * 100.0 if total_faults else 0.0
    log.info(f'\nTotal Faults: {total_faults}')
    log.info(f'Detected Faults: {detected_count}')
    log.info(f'Fault Coverage: {coverage:.2f}%')
    log.info(f'Detected faults: {sorted(detected_faults)}')


if __name__ == '__main__':
    main()