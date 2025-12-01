# VLSI-Testing
VLSI testing research repository (From Oct 2025-March 2026)

This repository will have the resources used for the VLSI testing and the required laboratories by prof. Wen and prof. Stefan

# Updating required (Oct-2025)
When running './2_make_random_tests.py' I get error "AttributeError: `np.unicode_` was removed in the NumPy 2.0 release. Use `np.str_` instead."
In order to run the python script. Had to change the code as suggested 'np.unicode_' to 'np.str_'

# Running [vlsi.py](./fsim-contest.github/fsim-contest.github/vlsi.py)
If running from terminal, the code should be as follows: 

```
python3 
import vlsi
a=vlsi.SA_faults(<bench file>)
a.generate_diagram() #to generate wokwi diagram code
a.generate_test_vector() #to generate test cubes for testing
```
# Verification scripts before programing
1. A python script was wrote in [testing.ipynb](./fsim-contest.github/fsim-contest.github/testing.ipynb) to verify the information from the bench files.
 

|File|Primary Inputs (PIs)|Primary Outputs (POs)|Logic gates|
|---|---|---|--- |
c1.bench|3|1|6|
c2.bench|3|1|10|
c3.bench|3|1|6|
c17.bench|5|2|6|
c6288.bench|32|32|2416|
c1908.bench|33|25|880|
c432.bench|36|7|160|
c499.bench|41|32|202|
c1355.bench|41|32|546|
c3540.bench|50|22|1669|
c880.bench|60|26|383|
c5315.bench|178|123|2307|
c7552.bench|207|108|3512|
c2670.bench|233|140|1193|

1. After manually reviewing the bench files, **ALL** gates only have one output.
   - For operations for the logic gate, I can ignore the order, prioritize the operation
   - **pending confirmation from prof. Stephan** The order of operation will be from top to bottom on the bench file
2. After manually reviewing the test files, I found the following
   - it's a string of 0/1 followed by '--'(the # of hyphes is the number of outputs)
     - some discrepancies were found

# Programming 
## Data formating
Data is read from the bench file and transformed into a dictionary.
Given the data structure in the bench file and the data in test file a `dict()` will be used as following
`dict[key]=corresponding bit position from the bench file`\
`dict[value]=assigned value from test file or result of the logic operation`

Data manipulation
- Pattern Parallel Single Fault Propagation (PPSFP): Transforms the truth table into an integer value to process into the logic function
> [!Note]
> This is prone to change when further information on data manipulation has been collected 
>
Example on C1.bench
C1 circuit truth table
a|b|c|y|
|---|---|---|---|
0|0|0|0|
0|0|1|1|
0|1|0|0|
0|1|1|0|
1|0|0|0|
1|0|1|1|
1|1|0|1|
1|1|1|1|

PPSFP value <br>
a=[0,0,0,0,1,1,1,1]=(15)<sub>10</sub><br>
b=[0,0,1,1,0,0,1,1]=(51)<sub>10</sub><br>
c=[0,1,0,1,0,1,0,1]=(85)<sub>10</sub><br>
y=[0,1,0,0,0,1,1,1]=(71)<sub>10</sub>
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
**Last update December 1,2025**
Functions coded in [program](./fsim-contest.github/fsim-contest.github/vlsi.py)

`def read_bench:` This function reads the overall information of the circuit.
- primary inputs
- primary outputs
- interconnected signals
- logic gate inputs and outputs
- total possible single stuck at fault circuits

`def read_test:` This function reads the data of the circuit and executes the "correct" behavior and compares to single Stuck at faults and returns the yield.

`def singleSA (signal,value):` This function generates the test cube for the specific signal and the desired value

`def generate_test_vector:` This function generate test cubes/test vector for ALL the single stuck at faults.

`def generate_diagram:` This function generate the [Wokwi](https://wokwi.com/projects/354858054593504257) code for creating the corresponding diagram. **Only for small circuit,10 or less primary inputs**

**pending**
- tranform test cube into test vector
- enable matrix data operations
- restrictions for SAT solver


## Single Stuck-at-fault model

Making a truth table for doing functional testing proved fruitless. When trying to run the truth table for [C6288](./fsim-contest.github/fsim-contest.github/data.nogit/c6288.bench) the VM colapsed after 71 min and only performed 0.0039% of the needed outputs.

Structural testing implemented. Generate a fault in line and obtain the first test cube that allows fault detection.

### Fault colapsing
This approach was recommended by prof. Stefan in order to reduce the amount of required operations. In [file](./fsim-contest.github/fsim-contest.github/fault%20colapsing) all the brute force fault collapsing for all the logic gates was performed.

### Path generations 
#### Propagation
Using 5 value algebra, looks values for the path (signals and logic gates) in order to obtain a faulty value at any primary output. From this process is also generate a list of other signals and the needed values to ensure fault propagation

#### Line justification
Using the values from the propagation function and the desired fault a list of test cubes is generate that will result in the desired behaviour, allowing fault detection.

### SAT solver implementation
#### [Tseitin clauses](https://en.wikipedia.org/wiki/Tseytin_transformation)
This function transform the circuit information (logic gates) into mathematical equations that simulate the behaviour of the circuit.

#### Implementing SAT solver
Receives the tseitin clauses and restrictions needed to generate a test vector.<br>
**Pending** 
1. generate the tseitin clauses for a correct restriction
2. differenciate from a test vector and test cube. 
