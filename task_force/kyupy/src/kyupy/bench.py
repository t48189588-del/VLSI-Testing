"""A parser for the ISCAS89 benchmark format.

The ISCAS89 benchmark format (`.bench`-suffix) is a very simple textual description of gate-level netlists.
Historically it was first used in the
`ISCAS89 benchmark set <https://people.engr.ncsu.edu/brglez/CBL/benchmarks/ISCAS89/>`_.
Besides loading these benchmarks, this module is also useful for easily constructing simple circuits:
``c = bench.parse('input(x, y) output(a, o, n) a=and(x,y) o=or(x,y) n=not(x)')``.
"""

from lark import Lark, Transformer

from .circuit import Circuit, Node, Line
from . import readtext, batchrange

def treeify(l, max_degree=4):
    if len(l) <= max_degree: return l
    return treeify([l[bo:bo+bs] for bo, bs in batchrange(len(l), max_degree)])


class BenchTransformer(Transformer):

    def __init__(self, name):
        super().__init__()
        self.c = Circuit(name)

    def start(self, _): return self.c

    def parameters(self, args): return [self.c.get_or_add_fork(str(name)) for name in args if name is not None]

    def interface(self, args): self.c.io_nodes.extend(args[0])

    def _cell_tree_inner(self, name, kind, inner_kind, drivers):
        cell = Node(self.c, name, f'{kind}{len(drivers)}')
        fork = self.c.get_or_add_fork(name)
        Line(self.c, cell, fork)
        for i, d in enumerate(drivers):
            while isinstance(d, list) and len(d) == 1: d = d[0]
            if isinstance(d, list):
                d = self._cell_tree_inner(f'{name}~{i}', inner_kind, inner_kind, d)
            Line(self.c, d, cell)
        return fork

    def cell_tree(self, name, kind, drivers):
        root_kind = kind.upper()
        inner_kind = root_kind
        if root_kind == 'NAND': inner_kind = 'AND'
        if root_kind == 'NOR': inner_kind = 'OR'
        if root_kind == 'XNOR': inner_kind = 'XOR'
        return self._cell_tree_inner(name, root_kind, inner_kind, treeify(drivers))

    def assignment(self, args):
        name, kind, drivers = args
        if kind.upper() in ('AND', 'NAND', 'OR', 'NOR', 'XOR', 'XNOR'):
            self.cell_tree(name, kind, drivers)
            return
        if kind.upper().startswith('BUF'):
            kind = 'BUF1'
        elif kind.upper().startswith('INV') or kind.upper().startswith('NOT'):
            kind = 'INV1'
        cell = Node(self.c, str(name), str(kind))
        Line(self.c, cell, self.c.get_or_add_fork(str(name)))
        for d in drivers: Line(self.c, d, cell)


GRAMMAR = r"""
    start: (statement)*
    statement: input | output | assignment
    input: ("INPUT" | "input") parameters -> interface
    output: ("OUTPUT" | "output") parameters -> interface
    assignment: NAME "=" NAME parameters
    parameters: "(" [ NAME ( "," NAME )* ] ")"
    NAME: /[-_a-z0-9]+/i
    %ignore ( /\r?\n/ | "#" /[^\n]*/ | /[\t\f ]/ )+
    """


def parse(text, name=None) -> Circuit:
    """Parses the given ``text`` as ISCAS89 bench code.

    :param text: A string with bench code.
    :param name: The name of the circuit. Circuit names are not included in bench descriptions.
    :return: A :class:`Circuit` object.
    """
    return Lark(GRAMMAR, parser="lalr", transformer=BenchTransformer(name)).parse(text) # type: ignore


def load(file, name=None):
    """Parses the contents of ``file`` as ISCAS89 bench code.

    :param file: The file to be loaded. Files with `.gz`-suffix are decompressed on-the-fly.
    :param name: The name of the circuit. If None, the file name is used as circuit name.
    :return: A :class:`Circuit` object.
    """
    return parse(readtext(file), name=name or str(file))
