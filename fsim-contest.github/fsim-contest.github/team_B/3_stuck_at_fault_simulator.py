#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import time
from collections import defaultdict, deque

# -------------------------------
# BENCH 解析
# -------------------------------

def net_name(s):
    s = s.strip()
    try:
        return int(s)
    except ValueError:
        return s

def parse_bench(path):
    pis, pos = [], []
    raw_gates = []
    gid = 0

    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue

            m = re.match(r'INPUT\(([^)]+)\)', line, re.IGNORECASE)
            if m:
                pis.append(net_name(m.group(1).strip()))
                continue

            m = re.match(r'OUTPUT\(([^)]+)\)', line, re.IGNORECASE)
            if m:
                pos.append(net_name(m.group(1).strip()))
                continue

            m = re.match(r'([^=]+)=\s*([A-Za-z]+)\(([^)]*)\)', line)
            if m:
                out = net_name(m.group(1))
                gtype = m.group(2).upper()
                args = m.group(3).strip()
                ins = [] if args == '' else [net_name(a.strip()) for a in args.split(',')]
                raw_gates.append({"id": gid, "type": gtype, "ins": ins, "out": out})
                gid += 1

    producer = {g["out"]: g["id"] for g in raw_gates}

    indeg = {g["id"]: 0 for g in raw_gates}
    fanouts_gates = defaultdict(list)
    for g in raw_gates:
        for n in g["ins"]:
            if n in producer:
                p = producer[n]
                indeg[g["id"]] += 1
                fanouts_gates[p].append(g["id"])

    q = deque([gid for gid, d in indeg.items() if d == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in fanouts_gates[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(topo) != len(raw_gates):
        raise ValueError("Netlist is not a DAG or parsing failed (topological sort incomplete).")

    gid2gate = {}
    gid_to_topo_idx = {}
    gates = []
    for i, gid in enumerate(topo):
        g = next(x for x in raw_gates if x["id"] == gid)
        gates.append(g)
        gid2gate[gid] = g
        gid_to_topo_idx[gid] = i

    lines = []
    for g in gates:
        lines.append(("stem", g["out"], g["id"], None))
        for pidx, src in enumerate(g["ins"]):
            lines.append(("branch", src, g["id"], pidx))

    net_to_fanout_pins = defaultdict(list)
    for g in gates:
        for pidx, n in enumerate(g["ins"]):
            net_to_fanout_pins[n].append((g["id"], pidx))

    # 預先排序 fanout gate ID
    net_to_sorted_fan_gids = {
        net: sorted({gid for gid, _ in pins}, key=lambda g: gid_to_topo_idx[g])
        for net, pins in net_to_fanout_pins.items()
    }

    return {
        "pis": pis,
        "pos": pos,
        "gates": gates,
        "lines": lines,
        "producer": {g["out"]: g["id"] for g in gates},
        "gid2gate": gid2gate,
        "net_to_fanout_pins": net_to_fanout_pins,
        "net_to_sorted_fan_gids": net_to_sorted_fan_gids,
        "gid_to_topo_idx": gid_to_topo_idx,
        "fanouts_gates": fanouts_gates,
    }

# -------------------------------
# Gate eval
# -------------------------------

def eval_gate(gtype, in_vals):
    if gtype in ("BUF", "BUFF"):
        return in_vals[0]
    if gtype == "NOT":
        return 1 - in_vals[0]
    if gtype == "AND":
        v = 1
        for a in in_vals: v &= a
        return v
    if gtype == "NAND":
        return 1 - eval_gate("AND", in_vals)
    if gtype == "OR":
        v = 0
        for a in in_vals: v |= a
        return v
    if gtype == "NOR":
        return 1 - eval_gate("OR", in_vals)
    if gtype == "XOR":
        v = 0
        for a in in_vals: v ^= a
        return v
    if gtype == "XNOR":
        return 1 - eval_gate("XOR", in_vals)
    raise ValueError(f"Unsupported gate: {gtype}")

# -------------------------------
# 測試讀取
# -------------------------------

def read_tests(path, num_pis):
    vecs = []
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            bits = re.findall(r'[01]', raw)
            if len(bits) >= num_pis:
                vecs.append([int(b) for b in bits[:num_pis]])
    return vecs

# -------------------------------
# 模擬
# -------------------------------

def simulate_good(nl, vec_bits):
    net_val = {}
    for i, n in enumerate(nl["pis"]):
        net_val[n] = vec_bits[i]
    for g in nl["gates"]:
        ins = [net_val[n] for n in g["ins"]]
        net_val[g["out"]] = eval_gate(g["type"], ins)
    return net_val

# -------------------------------
# 差分模擬 (branch/stem)
# -------------------------------

def difference_sim_branch(nl, good_net, line, sa, pos_list, golden_pos_t):
    _, src_net, tgt_gid, pin_idx = line
    tgt_gate = nl["gid2gate"][tgt_gid]

    ins = [sa if pidx == pin_idx else good_net[n] for pidx, n in enumerate(tgt_gate["ins"])]
    new_out = eval_gate(tgt_gate["type"], ins)
    if new_out == good_net[tgt_gate["out"]]:
        return None

    work = {tgt_gate["out"]: new_out}
    if tgt_gate["out"] in pos_list:
        bad_t = tuple(work.get(po, good_net[po]) for po in pos_list)
        if bad_t != golden_pos_t:
            return True

    q = [(nl["gid_to_topo_idx"][tgt_gid], tgt_gid)]
    visited = set()
    while q:
        _, gid = q.pop(0)
        for fan_gid in nl["fanouts_gates"].get(gid, []):
            if fan_gid in visited:
                continue
            visited.add(fan_gid)
            gg = nl["gid2gate"][fan_gid]
            ins2 = [work.get(n, good_net[n]) for n in gg["ins"]]
            new_out2 = eval_gate(gg["type"], ins2)
            if new_out2 != good_net[gg["out"]]:
                work[gg["out"]] = new_out2
                if gg["out"] in pos_list:
                    bad_t = tuple(work.get(po, good_net[po]) for po in pos_list)
                    if bad_t != golden_pos_t:
                        return True
                q.append((nl["gid_to_topo_idx"][fan_gid], fan_gid))
    return None

def difference_sim_stem(nl, good_net, line, sa, pos_list, golden_pos_t):
    _, net, src_gid, _ = line
    if good_net.get(net, 0) == sa:
        return None

    work = {net: sa}
    if net in pos_list:
        bad_t = tuple(work.get(po, good_net[po]) for po in pos_list)
        if bad_t != golden_pos_t:
            return True

    q = deque(nl["net_to_sorted_fan_gids"].get(net, []))
    visited = set()
    while q:
        gid = q.popleft()
        if gid in visited:
            continue
        visited.add(gid)
        gg = nl["gid2gate"][gid]
        ins2 = [work.get(n, good_net[n]) for n in gg["ins"]]
        new_out2 = eval_gate(gg["type"], ins2)
        if new_out2 != good_net[gg["out"]]:
            work[gg["out"]] = new_out2
            if gg["out"] in pos_list:
                bad_t = tuple(work.get(po, good_net[po]) for po in pos_list)
                if bad_t != golden_pos_t:
                    return True
            for nxt in nl["fanouts_gates"].get(gid, []):
                q.append(nxt)
    return None

# -------------------------------
# 主程式
# -------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bench")
    ap.add_argument("tests")
    ap.add_argument("--no-early-stop", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    nl = parse_bench(args.bench)
    vecs = read_tests(args.tests, len(nl["pis"]))
    if not vecs:
        raise ValueError("tests 讀不到任何有效向量。")

    golden_nets = [simulate_good(nl, v) for v in vecs]
    pos_list = nl["pos"]
    golden_pos = [tuple(gn[po] for po in pos_list) for gn in golden_nets]

    faults = [(idx, line, sa) for idx, line in enumerate(nl["lines"]) for sa in (0, 1)]
    detected_at = {}

    for t_idx, v in enumerate(vecs):
        to_check = faults if args.no_early_stop else [(lidx, line, sa)
                         for (lidx, line, sa) in faults if (lidx, sa) not in detected_at]
        if not to_check:
            break
        good_net = golden_nets[t_idx]
        gpos_t = golden_pos[t_idx]
        for (lidx, line, sa) in to_check:
            if line[0] == "branch":
                _, src_net, tgt_gid, pin_idx = line
                seen = good_net[nl["gid2gate"][tgt_gid]["ins"][pin_idx]]
                if seen == sa:
                    continue
                res = difference_sim_branch(nl, good_net, line, sa, pos_list, gpos_t)
            else:
                _, net, _, _ = line
                if good_net.get(net, 0) == sa:
                    continue
                res = difference_sim_stem(nl, good_net, line, sa, pos_list, gpos_t)

            if res and (lidx, sa) not in detected_at:
                detected_at[(lidx, sa)] = t_idx

    total_lines = len(nl["lines"])
    total_faults = total_lines * 2
    detected_cnt = len(detected_at)

    print(f"# File: bench={args.bench} tests={args.tests}")
    print(f"# Lines: {total_lines}")
    print(f"# Faults: {total_faults}")
    print(f"# Detected: {detected_cnt} / {total_faults} ({detected_cnt*100.0/total_faults:.2f}%)")
    print(f"# Time: {time.time() - t0:.3f} s")
    print("=" * 90)

if __name__ == "__main__":
    main()
