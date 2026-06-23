from kyupy import bench
from kyupy.techlib import KYUPY
from fsim.static import LineRoles

def test_trivial_inv():
    c = bench.parse('input(i) output(o) o=INV(i)')
    lr = LineRoles(c, KYUPY)
    assert len(lr.line2roles) == 2
    assert len(lr.roles2lines[LineRoles.LOGIC_OUT]) == 2

def test_input_fanout():
    c = bench.parse('input(i) output(o1) output(o2) o1=INV(i) o2=INV(i)')
    lr = LineRoles(c, KYUPY)
    assert len(lr.line2roles) == 4
    assert len(lr.roles2lines[LineRoles.LOGIC_OUT]) == 4

def test_fanout():
    c = bench.parse('input(i) output(o1) output(o2) ii=INV(i) o1=INV(ii) o2=INV(ii)')
    lr = LineRoles(c, KYUPY)
    assert len(lr.line2roles) == 6
    assert len(lr.roles2lines[LineRoles.LOGIC_OUT]) == 6

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
    lr = LineRoles(c, KYUPY)
    assert len(lr.line2roles) == 34  # total number of signal lines in circuit
    # 2 + 9 + 23 = 34
    assert len(lr.roles2lines[LineRoles.LOGIC_OUT]) == 2
    assert len(lr.roles2lines[LineRoles.LOGIC_SEQ]) == 9
    assert len(lr.roles2lines[LineRoles.LOGIC_OUT|LineRoles.LOGIC_SEQ]) == 23
