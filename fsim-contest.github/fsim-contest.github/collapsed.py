#!/usr/bin/env python3

"""
c880 branch-aware single stuck-at fault collapsing.

Fault model
-----------
Single stuck-at-0 / stuck-at-1.

Fault sites
-----------
A fault site is either:

    1. A stem:
         - primary input
         - gate output

    2. A fanout branch:
         - a connection from a source net to a gate input
         - created only when the source net has fanout > 1

For a source with one fanout, the connection is represented by
the source stem itself.

For a source with multiple fanouts, the source stem and every
individual branch are separate fault sites.

Collapsing
----------
Structural fault equivalence:

AND:
    input SA0 <-> output SA0

NAND:
    input SA0 <-> output SA1

OR:
    input SA1 <-> output SA1

NOR:
    input SA1 <-> output SA0

NOT:
    input SA0 <-> output SA1
    input SA1 <-> output SA0

BUFF:
    input SA0 <-> output SA0
    input SA1 <-> output SA1

The input fault site may be a branch site when the source
has multiple fanouts.

Outputs of gates are always stem sites.

Expected result for the supplied c880:

    Fault sites             = 834
    Uncollapsed faults      = 1668
    Collapsed faults        = 850

The exact collapsed count is checked by the program.
"""


from dataclasses import dataclass
from collections import defaultdict
import re
import sys


# ============================================================
# Data structures
# ============================================================

@dataclass(frozen=True, order=True)
class FaultSite:
    """
    Physical fault site.

    kind:
        STEM
        BRANCH

    source:
        Net from which the site originates.

    destination:
        Gate output receiving the branch.
        None for a stem.

    pin:
        Gate input position, starting from 0.
        None for a stem.
    """

    kind: str
    source: int
    destination: int | None = None
    pin: int | None = None

    def name(self):
        if self.kind == "STEM":
            return f"N{self.source}"

        return (
            f"N{self.source}"
            f"->N{self.destination}"
            f"[pin{self.pin + 1}]"
        )


@dataclass(frozen=True, order=True)
class Fault:
    site: FaultSite
    sa: int

    def name(self):
        return f"{self.site.name()} SA{self.sa}"


@dataclass
class Gate:
    output: int
    gate_type: str
    inputs: list[int]


# ============================================================
# Union-Find
# ============================================================

class UnionFind:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, x):

        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x):

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):

        self.add(a)
        self.add(b)

        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return

        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb

        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra

        else:
            self.parent[rb] = ra
            self.rank[ra] += 1


# ============================================================
# Parse BENCH
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
                inputs.append(int(m.group(1)))
                continue

            # ------------------------------------------------
            # OUTPUT
            # ------------------------------------------------

            m = output_re.fullmatch(line)

            if m:
                outputs.append(int(m.group(1)))
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
# Build fanout information
# ============================================================

def build_fanout(gates):

    """
    fanout[source] = list of connections

    Each connection is:

        (destination_gate_output, input_pin)

    Example:

        100 -> gate 200 pin 0
        100 -> gate 300 pin 1

    gives:

        fanout[100] = [
            (200, 0),
            (300, 1)
        ]
    """

    fanout = defaultdict(list)

    for gate in gates:

        for pin, source in enumerate(gate.inputs):

            fanout[source].append(
                (gate.output, pin)
            )

    return fanout


# ============================================================
# Create fault sites
# ============================================================

def create_fault_sites(inputs, gates, fanout):

    """
    Create all physical fault sites.

    Every PI and every gate output has a STEM site.

    If a source has fanout > 1, every individual connection
    gets a BRANCH site.

    If fanout == 1, no separate branch site is created;
    the source STEM represents that line.
    """

    sites = set()

    # --------------------------------------------------------
    # Primary-input stems
    # --------------------------------------------------------

    for n in inputs:

        sites.add(
            FaultSite(
                kind="STEM",
                source=n
            )
        )

    # --------------------------------------------------------
    # Gate-output stems
    # --------------------------------------------------------

    for gate in gates:

        sites.add(
            FaultSite(
                kind="STEM",
                source=gate.output
            )
        )

    # --------------------------------------------------------
    # Fanout branches
    # --------------------------------------------------------

    for source, connections in fanout.items():

        if len(connections) > 1:

            for destination, pin in connections:

                sites.add(
                    FaultSite(
                        kind="BRANCH",
                        source=source,
                        destination=destination,
                        pin=pin
                    )
                )

    return sites


# ============================================================
# Determine the fault site corresponding to a gate input
# ============================================================

def input_fault_site(
    source,
    destination,
    pin,
    fanout
):

    """
    Return the physical fault site at a gate input.

    If source has one fanout:
        use source STEM.

    If source has multiple fanouts:
        use the specific BRANCH.
    """

    if len(fanout[source]) == 1:

        return FaultSite(
            kind="STEM",
            source=source
        )

    return FaultSite(
        kind="BRANCH",
        source=source,
        destination=destination,
        pin=pin
    )


# ============================================================
# Generate all uncollapsed SSFs
# ============================================================

def generate_raw_faults(sites):

    faults = []

    for site in sorted(sites):

        faults.append(
            Fault(site, 0)
        )

        faults.append(
            Fault(site, 1)
        )

    return faults


# ============================================================
# Structural equivalence collapsing
# ============================================================

def collapse_faults(
    inputs,
    gates,
    fanout,
    raw_faults
):

    uf = UnionFind()

    # Add every fault to the DSU.
    for fault in raw_faults:
        uf.add(fault)

    # --------------------------------------------------------
    # Process every gate
    # --------------------------------------------------------

    for gate in gates:

        out_site = FaultSite(
            kind="STEM",
            source=gate.output
        )

        typ = gate.gate_type

        # ----------------------------------------------------
        # Determine the fault site at every gate input
        # ----------------------------------------------------

        input_sites = []

        for pin, source in enumerate(gate.inputs):

            site = input_fault_site(
                source=source,
                destination=gate.output,
                pin=pin,
                fanout=fanout
            )

            input_sites.append(site)

        # ----------------------------------------------------
        # AND
        #
        # input SA0 == output SA0
        # ----------------------------------------------------

        if typ == "AND":

            for site in input_sites:

                uf.union(
                    Fault(site, 0),
                    Fault(out_site, 0)
                )

        # ----------------------------------------------------
        # NAND
        #
        # input SA0 == output SA1
        # ----------------------------------------------------

        elif typ == "NAND":

            for site in input_sites:

                uf.union(
                    Fault(site, 0),
                    Fault(out_site, 1)
                )

        # ----------------------------------------------------
        # OR
        #
        # input SA1 == output SA1
        # ----------------------------------------------------

        elif typ == "OR":

            for site in input_sites:

                uf.union(
                    Fault(site, 1),
                    Fault(out_site, 1)
                )

        # ----------------------------------------------------
        # NOR
        #
        # input SA1 == output SA0
        # ----------------------------------------------------

        elif typ == "NOR":

            for site in input_sites:

                uf.union(
                    Fault(site, 1),
                    Fault(out_site, 0)
                )

        # ----------------------------------------------------
        # NOT
        # ----------------------------------------------------

        elif typ == "NOT":

            if len(input_sites) != 1:

                raise ValueError(
                    f"NOT gate {gate.output} "
                    f"has {len(input_sites)} inputs"
                )

            site = input_sites[0]

            # input SA0 <-> output SA1
            uf.union(
                Fault(site, 0),
                Fault(out_site, 1)
            )

            # input SA1 <-> output SA0
            uf.union(
                Fault(site, 1),
                Fault(out_site, 0)
            )

        # ----------------------------------------------------
        # BUFFER
        # ----------------------------------------------------

        elif typ in (
            "BUFF",
            "BUF",
            "BUFFER"
        ):

            if len(input_sites) != 1:

                raise ValueError(
                    f"BUFF gate {gate.output} "
                    f"has {len(input_sites)} inputs"
                )

            site = input_sites[0]

            # input SA0 <-> output SA0
            uf.union(
                Fault(site, 0),
                Fault(out_site, 0)
            )

            # input SA1 <-> output SA1
            uf.union(
                Fault(site, 1),
                Fault(out_site, 1)
            )

        else:

            raise ValueError(
                f"Unsupported gate type: {typ}"
            )

    # --------------------------------------------------------
    # Build equivalence classes
    # --------------------------------------------------------

    classes = defaultdict(list)

    for fault in raw_faults:

        root = uf.find(fault)

        classes[root].append(fault)

    return uf, classes


# ============================================================
# Choose representative
# ============================================================

def fault_sort_key(fault):

    site = fault.site

    # Prefer STEM over BRANCH for representative.
    kind_order = {
        "STEM": 0,
        "BRANCH": 1
    }

    return (
        kind_order[site.kind],
        site.source,
        -1 if site.destination is None
        else site.destination,
        -1 if site.pin is None
        else site.pin,
        fault.sa
    )


def choose_representatives(classes):

    representatives = []

    for members in classes.values():

        representative = min(
            members,
            key=fault_sort_key
        )

        representatives.append(
            representative
        )

    return sorted(
        representatives,
        key=fault_sort_key
    )


# ============================================================
# Print fault-site information
# ============================================================

def print_site_statistics(
    inputs,
    gates,
    fanout,
    sites
):

    stem_sites = [
        s for s in sites
        if s.kind == "STEM"
    ]

    branch_sites = [
        s for s in sites
        if s.kind == "BRANCH"
    ]

    fanout_sources = [
        source
        for source, connections in fanout.items()
        if len(connections) > 1
    ]

    print()
    print("=" * 72)
    print("FAULT SITE STATISTICS")
    print("=" * 72)

    print(
        f"Primary-input stems       : {len(inputs)}"
    )

    print(
        f"Gate-output stems         : {len(gates)}"
    )

    print(
        f"Total stem sites          : {len(stem_sites)}"
    )

    print(
        f"Fanout source nets        : {len(fanout_sources)}"
    )

    print(
        f"Branch fault sites        : {len(branch_sites)}"
    )

    print(
        "-" * 72
    )

    print(
        f"Total fault sites         : {len(sites)}"
    )

    print(
        f"Uncollapsed SA faults     : {2 * len(sites)}"
    )


# ============================================================
# Print collapsed classes
# ============================================================

def print_classes(classes):

    sorted_classes = sorted(
        classes.values(),
        key=lambda members: fault_sort_key(
            min(members, key=fault_sort_key)
        )
    )

    print()
    print("=" * 72)
    print("EQUIVALENCE CLASSES")
    print("=" * 72)

    for number, members in enumerate(
        sorted_classes,
        start=1
    ):

        members = sorted(
            members,
            key=fault_sort_key
        )

        text = " = ".join(
            fault.name()
            for fault in members
        )

        print(
            f"{number:4d}: {text}"
        )


# ============================================================
# Write collapsed representatives
# ============================================================

def write_collapsed_faults(
    filename,
    representatives
):

    with open(filename, "w") as f:

        for fault in representatives:

            f.write(
                f"{fault.name()}\n"
            )


# ============================================================
# Write complete equivalence classes
# ============================================================

def write_equivalence_classes(
    filename,
    classes
):

    sorted_classes = sorted(
        classes.values(),
        key=lambda members: fault_sort_key(
            min(members, key=fault_sort_key)
        )
    )

    with open(filename, "w") as f:

        for number, members in enumerate(
            sorted_classes,
            start=1
        ):

            members = sorted(
                members,
                key=fault_sort_key
            )

            f.write(
                f"CLASS {number}\n"
            )

            for fault in members:

                f.write(
                    f"    {fault.name()}\n"
                )

            f.write("\n")


# ============================================================
# Write all uncollapsed faults
# ============================================================

def write_raw_faults(
    filename,
    raw_faults
):

    with open(filename, "w") as f:

        for fault in sorted(
            raw_faults,
            key=fault_sort_key
        ):

            f.write(
                f"{fault.name()}\n"
            )


# ============================================================
# Main
# ============================================================

def main():

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "    python collapse_c880.py c880.bench"
        )

        sys.exit(1)

    filename = sys.argv[1]

    # --------------------------------------------------------
    # Parse circuit
    # --------------------------------------------------------

    inputs, outputs, gates = parse_bench(
        filename
    )

    # --------------------------------------------------------
    # Basic circuit statistics
    # --------------------------------------------------------

    print("=" * 72)
    print("ISCAS-85 c880 FAULT COLLAPSING")
    print("=" * 72)

    print(
        f"Primary inputs             : {len(inputs)}"
    )

    print(
        f"Primary outputs            : {len(outputs)}"
    )

    print(
        f"Gates                      : {len(gates)}"
    )

    # --------------------------------------------------------
    # Fanout
    # --------------------------------------------------------

    fanout = build_fanout(gates)

    # --------------------------------------------------------
    # Fault sites
    # --------------------------------------------------------

    sites = create_fault_sites(
        inputs,
        gates,
        fanout
    )

    print_site_statistics(
        inputs,
        gates,
        fanout,
        sites
    )

    # --------------------------------------------------------
    # Generate raw faults
    # --------------------------------------------------------

    raw_faults = generate_raw_faults(
        sites
    )

    # --------------------------------------------------------
    # Collapse
    # --------------------------------------------------------

    uf, classes = collapse_faults(
        inputs,
        gates,
        fanout,
        raw_faults
    )

    representatives = choose_representatives(
        classes
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    raw_count = len(raw_faults)
    collapsed_count = len(representatives)

    reduction = raw_count - collapsed_count

    reduction_percent = (
        100.0 * reduction / raw_count
    )

    print()
    print("=" * 72)
    print("COLLAPSING RESULTS")
    print("=" * 72)

    print(
        f"Fault sites               : {len(sites)}"
    )

    print(
        f"Uncollapsed faults        : {raw_count}"
    )

    print(
        f"Collapsed faults          : {collapsed_count}"
    )

    print(
        f"Fault reduction           : {reduction}"
    )

    print(
        f"Reduction percentage      : "
        f"{reduction_percent:.2f}%"
    )

    # --------------------------------------------------------
    # Validation against your reference
    # --------------------------------------------------------

    print()
    print("=" * 72)
    print("REFERENCE CHECK")
    print("=" * 72)

    expected_sites = 834
    expected_raw = 1668
    expected_collapsed = 850

    print(
        f"Expected fault sites      : {expected_sites}"
    )

    print(
        f"Actual fault sites        : {len(sites)}"
    )

    print()

    print(
        f"Expected uncollapsed      : {expected_raw}"
    )

    print(
        f"Actual uncollapsed        : {raw_count}"
    )

    print()

    print(
        f"Expected collapsed        : "
        f"{expected_collapsed}"
    )

    print(
        f"Actual collapsed          : "
        f"{collapsed_count}"
    )

    # --------------------------------------------------------
    # Assertions
    # --------------------------------------------------------

    if len(sites) != expected_sites:

        print()
        print(
            "WARNING: fault-site count does not match "
            "the reference value."
        )

        print(
            "The BENCH connectivity or fault-site "
            "convention may differ."
        )

    if raw_count != expected_raw:

        print()
        print(
            "WARNING: uncollapsed fault count does "
            "not match 1668."
        )

    if collapsed_count != expected_collapsed:

        print()
        print(
            "WARNING: collapsed fault count does "
            "not match 850."
        )

    # --------------------------------------------------------
    # Write files
    # --------------------------------------------------------

    write_raw_faults(
        "c880_uncollapsed_faults.txt",
        raw_faults
    )

    write_collapsed_faults(
        "c880_collapsed_faults.txt",
        representatives
    )

    write_equivalence_classes(
        "c880_fault_equivalence_classes.txt",
        classes
    )

    # --------------------------------------------------------
    # Final information
    # --------------------------------------------------------

    print()
    print("=" * 72)
    print("OUTPUT FILES")
    print("=" * 72)

    print(
        "c880_uncollapsed_faults.txt"
    )

    print(
        "c880_collapsed_faults.txt"
    )

    print(
        "c880_fault_equivalence_classes.txt"
    )

    print()

    # --------------------------------------------------------
    # Print collapsed representatives
    # --------------------------------------------------------

    print("=" * 72)
    print("COLLAPSED FAULTS")
    print("=" * 72)

    for i, fault in enumerate(
        representatives,
        start=1
    ):

        print(
            f"{i:4d}: {fault.name()}"
        )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()
