use <../../keyboard.scad>

layout = [
  [[],[]],
  [[],[]]
];
top_plate_drawing(layout)
  translate([u_mm(1),u_mm(1),0])
    circle(d=u_mm(3));
