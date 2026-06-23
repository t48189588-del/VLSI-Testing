KyuPy - Pythonic Processing of VLSI Circuits
============================================

KyuPy is a Python package for processing and analysis of non-hierarchical gate-level VLSI designs.
It contains fundamental building blocks for research software in the fields of VLSI test, diagnosis and reliability:

* Efficient data structures for gate-level circuits and related design data.
* Partial [lark](https://github.com/lark-parser/lark) parsers for common design files like
  bench, gate-level Verilog, standard delay format (SDF), standard test interface language (STIL), design exchange format (DEF).
* Bit-parallel gate-level 2-, 4-, and 8-valued logic simulation.
* GPU-accelerated high-throughput gate-level timing simulation.
* High-performance through the use of [numpy](https://numpy.org) and [numba](https://numba.pydata.org).


Getting Started
---------------

KyuPy is available in [PyPI](https://pypi.org/project/kyupy).
It requires Python 3.10 or newer, [lark](https://pypi.org/project/lark), and [numpy](https://numpy.org).
Although optional, [numba](https://numba.pydata.org) should be installed for best performance. [numba-cuda](https://nvidia.github.io/numba-cuda/) is required for GPU/CUDA acceleration.
If numba is not available, KyuPy will automatically fall back to slow, pure Python execution.

The Jupyter Notebook [Introduction.ipynb](https://github.com/s-holst/kyupy/blob/main/examples/Introduction.ipynb) contains some useful examples to get familiar with the API.


Development
-----------

To work with the latest pre-release source code, clone the [KyuPy GitHub repository](https://github.com/s-holst/kyupy).

* Using ``pip``: Run ``pip install -e .`` within your local checkout to make the package available in your Python environment. The source code comes with tests that can be run with ``pytest``.
* Using ``uv``: Run ``uv run pytest`` within your local checkout to get started.
