from kyupy import bench
from kyupy.techlib import KYUPY
from fsim.static import FaultSet

def test_trivial_inv():
    c = bench.parse('input(i) output(o) o=INV(i)')
    fs = FaultSet(c, KYUPY)
    assert len(fs.saf_set) == 4
    assert len(fs.saf_equiv_classes) == 2
    oline = c.forks['o'].ins[0]
    iline = oline.driver.ins[0]
    assert fs.fault_str(oline.index*2) == 'o/o@0'
    assert fs.fault_str(oline.index*2+1) == 'o/o@1'
    assert fs.fault_str(iline.index*2) == 'o/i0@0'
    assert fs.fault_str(iline.index*2+1) == 'o/i0@1'
    assert oline.index*2 in fs.saf_equiv_classes
    assert iline.index*2+1 in fs.saf_equiv_classes[oline.index*2]
    assert oline.index*2+1 in fs.saf_equiv_classes
    assert iline.index*2 in fs.saf_equiv_classes[oline.index*2+1]

def test_and():
    c = bench.parse('input(i0, i1) output(o) o=AND(i0, i1)')
    for n in c.nodes:
        print(n)
    fs = FaultSet(c, KYUPY)
    assert len(fs.saf_set) == 6
    assert len(fs.saf_equiv_classes) == 4
    oline = c.forks['o'].ins[0]
    i0line = oline.driver.ins[0]
    i1line = oline.driver.ins[0]
    assert oline.index*2 in fs.saf_equiv_classes
    assert i0line.index*2 not in fs.saf_equiv_classes
    assert i1line.index*2 not in fs.saf_equiv_classes
    assert oline.index*2+1 in fs.saf_equiv_classes
    assert len(fs.saf_equiv_classes[oline.index*2]) == 3
    assert len(fs.saf_equiv_classes[oline.index*2+1]) == 1


def _class_sizes(src):
    """Returns (#equiv class of output s-a-0, #equiv class of output s-a-1)."""
    c = bench.parse(src)
    fs = FaultSet(c, KYUPY)
    oline = c.forks['o'].ins[0]
    return (len(fs.saf_equiv_classes.get(oline.index*2, set())),
            len(fs.saf_equiv_classes.get(oline.index*2+1, set())))


def test_nand():
    # out s-a-1 collapses with both inputs s-a-0; out s-a-0 has no equivalent.
    assert _class_sizes('input(i0,i1) output(o) o=NAND2(i0,i1)') == (1, 3)


def test_or():
    # out s-a-1 collapses with all inputs s-a-1; out s-a-0 has no equivalent.
    assert _class_sizes('input(i0,i1) output(o) o=OR2(i0,i1)') == (1, 3)
    assert _class_sizes('input(i0,i1,i2,i3) output(o) o=OR4(i0,i1,i2,i3)') == (1, 5)


def test_nor():
    # out s-a-0 collapses with all inputs s-a-1; out s-a-1 has no equivalent.
    assert _class_sizes('input(i0,i1) output(o) o=NOR2(i0,i1)') == (3, 1)


def test_aoi_oai_complex():
    # Only the "single" term of the and-or/or-and cells forces the output.
    assert _class_sizes('input(i0,i1,i2) output(o) o=AO21(i0,i1,i2)') == (1, 2)
    assert _class_sizes('input(i0,i1,i2) output(o) o=AOI21(i0,i1,i2)') == (2, 1)
    assert _class_sizes('input(i0,i1,i2) output(o) o=OA21(i0,i1,i2)') == (2, 1)
    assert _class_sizes('input(i0,i1,i2) output(o) o=OAI21(i0,i1,i2)') == (1, 2)
    assert _class_sizes('input(i0,i1,i2,i3) output(o) o=AO211(i0,i1,i2,i3)') == (1, 3)
    assert _class_sizes('input(i0,i1,i2,i3) output(o) o=OAI211(i0,i1,i2,i3)') == (1, 3)
    # The two-term variants do not collapse onto any single input.
    assert _class_sizes('input(i0,i1,i2,i3) output(o) o=AO22(i0,i1,i2,i3)') == (1, 1)

def test_s27():
    # bench parser does not add any clock or set/reset logic.
    c = bench.parse('''
        # 1 outputs
        # 3 D-type flipflops
        # 2 inverters
        # 8 gates (1 ANDs + 1 NANDs + 2 ORs + 4 NORs)

        INPUT(G0)
        INPUT(G1)
        INPUT(G2)
        INPUT(G3)

        OUTPUT(G17)

        G5 = DFF(G10)
        G6 = DFF(G11)
        G7 = DFF(G13)

        G14 = NOT(G0)
        G17 = NOT(G11)

        G8 = AND(G14, G6)

        G15 = OR(G12, G8)
        G16 = OR(G3, G8)

        G9 = NAND(G16, G15)

        G10 = NOR(G14, G11)
        G11 = NOR(G5, G9)
        G12 = NOR(G1, G7)
        G13 = NOR(G2, G12)
    ''')
    fs = FaultSet(c, KYUPY)
    assert len(fs.saf_set) == 52
    assert len(fs.saf_equiv_classes) == 32
    g11_line = c.cells['G11'].outs[0]
    g11_sa_0 = g11_line.index*2
    assert g11_sa_0 in fs.saf_equiv_classes
    assert len(fs.saf_equiv_classes[g11_sa_0]) == 5  # collapse via G9
    g15_line = c.cells['G15'].outs[0]
    g15_sa_0 = g15_line.index*2
    assert g15_sa_0 in fs.saf_equiv_classes[g11_sa_0]

