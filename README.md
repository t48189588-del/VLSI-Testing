# VLSI-Testing
VLSI testing research repository (From Oct 2025-March 2026)

This repository will have the resources used for the VLSI testing and the required laboratories by prof. Wen and prof. Stefan

# Updating required (Oct-2025)
When running './2_make_random_tests.py' I get error "AttributeError: `np.unicode_` was removed in the NumPy 2.0 release. Use `np.str_` instead."
In order to run the python script. Had to change the code as suggested `np.unicode_` to `np.str_`

# Running [stuck_at_fault_simulator](./fsim-contest.github/fsim-contest.github/3_stuck_at_fault_simulator.py)
If running from terminal, it must include the bench and test as arguments for example if making bench and test for c17 circuit, the code should be as follows: 

```
python3 ../3_stuck_at_fault_simulator data.nogit/c17.bench data.nogit/c17.tests
```
