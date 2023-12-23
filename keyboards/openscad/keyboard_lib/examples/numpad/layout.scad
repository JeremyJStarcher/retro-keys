use <../../keyboard.scad>

function layout() = [
  [[],[],[],[]],
  [[],[],[],[2,1,0,[90]]],
  [[],[],[]],
  [[],[],[],[2,1,0,[90]]],
  [[2],[]]
];

module case() {
  translate([0,-u_mm(1.85)])
  square([u_mm(4),u_mm(6.85)]);
}

function circuits() = [
  [1.5,-1.85,0,0,"pro_micro"]
];
