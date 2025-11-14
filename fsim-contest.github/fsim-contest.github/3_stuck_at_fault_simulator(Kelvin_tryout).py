#!/usr/bin/env python3

import argparse
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
    elif gate=="NOT":
        return 0 if inputs[0] else 1
    elif gate=="BUFF":
        return 1 if inputs[0] else 0

#circuit code
def circuit_code(signal_line:dict, circ_struc:list):
    for a in circ_struc:
        output_signal=a.split(' = ')[0]
        gate=a.split(' = ')[1].split('(')[0]
        input_signal_index=a.split(' = ')[1].split('(')[1][:-1]
        input_signals=[signal_line[x.strip()] for x in input_signal_index.split(',')]
        signal_line[output_signal]=logic_gate(gate,input_signals)
    return signal_line

def truth_table(primary_inputs:list, primary_outputs:list,circ_struc:list):
    '''
    Params:
        primary_inputs(list): A list of the primary input signals index
        primary_outputs(list): A list of the primary output signals index
        circ_struct(list): A list with the relationships between inputs and outputs
    Returns:
        fault_free_circuit(dict): key:binary input for primary inputs value:fault-free output
    '''
    log("Beginning truth table generation")
    b={}
    fault_free_circuit={}
    print(primary_inputs)
    for a in range(2**len(primary_inputs)):
        aux=0
        c=bin(a)[2:].zfill(len(primary_inputs))
        while aux<len(primary_inputs):
            b[primary_inputs[aux]]=int(c[aux])
            aux+=1
        normal_output=circuit_code(b,circ_struc)
        bench_outputs=[normal_output[x] for x in primary_outputs]
        print(bin(a)[2:].zfill(3),bench_outputs)
        fault_free_circuit['0'*(len(primary_inputs)-(len(bin(a))-2))+bin(a)[2:]]=bench_outputs
    log("Finished generating truth table")
    return fault_free_circuit

#reading the bench file to assign the input, output and intermediate connections.
#read only once (the rutine is the same for ALL the data)
def read_bench(bench_file:str):
    """_summary_

    Args
    -------
        bench_file : str
            the path of the bench file to evaluate

    Returns
    -------
        signal_logic_value : dict
            logic value for each of the signal

        circ_struct: list
            relationship input, gate and output

        signal_hierarchy: dict
            signals map of the circuit
        
        truth table: dict
            ONLY if the circuit has 8 or less inputs, the truth table is generated
    """      
    aux=0
    signal_logic_value={} #key:singal line value: logic value (0/1)
    circ_struc=[] #circuit structure
    signal_hierarchy={} #key: level #value[list]: list of inputs. All signals are considered input
    signal_hierarchy[0]=[]
    with open(bench_file) as f:
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
                        # b=''.join(filter(str.isnumeric,a))
                        b=a.split('(')[1][:-1]
                        signal_logic_value[b]=''
                        if 'INPUT' in a:
                            signal_hierarchy[0].append(b)
                    else: # signal = gate (input signal)
                        signal_logic_value[a.split(' = ')[0]]=''
                        circ_struc.append(a)
                        y='0'
                        for z in a.split(' = ')[1].split('(')[1][:-1].split(', '):
                            y=max(y,z)
                        ind=0
                        #evaluates in string format
                        while ind<len(signal_hierarchy):
                            if y not in signal_hierarchy[ind]:
                                ind+=1
                            else:
                                break
                        ind+=1
                        if ind not in signal_hierarchy:
                            signal_hierarchy[ind]=[]
                        signal_hierarchy[ind].append(a.split(' = ')[0])
    f.close()
    log (f"Finished reading bench file: {bench_file}")
    if len(signal_hierarchy[0])<8: #it was chosen 8, in order to use an 8 switch input from wokwi
        log(f'circuit is small enough to perform a functional testing, generating truth table')
        truth=truth_table(signal_hierarchy[0],signal_hierarchy[len(signal_hierarchy)-1],circ_struc)
        return signal_logic_value, circ_struc, signal_hierarchy,truth
    else:
        log(f'circuit has over 10  inputs, too large to perfom a functional testing')
        return signal_logic_value, circ_struc, signal_hierarchy 


def truth_table(primary_inputs:list, primary_outputs:list,circ_struc:list):
    '''
    Params:
        primary_inputs(list): A list of the primary input signals index
        primary_outputs(list): A list of the primary output signals index
        circ_struct(list): A list with the relationships between inputs and outputs
    Returns:
        fault_free_circuit(dict): key:binary input for primary inputs value:fault-free output
    '''
    log("Beginning truth table generation")
    b={}
    fault_free_circuit=[]
    for a in range(2**len(primary_inputs)):
        aux=0
        c=bin(a)[2:].zfill(len(primary_inputs))
        while aux<len(primary_inputs):
            b[primary_inputs[aux]]=int(c[aux])
            aux+=1
        normal_output=circuit_code(b,circ_struc)
        bench_outputs=[normal_output[x] for x in primary_outputs]
        # print(bin(a)[2:].zfill(3),bench_outputs)
        fault_free_circuit.append(bench_outputs)
    log("Finished generating truth table")
    return fault_free_circuit

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
                signal_line=circuit_code(signal_line,circ_struc)
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
    #1. read bench
    #2. generated truth table

    fault_count_total = 1234  # mock result
    fault_count_detected = 1233  # mock result

    # print results
    log.info(f'TotalFaults {fault_count_total}')
    log.info(f'DetectedFaults {fault_count_detected}')
    log.info(f'FaultCoverage {fault_count_detected/fault_count_total*100:.2f}%')

if __name__ == '__main__':
    
    print(f'Testing starting at: {t0}')
    main()