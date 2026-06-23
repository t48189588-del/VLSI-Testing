"""A set of tools for static (structural) analysis of gate-level circuits.
"""

from collections import defaultdict
from itertools import product

import numpy as np

from kyupy.circuit import Circuit, Node
from kyupy.techlib import TechLib

class LineRoles:
    """Computes signal line roles of a circuit depending on the structural reach of each signal.

    The possible roles are any combination of the following:
    - 'lout' / LOGIC_OUT: there is a structural path to a primary output via zero or more combinational gates.
    - 'lseq' / LOGIC_SEQ: there is a structural path to a D input of a sequential cell via zero or more combinational gates.
    - 'clk' / CLOCK: there is a structural path to a clock input of a sequential cell via zero or more combinational gates.
    - 'rst' / RESET: there is a structural path to an asynchronous set or reset input of a sequential cell via zero or more combinational gates.
    - 'dft' / DFT: there is a structural path to an scan-in or scan-enable input of a sequential cell via zero or more combinational gates.

    Signal lines that may propagate to various cells may have multiple roles.
    The roles are encoded using bit positions in integers.
    The corresponding masks are defines as class constants LOGIC_OUT, LOGIC_SEQ, etc.
    """

    LOGIC_OUT = 1
    LOGIC_SEQ = 2
    CLOCK = 4
    RESET = 8
    DFT = 16

    def __init__(self, circuit: Circuit, tlib: TechLib):
        self.line2roles = np.zeros(len(circuit.lines), dtype=np.uint8)
        """Array of roles for each line index in the circuit.
        """

        outputs = {n for n in circuit.io_nodes if len(n.ins) > 0}

        for n in circuit.reversed_topological_order(tlib):
            if tlib.is_dff(n.kind):
                for il in n.ins.without_nones():
                    pname = tlib.pin_name(n.kind, il.reader_pin)
                    if pname == 'D': self.line2roles[il] = self.LOGIC_SEQ
                    elif pname in ('CK', 'CLK', 'CLK_N'): self.line2roles[il] = self.CLOCK
                    elif pname in ('SET_B', 'RESET_B', 'SETB', 'RSTB', 'RN', 'SN'): self.line2roles[il] = self.RESET
                    elif pname in ('SCD', 'SCE', 'SE', 'SI'): self.line2roles[il] = self.DFT
                    else: raise ValueError(f'Unable to classify pin name "{pname}" for "{n.kind}".')
            elif n in outputs: # or len(n.outs) == 0:
                for il in n.ins.without_nones():
                    self.line2roles[il] = self.LOGIC_OUT
            else:
                lc = 0
                for ol in n.outs.without_nones():
                    lc |= self.line2roles[ol]
                for il in n.ins.without_nones():
                    self.line2roles[il] = lc

        self.roles2lines: defaultdict[int,set[int]] = defaultdict(set)
        """A dictionary that maps a role combination to a set of line indices matching that role combination.
        """
        for li, lc in enumerate(self.line2roles):
            self.roles2lines[lc].add(li)

    @classmethod
    def roles_str(cls, roles: int) -> str:
        """Returns a human-readable string for a role combination given as int.
        """
        roles_list = [n for v, n in (
            (cls.LOGIC_OUT, 'lout'),
            (cls.LOGIC_SEQ, 'lseq'),
            (cls.CLOCK, 'clk'),
            (cls.RESET, 'rst'),
            (cls.DFT, 'dft')) if (roles&v) != 0]
        return 'none' if len(roles_list) == 0 else '|'.join(roles_list)

    @property
    def stats(self):
        """A dictionary mapping each role combination to the number of matching signal lines.
        """
        return {self.roles_str(roles): len(self.roles2lines[roles]) for roles in range(256) if len(self.roles2lines[roles]) > 0}


class FaultSet:
    """Computes eligible fault sites and a collapsed set of stuck-at faults for a circuit.

    Faults in this class are represented by integers of the form: `line_index * 2 + polarity`.
    Line index defines the location in the circuit, and polarity is 0 for stuck-at-0 and 1 for stuck-at-1.
    Faults sites are located only in the combinational portion of the circuit (excluding clock tree, asynchronous set/reset logic, dft/scan).
    Stuck-at faults are collapsed using basic controlling-value theory of simple gates.
    """

    def __init__(self, circuit: Circuit, tlib: TechLib):
        lr = LineRoles(circuit, tlib)

        self.fault_sites = {l.index for l in circuit.lines
            if (lr.line2roles[l] & (lr.LOGIC_OUT|lr.LOGIC_SEQ))  # line propagates to output or sequential element
                and (
                    (l.driver.kind == '__fork__' and len(l.driver.outs) > 1)  # fanout branch
                or (l.driver.kind == '__fork__' and len(l.driver.ins) == 0)  # primary input
                or (l.driver.kind != '__fork__' )  # gate output
                )
        }
        """Set of line indices of all eligible fault sites. A fault site is eligible iff:
        fault effect can propagate via combinational gates (only) to outputs of to a flip-flop, AND
        (fault site is driven by a standard cell OR it is a primary input signal OR it is a branch of a fan-out).
        """

        self.saf_set = {site*2+polarity for site, polarity in product(self.fault_sites, (0, 1))}
        """Set of all stuck-at faults in the circuit. Each stuck-at fault is encoded as integer i with
        i & 1 being the polarity and i // 2 the circuit line index of its location.
        """

        self.saf_equiv_classes : dict[int,set[int]] = {}
        r"""Dictionary mapping a representative stuck-at fault to its set of equivalent faults. The
        representative is always the fault closest to the circuit's outputs. The value set of
        representative f always contains at least f (:math:`f \in` saf_equiv_classes[f]).
        """

        def collect_equivalent_faults(circuit: Circuit, fault: int) -> set:
            site = fault//2
            polarity = fault&1
            driver = circuit.lines[site].driver
            # Stop collapsing at fanout stems, primary inputs, and cells whose
            # output faults have no equivalent single-input fault (XOR/XNOR, MUX, the two-term
            # AND-OR/OR-AND cells, and sequential elements).
            if len(driver.outs) > 1 or len(driver.ins) == 0 or driver.kind in ('XOR2', 'XOR3', 'XOR4', 'XNOR2', 'XNOR3', 'XNOR4', 'MUX21', 'AO22', 'AOI22', 'OA22', 'OAI22', 'DFF', 'LATCH'): return {fault}
            if driver.kind == 'INV1': return {fault} | collect_equivalent_faults(circuit, driver.ins[0].index*2 + (1-polarity))
            if driver.kind in ('BUF1', '__fork__'): return {fault} | collect_equivalent_faults(circuit, driver.ins[0].index*2 + (polarity))

            def collapse(*faults: tuple) -> set:
                """Collapse the output fault onto the given (input_line, stuck_value) pairs."""
                equiv = {fault}
                for site, value in faults:
                    equiv |= collect_equivalent_faults(circuit, site.index*2 + value)
                return equiv

            # Simple gates: driving any input to its controlling value forces the output.
            #   AND : out s-a-0 == every input s-a-0   (out s-a-1 has no equivalent)
            #   NAND: out s-a-1 == every input s-a-0   (out s-a-0 has no equivalent)
            #   OR  : out s-a-1 == every input s-a-1   (out s-a-0 has no equivalent)
            #   NOR : out s-a-0 == every input s-a-1   (out s-a-1 has no equivalent)
            if driver.kind.startswith('NAND'):
                return collapse(*((il, 0) for il in driver.ins.without_nones())) if polarity == 1 else {fault}
            if driver.kind.startswith('AND'):
                return collapse(*((il, 0) for il in driver.ins.without_nones())) if polarity == 0 else {fault}
            if driver.kind.startswith('NOR'):
                return collapse(*((il, 1) for il in driver.ins.without_nones())) if polarity == 0 else {fault}
            if driver.kind.startswith('OR'):
                return collapse(*((il, 1) for il in driver.ins.without_nones())) if polarity == 1 else {fault}

            # AND-OR / OR-AND complex gates: only the "single" (un-paired) terms force the output.
            #   AO21  = (i0&i1) | i2        : out s-a-1 == i2 s-a-1
            #   AOI21 = ~AO21              : out s-a-0 == i2 s-a-1
            #   OA21  = (i0|i1) & i2        : out s-a-0 == i2 s-a-0
            #   OAI21 = ~OA21              : out s-a-1 == i2 s-a-0
            #   AO211 = (i0&i1) | i2 | i3   : out s-a-1 == i2 s-a-1, i3 s-a-1
            #   AOI211= ~AO211             : out s-a-0 == i2 s-a-1, i3 s-a-1
            #   OA211 = (i0|i1) & i2 & i3   : out s-a-0 == i2 s-a-0, i3 s-a-0
            #   OAI211= ~OA211             : out s-a-1 == i2 s-a-0, i3 s-a-0
            if driver.kind == 'AO21':   return collapse((driver.ins[2], 1)) if polarity == 1 else {fault}
            if driver.kind == 'AOI21':  return collapse((driver.ins[2], 1)) if polarity == 0 else {fault}
            if driver.kind == 'OA21':   return collapse((driver.ins[2], 0)) if polarity == 0 else {fault}
            if driver.kind == 'OAI21':  return collapse((driver.ins[2], 0)) if polarity == 1 else {fault}
            if driver.kind == 'AO211':  return collapse((driver.ins[2], 1), (driver.ins[3], 1)) if polarity == 1 else {fault}
            if driver.kind == 'AOI211': return collapse((driver.ins[2], 1), (driver.ins[3], 1)) if polarity == 0 else {fault}
            if driver.kind == 'OA211':  return collapse((driver.ins[2], 0), (driver.ins[3], 0)) if polarity == 0 else {fault}
            if driver.kind == 'OAI211': return collapse((driver.ins[2], 0), (driver.ins[3], 0)) if polarity == 1 else {fault}

            raise ValueError(f'Unknown node kind {driver.kind}. Circuit should have been resolved to techlib.KYUPY?')

        remaining = self.saf_set.copy()
        circuit_resolved = circuit.copy()
        circuit_resolved.resolve_tlib_cells(tlib)
        for n in circuit.reversed_topological_order(tlib):
            for il in n.ins.without_nones():
                for polarity in (0, 1):
                    repr = il.index*2+polarity
                    if repr in remaining:
                        equiv = collect_equivalent_faults(circuit_resolved, repr) & remaining
                        remaining.difference_update(equiv)
                        self.saf_equiv_classes[repr] = equiv

        self.circuit = circuit
        self.tlib = tlib

    def fault_str(self, fault: int) -> str:
        site = self.circuit.lines[fault//2]
        polarity = '@1' if fault&1 else '@0'
        if site.driver.kind == '__fork__':
            return f'{site.reader.name}/{self.tlib.pin_name(site.reader.kind, site.reader_pin)}{polarity}'
        else:
            return f'{site.driver.name}/{self.tlib.pin_name(site.driver.kind, site.driver_pin, output=True)}{polarity}'
