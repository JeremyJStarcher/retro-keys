function circuit() = [[8,0,0,0,"pro_micro"],[9.1,0,0,0,"trrs_right"],[4,1,0,0,"manual_trace", [[0,0],[0,10],[10,10]]]];

function layout() = [
  [[6.26], [1,1,1,[20,1,2]]],
  [[2.25],[1.75],[1.25],[]]
];

include <../../../keyboard.scad>

linear_extrude(1)
  pcb_outline(layout=layout(), bit=0.2, circuits=circuit());
