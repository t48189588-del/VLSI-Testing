#!/usr/bin/env python3

"""
SCOAP analysis for a combinational BENCH circuit.

Calculates:

    CC0(n) = combinational controllability to logic 0
    CC1(n) = combinational controllability to logic 1
    CO(n)  = combinational observability

For primary inputs:
    CC0 = 1
    CC1 = 1

For primary outputs:
    CO = 0

Gate formulas follow standard SCOAP definitions.

Supported gates:
    AND
    NAND
    OR
    NOR
    NOT
    BUFF / BUF / BUFFER
"""

from dataclasses import dataclass
from collections import defaultdict
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

            # Remove comments
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
                gate_type = m.group(2).upper()

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
# Build circuit information
# ============================================================

def build_circuit(inputs, outputs, gates):

    """
    Build:

        fanout[source] = [(gate_output, pin), ...]

    and

        gate_by_output[output] = Gate
    """

    fanout = defaultdict(list)

    gate_by_output = {}

    for gate in gates:

        gate_by_output[gate.output] = gate

        for pin, source in enumerate(gate.inputs):

            fanout[source].append(
                (gate.output, pin)
            )

    return fanout, gate_by_output


# ============================================================
# SCOAP helper functions
# ============================================================

INF = float("inf")


def safe_add(*values):

    """
    Add SCOAP values while preserving infinity.
    """

    if any(v == INF for v in values):
        return INF

    return sum(values)


# ============================================================
# Forward SCOAP calculation
# ============================================================

def calculate_controllability(
    inputs,
    gates
):

    """
    Calculate CC0 and CC1.

    Primary inputs:

        CC0 = 1
        CC1 = 1

    Gates are processed in topological order.

    Since a normal BENCH circuit is topologically ordered,
    the supplied gate order is sufficient. We nevertheless
    use the gate dependencies to make the implementation
    robust.
    """

    cc0 = {}
    cc1 = {}

    # --------------------------------------------------------
    # Primary inputs
    # --------------------------------------------------------

    for n in inputs:

        cc0[n] = 1
        cc1[n] = 1

    # --------------------------------------------------------
    # Process gates
    # --------------------------------------------------------

    for gate in gates:

        typ = gate.gate_type
        ins = gate.inputs
        out = gate.output

        # Make sure all input SCOAP values exist.
        for n in ins:

            if n not in cc0:

                raise ValueError(
                    f"Signal {n} used by gate {out} "
                    f"has not been processed."
                )

        # ====================================================
        # AND
        #
        # y = a & b & ...
        #
        # CC1 = sum(CC1(inputs)) + 1
        #
        # CC0 = min(CC0(inputs)) + 1
        # ====================================================

        if typ == "AND":

            cc1[out] = (
                sum(cc1[n] for n in ins) + 1
            )

            cc0[out] = (
                min(cc0[n] for n in ins) + 1
            )

        # ====================================================
        # NAND
        #
        # y = ~(AND)
        #
        # CC0 = sum(CC1(inputs)) + 1
        #
        # CC1 = min(CC0(inputs)) + 1
        # ====================================================

        elif typ == "NAND":

            cc0[out] = (
                sum(cc1[n] for n in ins) + 1
            )

            cc1[out] = (
                min(cc0[n] for n in ins) + 1
            )

        # ====================================================
        # OR
        #
        # CC0 = sum(CC0(inputs)) + 1
        #
        # CC1 = min(CC1(inputs)) + 1
        # ====================================================

        elif typ == "OR":

            cc0[out] = (
                sum(cc0[n] for n in ins) + 1
            )

            cc1[out] = (
                min(cc1[n] for n in ins) + 1
            )

        # ====================================================
        # NOR
        #
        # CC0 = min(CC1(inputs)) + 1
        #
        # CC1 = sum(CC0(inputs)) + 1
        # ====================================================

        elif typ == "NOR":

            cc0[out] = (
                min(cc1[n] for n in ins) + 1
            )

            cc1[out] = (
                sum(cc0[n] for n in ins) + 1
            )

        # ====================================================
        # NOT
        # ====================================================

        elif typ == "NOT":

            if len(ins) != 1:

                raise ValueError(
                    f"NOT gate {out} has "
                    f"{len(ins)} inputs."
                )

            n = ins[0]

            cc0[out] = cc1[n] + 1
            cc1[out] = cc0[n] + 1

        # ====================================================
        # BUFFER
        # ====================================================

        elif typ in (
            "BUFF",
            "BUF",
            "BUFFER"
        ):

            if len(ins) != 1:

                raise ValueError(
                    f"BUFF gate {out} has "
                    f"{len(ins)} inputs."
                )

            n = ins[0]

            cc0[out] = cc0[n] + 1
            cc1[out] = cc1[n] + 1

        else:

            raise ValueError(
                f"Unsupported gate type '{typ}' "
                f"at output {out}"
            )

    return cc0, cc1


# ============================================================
# Backward SCOAP observability calculation
# ============================================================

def calculate_observability(
    inputs,
    outputs,
    gates,
    cc0,
    cc1
):

    """
    Calculate CO for every signal.

    Primary outputs:

        CO = 0

    For a gate:

        CO(input) =
            CO(output)
            + 1
            + cost of controlling all
              other inputs to the
              non-controlling value.

    Standard formulas:

    AND:
        controlling value = 0
        non-controlling = 1

        CO(x_i) =
            CO(y) + 1
            + sum(CC1(x_j)), j != i

    NAND:
        same propagation condition as AND

        CO(x_i) =
            CO(y) + 1
            + sum(CC1(x_j)), j != i

    OR:
        controlling value = 1
        non-controlling = 0

        CO(x_i) =
            CO(y) + 1
            + sum(CC0(x_j)), j != i

    NOR:
        same propagation condition as OR

        CO(x_i) =
            CO(y) + 1
            + sum(CC0(x_j)), j != i

    NOT:
        CO(input) = CO(output) + 1

    BUFF:
        CO(input) = CO(output) + 1
    """

    co = {
        n: INF
        for n in set(
            list(cc0.keys()) +
            list(cc1.keys())
        )
    }

    # --------------------------------------------------------
    # Primary outputs
    # --------------------------------------------------------

    for n in outputs:

        co[n] = 0

    # --------------------------------------------------------
    # Process gates backwards
    # --------------------------------------------------------

    for gate in reversed(gates):

        out = gate.output
        typ = gate.gate_type
        ins = gate.inputs

        # Output may not be directly observable if this is
        # not on a path to a primary output.

        if co[out] == INF:
            continue

        # ====================================================
        # AND / NAND
        #
        # To propagate input i:
        # every other input must be 1.
        # ====================================================

        if typ in ("AND", "NAND"):

            for i, n in enumerate(ins):

                other_inputs = [
                    x
                    for j, x in enumerate(ins)
                    if j != i
                ]

                cost = sum(
                    cc1[x]
                    for x in other_inputs
                )

                candidate = (
                    co[out]
                    + 1
                    + cost
                )

                co[n] = min(
                    co[n],
                    candidate
                )

        # ====================================================
        # OR / NOR
        #
        # To propagate input i:
        # every other input must be 0.
        # ====================================================

        elif typ in ("OR", "NOR"):

            for i, n in enumerate(ins):

                other_inputs = [
                    x
                    for j, x in enumerate(ins)
                    if j != i
                ]

                cost = sum(
                    cc0[x]
                    for x in other_inputs
                )

                candidate = (
                    co[out]
                    + 1
                    + cost
                )

                co[n] = min(
                    co[n],
                    candidate
                )

        # ====================================================
        # NOT / BUFF
        # ====================================================

        elif typ in (
            "NOT",
            "BUFF",
            "BUF",
            "BUFFER"
        ):

            if len(ins) != 1:

                raise ValueError(
                    f"{typ} gate {out} has "
                    f"{len(ins)} inputs."
                )

            n = ins[0]

            candidate = co[out] + 1

            co[n] = min(
                co[n],
                candidate
            )

        else:

            raise ValueError(
                f"Unsupported gate type '{typ}' "
                f"at output {out}"
            )

    return co


# ============================================================
# Topological ordering
# ============================================================

def topological_sort(inputs, gates):

    """
    Topologically sort gates.

    This makes the script independent of whether the BENCH
    file happens to list gates in strict topological order.
    """

    gate_by_output = {
        gate.output: gate
        for gate in gates
    }

    input_set = set(inputs)

    visited = set()
    visiting = set()
    ordered = []

    def visit_gate(output):

        if output in visited:
            return

        if output in visiting:

            raise ValueError(
                f"Combinational loop detected at {output}"
            )

        visiting.add(output)

        gate = gate_by_output[output]

        for source in gate.inputs:

            if source in gate_by_output:

                visit_gate(source)

            elif source not in input_set:

                raise ValueError(
                    f"Signal {source} has no driver."
                )

        visiting.remove(output)

        visited.add(output)

        ordered.append(gate)

    for gate in gates:

        visit_gate(gate.output)

    return ordered


# ============================================================
# Write SCOAP results
# ============================================================

def write_results(
    filename,
    signals,
    inputs,
    outputs,
    cc0,
    cc1,
    co
):

    input_set = set(inputs)
    output_set = set(outputs)

    with open(filename, "w") as f:

        f.write(
            "signal,type,CC0,CC1,CO\n"
        )

        for n in sorted(signals):

            if n in input_set:
                typ = "PI"

            elif n in output_set:
                typ = "PO"

            else:
                typ = "INTERNAL"

            f.write(
                f"{n},{typ},"
                f"{cc0[n]},"
                f"{cc1[n]},"
                f"{co[n]}\n"
            )


# ============================================================
# Main
# ============================================================

def main():

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "    python scoap_c880.py c880.bench"
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
    # Topological ordering
    # --------------------------------------------------------

    gates = topological_sort(
        inputs,
        gates
    )

    # --------------------------------------------------------
    # Collect signals
    # --------------------------------------------------------

    signals = set(inputs)
    signals.update(outputs)

    for gate in gates:

        signals.add(gate.output)
        signals.update(gate.inputs)

    # --------------------------------------------------------
    # CC0 / CC1
    # --------------------------------------------------------

    cc0, cc1 = calculate_controllability(
        inputs,
        gates
    )

    # --------------------------------------------------------
    # CO
    # --------------------------------------------------------

    co = calculate_observability(
        inputs,
        outputs,
        gates,
        cc0,
        cc1
    )

    # --------------------------------------------------------
    # Print circuit statistics
    # --------------------------------------------------------

    print("=" * 72)
    print("SCOAP ANALYSIS")
    print("=" * 72)

    print(
        f"Primary inputs  : {len(inputs)}"
    )

    print(
        f"Primary outputs : {len(outputs)}"
    )

    print(
        f"Gates           : {len(gates)}"
    )

    print(
        f"Signals         : {len(signals)}"
    )

    # --------------------------------------------------------
    # Print table
    # --------------------------------------------------------

    print()
    print(
        f"{'Signal':>8} "
        f"{'Type':>10} "
        f"{'CC0':>8} "
        f"{'CC1':>8} "
        f"{'CO':>8}"
    )

    print("-" * 50)

    input_set = set(inputs)
    output_set = set(outputs)

    for n in sorted(signals):

        if n in input_set:
            typ = "PI"

        elif n in output_set:
            typ = "PO"

        else:
            typ = "INTERNAL"

        print(
            f"{n:>8} "
            f"{typ:>10} "
            f"{cc0[n]:>8} "
            f"{cc1[n]:>8} "
            f"{co[n]:>8}"
        )

    # --------------------------------------------------------
    # Write CSV
    # --------------------------------------------------------

    write_results(
        "c880_scoap.csv",
        signals,
        inputs,
        outputs,
        cc0,
        cc1,
        co
    )

    print()
    print(
        "Results written to:"
    )

    print(
        "    c880_scoap.csv"
    )


if __name__ == "__main__":
    main()
