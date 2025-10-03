#!/usr/bin/env python3

from pathlib import Path
import argparse

import numpy as np
from kyupy import bench, log, logic

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='data.nogit/c17.bench')
    parser.add_argument('-o', '--outputfile')
    parser.add_argument('-n', '--ntests', default=100)
    args = parser.parse_args()
    inputfile = Path(args.inputfile)
    outputfile = Path(args.outputfile) if args.outputfile else inputfile.with_suffix('.tests')

    # load circuit
    circuit = bench.load(inputfile)
    log.info(f'Circuit {circuit}')
    input_mask = np.array([len(node.ins) == 0 for node in circuit.io_nodes], dtype=bool)
    log.info(f'InputPorts {np.sum(input_mask)}')

    # generate and store random test patterns
    np.random.seed(42)
    tests = np.random.randint(2, size=(len(input_mask), int(args.ntests)), dtype=np.uint8) * logic.ONE
    tests[~input_mask] = logic.UNASSIGNED  # all outputs are unassigned
    log.info(f'Writing {outputfile}')
    with open(outputfile, 'w') as f:
        f.write(logic.mv_str(tests))

if __name__ == '__main__':
    main()