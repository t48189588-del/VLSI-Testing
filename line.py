#!/usr/bin/env python3

"""
PO-directed line justification / propagation / backtracing
for a combinational BENCH circuit.

For every primary output, determine the signals involved in
backtracing from that PO toward the primary inputs.

The result contains:

    propagation signals
        Signals that can carry the propagated fault effect.

    justification signals
        Side inputs that must be assigned the non-controlling
        value to allow propagation through a gate.

    all signals
        Union of propagation + justification signals.

The script supports:

    AND
    NAND
    OR
    NOR
    NOT
    BUFF / BUF / BUFFER

Example:

    python po_backtrace.py c880.bench

Output:

    PO 388
        propagation : [...]
        justification: [...]
        all          : [...]

    ...

A JSON file is also generated:

    c880_po_backtrace.json
"""

from dataclasses import dataclass
from collections import defaultdict
import json
import re
import sys


# ============================================================
# Data structures
# ============================================================

@dataclass
class Gate:
    output: int
    gate_type: str
    inputs: list


# ============================================================
# BENCH parser
# ============================================================

def parse_bench(filename):

    inputs = []
    outputs = []
    gates = []

    input_re = re.compile(
        r"INPUT\((\d+)\)"
    )

    output_re = re.compile(
        r"OUTPUT\((\d+)\)"
    )

    gate_re = re.compile(
        r"(\d+)\s*=\s*([A-Za-z]+)\s*\(([^)]*)\)"
    )

    with open(filename, "r") as f:

        for line_number, line in enumerate(f, 1):

            line = line.split("#", 1)[0].strip()

            if not line:
                continue

            # ------------------------------------------------
            # INPUT
            # ------------------------------------------------

            m = input_re.fullmatch(line)

            if m:
                inputs.append(
                    int(m.group(1))
                )
                continue

            # ------------------------------------------------
            # OUTPUT
            # ------------------------------------------------

            m = output_re.fullmatch(line)

            if m:
                outputs.append(
                    int(m.group(1))
                )
                continue

            # ------------------------------------------------
            # GATE
            # ------------------------------------------------

            m = gate_re.fullmatch(line)

            if m:

                output = int(m.group(1))

                gate_type = (
                    m.group(2).upper()
                )

                input_list = [
                    int(x.strip())
                    for x in m.group(3).split(",")
                    if x.strip()
                ]

                gates.append(
                    Gate(
                        output=output,
                        gate_type=gate_type,
                        inputs=input_list
                    )
                )

                continue

            raise ValueError(
                f"Cannot parse line {line_number}: {line}"
            )

    return inputs, outputs, gates


# ============================================================
# Topological ordering
# ============================================================

def topological_sort(inputs, gates):

    gate_by_output = {
        gate.output: gate
        for gate in gates
    }

    input_set = set(inputs)

    visited = set()
    visiting = set()
    ordered = []

    def visit(signal):

        if signal in visited:
            return

        if signal in visiting:

            raise ValueError(
                f"Combinational loop detected at signal {signal}"
            )

        # PI
        if signal in input_set:

            visited.add(signal)
            return

        # Internal signal
        if signal not in gate_by_output:

            raise ValueError(
                f"Signal {signal} has no driver"
            )

        visiting.add(signal)

        gate = gate_by_output[signal]

        for inp in gate.inputs:

            visit(inp)

        visiting.remove(signal)

        visited.add(signal)

        ordered.append(gate)

    for gate in gates:

        visit(gate.output)

    return ordered


# ============================================================
# Circuit information
# ============================================================

def build_circuit(gates):

    gate_by_output = {}

    fanout = defaultdict(list)

    for gate in gates:

        gate_by_output[gate.output] = gate

        for pin, signal in enumerate(gate.inputs):

            fanout[signal].append(
                (gate.output, pin)
            )

    return gate_by_output, fanout


# ============================================================
# Gate propagation rules
# ============================================================

def propagation_side_inputs(gate, selected_input):

    """
    Return the side inputs that must be set to the
    non-controlling value in order to propagate the
    selected input through the gate.

    For AND/NAND:
        controlling value = 0
        side inputs = 1

    For OR/NOR:
        controlling value = 1
        side inputs = 0

    NOT/BUFF:
        no side inputs.
    """

    typ = gate.gate_type

    side_inputs = []

    for index, signal in enumerate(gate.inputs):

        if index == selected_input:
            continue

        side_inputs.append(signal)

    if typ in ("AND", "NAND"):

        return side_inputs, 1

    if typ in ("OR", "NOR"):

        return side_inputs, 0

    if typ in (
        "NOT",
        "BUFF",
        "BUF",
        "BUFFER"
    ):

        return [], None

    raise ValueError(
        f"Unsupported gate: {typ}"
    )


# ============================================================
# Recursive PO backtrace
# ============================================================

def backtrace_from_po(
    po,
    gate_by_output,
    inputs
):

    """
    Recursively backtrace from one PO.

    Returns:

        propagation
        justification
        all_signals

    Important:

    This is not a single ATPG path.

    For every gate encountered, every possible input path
    is explored.

    Thus the returned sets represent the complete structural
    PO backtrace cone together with the signals needed for
    propagation through those gates.
    """

    propagation = set()
    justification = set()

    visited = set()

    input_set = set(inputs)

    def recurse(
        signal,
        mode="propagation"
    ):

        state = (
            signal,
            mode
        )

        if state in visited:
            return

        visited.add(state)

        # ----------------------------------------------------
        # Primary input
        # ----------------------------------------------------

        if signal in input_set:

            if mode == "propagation":
                propagation.add(signal)

            else:
                justification.add(signal)

            return

        # ----------------------------------------------------
        # No gate
        # ----------------------------------------------------

        if signal not in gate_by_output:

            # Treat as an observable signal.
            if mode == "propagation":
                propagation.add(signal)
            else:
                justification.add(signal)

            return

        gate = gate_by_output[signal]

        # ----------------------------------------------------
        # Current gate output belongs to the backtrace cone.
        # ----------------------------------------------------

        if mode == "propagation":

            propagation.add(signal)

        else:

            justification.add(signal)

        typ = gate.gate_type

        # ----------------------------------------------------
        # NOT / BUFF
        # ----------------------------------------------------

        if typ in (
            "NOT",
            "BUFF",
            "BUF",
            "BUFFER"
        ):

            recurse(
                gate.inputs[0],
                mode
            )

            return

        # ----------------------------------------------------
        # AND / NAND
        #
        # Every input can potentially carry the propagated
        # value.
        #
        # For each selected input:
        #
        #   selected input -> propagation
        #
        #   all other inputs -> justification
        # ----------------------------------------------------

        if typ in (
            "AND",
            "NAND"
        ):

            for selected in range(
                len(gate.inputs)
            ):

                # Selected input
                recurse(
                    gate.inputs[selected],
                    "propagation"
                )

                # Side inputs
                for i in range(
                    len(gate.inputs)
                ):

                    if i == selected:
                        continue

                    recurse(
                        gate.inputs[i],
                        "justification"
                    )

            return

        # ----------------------------------------------------
        # OR / NOR
        # ----------------------------------------------------

        if typ in (
            "OR",
            "NOR"
        ):

            for selected in range(
                len(gate.inputs)
            ):

                # Selected input
                recurse(
                    gate.inputs[selected],
                    "propagation"
                )

                # Side inputs
                for i in range(
                    len(gate.inputs)
                ):

                    if i == selected:
                        continue

                    recurse(
                        gate.inputs[i],
                        "justification"
                    )

            return

        raise ValueError(
            f"Unsupported gate type: {typ}"
        )

    # Start at PO.
    recurse(
        po,
        "propagation"
    )

    all_signals = (
        propagation |
        justification
    )

    return (
        propagation,
        justification,
        all_signals
    )


# ============================================================
# More useful PO cone analysis
# ============================================================

def calculate_po_backtrace(
    inputs,
    outputs,
    gates
):

    gate_by_output, fanout = build_circuit(
        gates
    )

    results = {}

    for po in outputs:

        (
            propagation,
            justification,
            all_signals
        ) = backtrace_from_po(
            po,
            gate_by_output,
            inputs
        )

        results[po] = {
            "propagation": sorted(
                propagation
            ),
            "justification": sorted(
                justification
            ),
            "all_signals": sorted(
                all_signals
            )
        }

    return results


# ============================================================
# Print result
# ============================================================

def print_results(
    outputs,
    results
):

    for po in outputs:

        result = results[po]

        print()
        print("=" * 72)
        print(f"PRIMARY OUTPUT {po}")
        print("=" * 72)

        print(
            f"Propagation ({len(result['propagation'])}):"
        )

        print(
            result["propagation"]
        )

        print()

        print(
            f"Justification ({len(result['justification'])}):"
        )

        print(
            result["justification"]
        )

        print()

        print(
            f"All signals ({len(result['all_signals'])}):"
        )

        print(
            result["all_signals"]
        )


# ============================================================
# Save JSON
# ============================================================

def save_json(
    filename,
    results
):

    # JSON requires string keys.
    serializable = {
        str(po): result
        for po, result in results.items()
    }

    with open(filename, "w") as f:

        json.dump(
            serializable,
            f,
            indent=4
        )


# ============================================================
# Main
# ============================================================

def main():

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "    python po_backtrace.py c880.bench"
        )

        sys.exit(1)

    filename = sys.argv[1]

    # --------------------------------------------------------
    # Parse
    # --------------------------------------------------------

    inputs, outputs, gates = parse_bench(
        filename
    )

    # --------------------------------------------------------
    # Topological order
    # --------------------------------------------------------

    gates = topological_sort(
        inputs,
        gates
    )

    # --------------------------------------------------------
    # Calculate
    # --------------------------------------------------------

    results = calculate_po_backtrace(
        inputs,
        outputs,
        gates
    )

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print("=" * 72)
    print("PO BACKTRACE / PROPAGATION / JUSTIFICATION")
    print("=" * 72)

    print(
        f"Primary outputs : {len(outputs)}"
    )

    print(
        f"Gates           : {len(gates)}"
    )

    print_results(
        outputs,
        results
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_json(
        "c880_po_backtrace.json",
        results
    )

    print()
    print("=" * 72)
    print(
        "Results written to c880_po_backtrace.json"
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
