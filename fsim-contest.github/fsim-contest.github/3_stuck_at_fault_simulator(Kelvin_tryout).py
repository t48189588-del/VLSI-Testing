#!/usr/bin/env python3

import argparse

import numpy as np
from kyupy import bench, log, logic
import datetime

#setting time to Japan time (UTC+9)
jpTime=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
#when testing started
t0=jpTime.now()


def log (msg:str):
    """
    for logging system and debugging purposes
    """
    delta=jpTime.now()-t0 #show the running time
    print(f'{delta}...{msg}')

def main():

    # load circuit and test data
    parser = argparse.ArgumentParser()
    parser.add_argument('bench')
    parser.add_argument('tests')
    args = parser.parse_args()
    circuit = bench.load(args.bench)
    log.info(f'Circuit {circuit}')
    with open(args.tests, 'r') as file:
        tests = logic.mvarray(*file.read().splitlines())
    log.info(f'TestDataShape {tests.shape}')

    #
    # Add fault simulation code
    #

    fault_count_total = 1234  # mock result
    fault_count_detected = 1233  # mock result

    # print results
    log.info(f'TotalFaults {fault_count_total}')
    log.info(f'DetectedFaults {fault_count_detected}')
    log.info(f'FaultCoverage {fault_count_detected/fault_count_total*100:.2f}%')

if __name__ == '__main__':
    
    print(f'Testing starting at: {t0}')
    main()