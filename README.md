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
2. After manually reviewing the bench files, **ALL** gates only have one output.
 - For operations for the logic gate, I can ignore the order, prioritize the operation
 - **pending confirmation from prof. Stephan** The order of operation will be from top to bottom on the bench file
3. After manually reviewing the test files, I found the following
 - it's a string of 0/1 followed by '--'(the # of hyphes is the number of outputs)
  - some discrepancies were found

# Programming 
## "Correct" run
Given the data structure in the bench file and the data in test file a `dict()` will be used as following
`dict[key]=corresponding bit position from the bench file`
`dict[value]=assigned value from test file or result of the logic operation`

## Stuck-at-fautl model
