# VLSI-Testing
VLSI testing research repository (From Oct 2025-March 2026)

This repository will have the resources used for the VLSI testing and the required laboratories by prof. Wen and prof. Stefan

# Updating required (Oct-2025)
When running './2_make_random_tests.py' I get error "AttributeError: `np.unicode_` was removed in the NumPy 2.0 release. Use `np.str_` instead."
In order to run the python script. Had to change the code as suggested 'np.unicode_' to 'np.str_'

# Running [stuck_at_fault_simulator](./fsim-contest.github/fsim-contest.github/3_stuck_at_fault_simulator.py)
If running from terminal, it must include the bench and test as arguments for example if making bench and test for c17 circuit, the code should be as follows: 

```
python3 ../3_stuck_at_fault_simulator data.nogit/c17.bench data.nogit/c17.tests
```
# Verification scripts before programing
1. A python script was wrote in [testing.ipynb](./fsim-contest.github/fsim-contest.github/testing.ipynb) to verify the information from the bench files.
 - Verify the # of inputs, output, and logic gates in each bench file (compare the comment with the actual ammount of gates)
   - Some discrepancies were found 


| File | Bench comment info (INPUT) | Bench rows info (INPUT) | Test rows info(INPUT) | Bench comment info(OUTPUT) | Bench rows info(OUTPUT) | Test rows info(OUTPUT) | 
|---|---|---|---|---|---|---|
|C1 | 3 |3 |3 |2 |2| 2|
| c17 | 5 | 5 | 5 | 2 | 2 | 2 | 
| c6288 | 32 | 32 | 32 | 32 | 32 | 32 | 
| c1908 | 33 | 33 | 33 | 25 | 25 | 25 | 
| c432 | 36 | 36 | 36 | 7 | 7 | 7 | 
| c1355 | 41 | 41 | 41 | 32 | 32 | 32 | 
| c499 | 41 | 41 | 41 | 32 | 32 | 32 | 
| c3540 | 50 | 50 | 50 | 22 | 22 | 22 | 
| c880 | 60 | 60 | 60 | 26 | 26 | 26 | 
| c5315 | 178 | 178 | 178 | 123 | 123 | 123 | 
| c7552 | 207 | 207 | $${\color{red}208}$$ | 108 | 108 | $${\color{red}107}$$ | 
| c2670 | 233 | 233 | $${\color{red}309}$$ | 140 | 140 | $${\color{red}64}$$ | 
1. After manually reviewing the bench files, **ALL** gates only have one output.
   - For operations for the logic gate, I can ignore the order, prioritize the operation
   - **pending confirmation from prof. Stephan** The order of operation will be from top to bottom on the bench file
2. After manually reviewing the test files, I found the following
   - it's a string of 0/1 followed by '--'(the # of hyphes is the number of outputs)
     - some discrepancies were found

## Diagrams for concept familiarization. 
Based on the previous information. A simple diagram was drawn using [Wokwi](https://wokwi.com/). This diagram was based on [C17 bench](./fsim-contest.github/fsim-contest.github/data.nogit/c17.bench) information

[Diagram link](https://wokwi.com/projects/444225106610273281)

# Programming 
## "Correct" run
Given the data structure in the bench file and the data in test file a `dict()` will be used as following
`dict[key]=corresponding bit position from the bench file`\
`dict[value]=assigned value from test file or result of the logic operation`

### Logic gates

Information was obtained from this [link](https://www.geeksforgeeks.org/python/logic-gates-in-python/)

| Logic gate | Python operator/Expresion | Conditions |
| --- | --- | --- |
| NAND | `result = 0 if a&b else 1` | 
| AND | `a & b` |
| OR | `a \| b` |
| NOT | `result= 1 if a==0 else 0` | only accepts one input |
| NOR | `result = 0 if a\|b else 1 ` |
| BUFF | `result = a`| only accepts one input |
| XOR | `a ^ b` |
| XNOR | `result = 1 if a==b else 0`|

In the case of 3 or more inputs, a recursion will be used as follow
`6 = NAND (1,2,3,4,5)`\
`6 = NAND (NAND (NAND (NAND (1,2),3),4),5)`

### Coding
**Last update October 29,2025**
two functions have been coded in [program](./fsim-contest.github/fsim-contest.github/3_stuck_at_fault_simulator(Kelvin_tryout).py)

`def logic_gate:` This function has the behavior of the logic gates, as explain in the previous section

`def read_bench:` This function reads the overall information of the circuit.
- primary inputs
- primary outputs
- interconnected signals
- logic gate inputs and outputs

`def read_test:` This function reads the data of the circuit and executes the "correct" behavior

**pending**
- run stuck-at faults model
- compare output between "correct" and stuck-at fault model
## Stuck-at-fault model

Making a truth table for doing functional testing proved fruitless. When trying to run the truth table for [C6288](./fsim-contest.github/fsim-contest.github/data.nogit/c6288.bench) the VM colapsed after 71 min and only performed 0.0039% of the needed outputs.

### Fault colapsing
This approach was recommended by prof. Stefan in order to reduce the amount of required operations. In [file](./fsim-contest.github/fsim-contest.github/fault%20colapsing) all the brute force fault collapsing for all the logic gates was performed.

## Path generations
Using the information from circuit structure (the logic gates and the input and outputs) generate the "main" paths and "buffer" paths. With this information generate the best test vector to test the circuit.

| File | Primary input (PI) | Total possible patterns <br> Truth table inputs<br>2^PI|Primari Outputs (PO)| Total paths to evaluate| Time take to generate paths [sec]|
|---|:---:|:---:|:---:|:---:| :---:|
| C1 | 3 | 8 |1 | 8 |0.044 u | 
| c17 | 5 | 32 | 2 | 16 | 0.071 u|
| c6288 | 32 | 4294967296 | 32 | 4832 | 5.1101 | 
| c1908 | 33 | 8589934592 | 25 | 1286| 0.1150 |
| c432 | 36 | 68719476736 | 7 | 366 |5.062 m|
| c1355 | 41 | 2199023255552| 32 | 1100 | 0.072 |
| c499 | 41 |  2199023255552| 32 | 476 | 7.137 m |
| c3540 | 50 | 1125899906842624 | 22 | 2584 | 0.7601|
| c880 | 60 | 1152921504606846976 | 26 | 744 |0.03893 |
| c5315 | 178 | 383123885216472214589586756787577295904684780545900544 |123 |4404|1.4046|
| c7552 | 207 | 205688069665150755269371147819668813122841983204197482918576128 | 108 |5480|2.6805|
| c2670 | 233 | 13803492693581127574869511724554050904902217944340773110325048447598592  | 140 | 2046 |0.3457|