use <../../keyboard.scad>

layout = [
  [[],[]],
  [[],[]]
];
top_case(layout, depth=6)
  translate([u_mm(1),u_mm(1),0])
    circle(d=u_mm(3));
