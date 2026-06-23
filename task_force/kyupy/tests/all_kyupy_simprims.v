module all_kyupy_primitives (i0, i1, i2, i3, o);
    input i0;
    input i1;
    input i2;
    input i3;
    output [32:0] o;

    BUF1 buf1_0 (.i0(i0), .o(o[0]));
    INV1 inv1_0 (.i0(i1), .o(o[1]));

    AND2 and2_0 (.i0(i0), .i1(i1), .o(o[2]));
    AND3 and3_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[3]));
    AND4 and4_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[4]));

    NAND2 nand2_0 (.i0(i0), .i1(i1), .o(o[5]));
    NAND3 nand3_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[6]));
    NAND4 nand4_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[7]));

    OR2 or2_0 (.i0(i0), .i1(i1), .o(o[8]));
    OR3 or3_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[9]));
    OR4 or4_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[10]));

    NOR2 nor2_0 (.i0(i0), .i1(i1), .o(o[11]));
    NOR3 nor3_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[12]));
    NOR4 nor4_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[13]));

    XOR2 xor2_0 (.i0(i0), .i1(i1), .o(o[14]));
    XOR3 xor3_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[15]));
    XOR4 xor4_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[16]));

    XNOR2 xnor2_0 (.i0(i0), .i1(i1), .o(o[17]));
    XNOR3 xnor3_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[18]));
    XNOR4 xnor4_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[19]));

    AO21 ao21_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[20]));
    AO22 ao22_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[21]));
    OA21 oa21_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[22]));
    OA22 oa22_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[23]));

    AOI21 aoi21_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[24]));
    AOI22 aoi22_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[25]));
    OAI21 oai21_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[26]));
    OAI22 oai22_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[27]));

    AO211 ao211_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[28]));
    OA211 oa211_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[29]));

    AOI211 aoi211_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[30]));
    OAI211 oai211_0 (.i0(i0), .i1(i1), .i2(i2), .i3(i3), .o(o[31]));

    MUX21 mux21_0 (.i0(i0), .i1(i1), .i2(i2), .o(o[32]));

endmodule