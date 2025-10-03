#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from pathlib import Path
import random

def parse_bench_inputs(path: Path):
    """只讀 .bench 裡的 INPUT(...) 並回傳輸入腳位名稱列表（照出現順序）"""
    inputs = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split('#', 1)[0].strip()
            if line.startswith('INPUT(') and line.endswith(')'):
                inputs.append(line[6:-1].strip())
    if not inputs:
        raise ValueError("在 .bench 檔內找不到任何 INPUT()")
    return inputs

def main():
    ap = argparse.ArgumentParser(description="產生隨機 .tests（純 0/1，每行=輸入位元）")
    ap.add_argument('-i', '--inputfile', required=True, help='.bench 檔案路徑')
    ap.add_argument('-o', '--outputfile', help='輸出 .tests 檔案路徑（預設為同名 .tests）')
    ap.add_argument('-n', '--ntests', type=int, default=100, help='測試向量數量')
    ap.add_argument('-s', '--seed', type=int, default=42, help='隨機種子')
    args = ap.parse_args()

    bench_path = Path(args.inputfile)
    out_path = Path(args.outputfile) if args.outputfile else bench_path.with_suffix('.tests')

    inputs = parse_bench_inputs(bench_path)
    n_inputs = len(inputs)
    print(f"Inputs: {n_inputs}  -> {inputs}")

    random.seed(args.seed)
    with open(out_path, 'w', encoding='utf-8') as f:
        for _ in range(args.ntests):
            bits = ''.join('1' if random.randint(0,1) else '0' for _ in range(n_inputs))
            f.write(bits + '\n')

    print(f"寫出 {args.ntests} 組向量到 {out_path}")

if __name__ == '__main__':
    main()
