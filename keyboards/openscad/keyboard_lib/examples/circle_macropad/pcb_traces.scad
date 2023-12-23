use <../../keyboard.scad>

// layout = [
//   [[],[]],
//   [[],[]]
// ];
layout = [
  [[1,0,0,[],["hole","connect","connect","hole"]],[1,0,0,[],["hole","connect","hole","connect"]]],
  [[1,0,0,[],["connect","hole","connect","hole"]],[1,0,0,[],["connect","hole","hole","connect"]]]
];
pcb_render(layout, single=false);
