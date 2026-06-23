# Fault Simulation

PPSFP (Parallel-Pattern Single-Fault Propagation) style fault simulators and other utility functions for use in various projects.
These fault simulators are meant to be correct (ensured by unit-tests) and reasonably fast.

Fault simulation has $O(n^3)$ complexity. Every *fault* is simulated with every *pattern* involving every combinational *gate* in the circuit. We measure performance in terms of `gates * faults * patterns / second`. How fast can we make it?

## Quick Start

This project has submodules. To ensure everything is up-to-date, run
```
git submodule update --init --recursive
```
after `git clone`, `git pull` or `git checkout`.

This project manages reproducible programming environments with:
- [uv](https://docs.astral.sh/uv/) for managing python environments.
- [nix](https://nixos.org) for managing non-python tools and benchmark designs. Follow [this guide](https://librelane.readthedocs.io/en/stable/installation/nix_installation/index.html) or [this guide](https://github.com/fossi-foundation/nix-eda/blob/main/docs/installation.md) to setup [nix-eda](https://github.com/fossi-foundation/nix-eda/tree/main) binary cache to avoid re-building EDA-related tools.

Run all unit-tests: `uv run pytest`

Run a naive, baseline fault simulation with 1024 random patterns: `uv run main.py tests/c6288.bench`

Same on an 18k-gate circuit: `uv run main.py polito-itc99-b15-sky130`

`nix develop` makes [quaigh](https://github.com/coloquinte/quaigh) available, another simulator/atpg written in rust.

To run Jupyter Notebooks in the reproducible programming environment, install a kernelspec:
```
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --env PATH ${PATH} --name=uv-env
```
Run a Jupyter Lab server locally:
```
uv run jupyter lab
```
Choose `uv-env` as kernel in Jupyter Lab.





