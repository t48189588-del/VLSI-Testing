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

def logic_gate(gate:str, inputs:list):
    '''
    defining the logic gate functioning

    :param str gate: 'NAND', 'AND', 'OR', 'NOT', 'NOR', 'BUFF', 'XOR' name of gates in bench files
    :param list inputs: defines the inputs for the gate [A,B,C...], the number of elements in the function will determine the amount of pins for the logic gate.EXCEPT for NOT gates it will take ONLY the first element

    :return a single logic value to assign to the corresponding 
    '''

    if gate=='NAND':
        holder=1
        [holder:=holder&x for x in inputs]
        return 0 if holder else 1
    elif gate=="AND":
        holder=1
        [holder:=holder&x for x in inputs]
        return 1 if holder else 0
    elif gate=="NOR":
        holder =0
        [holder:=holder|x for x in inputs]
        return 0 if holder else 1
    elif gate=="OR":
        holder =0
        [holder:=holder|x for x in inputs]
        return 1 if holder else 0
    elif gate=="NOR":
        return 0 if inputs[0] else 1
    elif gate=="BUFF":
        return 1 if inputs[0] else 0

def read_bench(file: str):
    '''
    :param str file: it should be the path of the file to read (.bench)
    
    :return dict signal_line: #keys is the signal number #value is the signal logic value
    :return list circ_struc: this contains the interconnection information between the logic gates
    :return list primary_input: a list of the primary input indexes of the circuit
    :return list priamry_output: a list of the primary output indexes of the circuit
    '''
    aux=0
    signal_line={} #key:singal line value: logic value (0/1)
    primary_input=[]
    primary_output=[]
    circ_struc=[] #circuit structure
    with open(file) as f:
        while True:
            a=f.readline().strip()
            if aux>3:
                break
            if not(a):
                aux+=1
                continue
            else:
                if "#" in a:
                    continue
                else:
                    if 'INPUT' in a or 'OUTPUT' in a: #connections for primary input and primary output
                        b=''.join(filter(str.isnumeric,a))
                        signal_line[b]=''
                        if 'INPUT' in a:
                            primary_input.append(b)
                        else:
                            primary_output.append(b)
                    else: # signal = gate (input signal)
                        signal_line[a.split(' = ')[0]]=''
                        circ_struc.append(a)
    f.close()
    log (f"Finished reading bench file: {file}")
    return signal_line,circ_struc,primary_input,primary_output

def read_test(test_file:str, signal_line:dict, circ_struc:list, primary_input:list,primary_output:list):
    '''
    Args:
        test_file(str): the path of the file to read the data to test (.test)
        signal_line(dict): contains the "order" of the circuit
        circ_struc(list): it contains the information of the circuit behavior
        primary_input(list): the primary inputs of the circuit. It will be used to read the data from the test file
        primary_output(list): the primary outputs of the circuit.

    Returns:
        signal_line(dict): it contains the information of the circuit after run
        circuit_output(list): it contains only the primary output logic value
    '''
    #reading the test file for data and testing
    #this script produces the "correct" behaviour
    with open(test_file) as f:
        while True:
            line=f.readline().strip()
            if not(line):
                break
            else: #I assume the data is organized in the bench stated order
                #assigning the test data to the corresponding signals
                for a in range(len(primary_input)):
                    try:
                        signal_line[primary_input[a]]=int(line[a])
                    except:
                        continue
                
                #executing the testing from the bench file (running the circuit)
                #structure= output signal= logic gate (input signal)
                for a in circ_struc:
                    output_signal=a.split(' = ')[0]
                    gate=a.split(' = ')[1].split('(')[0]
                    input_signal_index=a.split(' = ')[1].split('(')[1][:-1]
                    input_signals=[signal_line[x.strip()] for x in input_signal_index.split(',')]
                    signal_line[output_signal]=logic_gate(gate,input_signals)
                circuit_output=[signal_line[x] for x in primary_output]
                # print(f'Data input: {line[:line.index('-')]}, \tData output: {circuit_output}')
    f.close()
    log(f"Finished running test file: {test_file}")
    return signal_line, circuit_output

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