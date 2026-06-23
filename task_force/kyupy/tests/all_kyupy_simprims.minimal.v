// Benchmark "all_kyupy_primitives" written by ABC on Thu Nov  6 13:13:21 2025

module all_kyupy_primitives ( 
    i0, i1, i2, i3,
    \o[0] , \o[1] , \o[2] , \o[3] , \o[4] , \o[5] , \o[6] , \o[7] , \o[8] ,
    \o[9] , \o[10] , \o[11] , \o[12] , \o[13] , \o[14] , \o[15] , \o[16] ,
    \o[17] , \o[18] , \o[19] , \o[20] , \o[21] , \o[22] , \o[23] , \o[24] ,
    \o[25] , \o[26] , \o[27] , \o[28] , \o[29] , \o[30] , \o[31] , \o[32]   );
  input  i0, i1, i2, i3;
  output \o[0] , \o[1] , \o[2] , \o[3] , \o[4] , \o[5] , \o[6] , \o[7] ,
    \o[8] , \o[9] , \o[10] , \o[11] , \o[12] , \o[13] , \o[14] , \o[15] ,
    \o[16] , \o[17] , \o[18] , \o[19] , \o[20] , \o[21] , \o[22] , \o[23] ,
    \o[24] , \o[25] , \o[26] , \o[27] , \o[28] , \o[29] , \o[30] , \o[31] ,
    \o[32] ;
  wire new_n45, new_n48, new_n51, new_n54, new_n55, new_n56, new_n57,
    new_n60, new_n61, new_n62, new_n63, new_n64, new_n65, new_n66, new_n67,
    new_n68, new_n69, new_n72, new_n73, new_n74, new_n75, new_n76, new_n77,
    new_n78, new_n79, new_n80, new_n81, new_n86, new_n87, new_n91, new_n92,
    new_n96, new_n99, new_n102, new_n103, new_n104;
  INV1 g00(.i0(i1), .o(\o[1] ));
  AND2 g01(.i0(i1), .i1(i0), .o(\o[2] ));
  AND2 g02(.i0(\o[2] ), .i1(i2), .o(\o[3] ));
  AND2 g03(.i0(\o[3] ), .i1(i3), .o(\o[4] ));
  INV1 g04(.i0(\o[2] ), .o(\o[5] ));
  INV1 g05(.i0(\o[3] ), .o(\o[6] ));
  INV1 g06(.i0(\o[4] ), .o(\o[7] ));
  INV1 g07(.i0(i0), .o(new_n45));
  AND2 g08(.i0(\o[1] ), .i1(new_n45), .o(\o[11] ));
  INV1 g09(.i0(\o[11] ), .o(\o[8] ));
  INV1 g10(.i0(i2), .o(new_n48));
  AND2 g11(.i0(\o[11] ), .i1(new_n48), .o(\o[12] ));
  INV1 g12(.i0(\o[12] ), .o(\o[9] ));
  INV1 g13(.i0(i3), .o(new_n51));
  AND2 g14(.i0(\o[12] ), .i1(new_n51), .o(\o[13] ));
  INV1 g15(.i0(\o[13] ), .o(\o[10] ));
  AND2 g16(.i0(\o[1] ), .i1(i0), .o(new_n54));
  INV1 g17(.i0(new_n54), .o(new_n55));
  AND2 g18(.i0(i1), .i1(new_n45), .o(new_n56));
  INV1 g19(.i0(new_n56), .o(new_n57));
  AND2 g20(.i0(new_n57), .i1(new_n55), .o(\o[17] ));
  INV1 g21(.i0(\o[17] ), .o(\o[14] ));
  AND2 g22(.i0(i2), .i1(i1), .o(new_n60));
  INV1 g23(.i0(new_n60), .o(new_n61));
  AND2 g24(.i0(new_n48), .i1(\o[1] ), .o(new_n62));
  INV1 g25(.i0(new_n62), .o(new_n63));
  AND2 g26(.i0(new_n63), .i1(new_n61), .o(new_n64));
  INV1 g27(.i0(new_n64), .o(new_n65));
  AND2 g28(.i0(new_n65), .i1(i0), .o(new_n66));
  INV1 g29(.i0(new_n66), .o(new_n67));
  AND2 g30(.i0(new_n64), .i1(new_n45), .o(new_n68));
  INV1 g31(.i0(new_n68), .o(new_n69));
  AND2 g32(.i0(new_n69), .i1(new_n67), .o(\o[18] ));
  INV1 g33(.i0(\o[18] ), .o(\o[15] ));
  AND2 g34(.i0(i3), .i1(new_n48), .o(new_n72));
  INV1 g35(.i0(new_n72), .o(new_n73));
  AND2 g36(.i0(new_n51), .i1(i2), .o(new_n74));
  INV1 g37(.i0(new_n74), .o(new_n75));
  AND2 g38(.i0(new_n75), .i1(new_n73), .o(new_n76));
  INV1 g39(.i0(new_n76), .o(new_n77));
  AND2 g40(.i0(new_n77), .i1(\o[17] ), .o(new_n78));
  INV1 g41(.i0(new_n78), .o(new_n79));
  AND2 g42(.i0(new_n76), .i1(\o[14] ), .o(new_n80));
  INV1 g43(.i0(new_n80), .o(new_n81));
  AND2 g44(.i0(new_n81), .i1(new_n79), .o(\o[19] ));
  INV1 g45(.i0(\o[19] ), .o(\o[16] ));
  AND2 g46(.i0(\o[5] ), .i1(new_n48), .o(\o[24] ));
  INV1 g47(.i0(\o[24] ), .o(\o[20] ));
  AND2 g48(.i0(i3), .i1(i2), .o(new_n86));
  INV1 g49(.i0(new_n86), .o(new_n87));
  AND2 g50(.i0(new_n87), .i1(\o[5] ), .o(\o[25] ));
  INV1 g51(.i0(\o[25] ), .o(\o[21] ));
  AND2 g52(.i0(\o[8] ), .i1(i2), .o(\o[22] ));
  AND2 g53(.i0(new_n51), .i1(new_n48), .o(new_n91));
  INV1 g54(.i0(new_n91), .o(new_n92));
  AND2 g55(.i0(new_n92), .i1(\o[8] ), .o(\o[23] ));
  INV1 g56(.i0(\o[22] ), .o(\o[26] ));
  INV1 g57(.i0(\o[23] ), .o(\o[27] ));
  AND2 g58(.i0(\o[5] ), .i1(new_n51), .o(new_n96));
  AND2 g59(.i0(new_n96), .i1(new_n48), .o(\o[30] ));
  INV1 g60(.i0(\o[30] ), .o(\o[28] ));
  AND2 g61(.i0(\o[8] ), .i1(i3), .o(new_n99));
  AND2 g62(.i0(new_n99), .i1(i2), .o(\o[29] ));
  INV1 g63(.i0(\o[29] ), .o(\o[31] ));
  AND2 g64(.i0(new_n48), .i1(i0), .o(new_n102));
  INV1 g65(.i0(new_n102), .o(new_n103));
  AND2 g66(.i0(new_n103), .i1(new_n61), .o(new_n104));
  INV1 g67(.i0(new_n104), .o(\o[32] ));
  BUF1 g68(.i0(i0), .o(\o[0] ));
endmodule


