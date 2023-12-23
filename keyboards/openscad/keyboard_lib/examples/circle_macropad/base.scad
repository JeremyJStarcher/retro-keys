use <../../keyboard.scad>

layout = [
  [[],[]],
  [[],[]]
];

thickness=10;

module circle_case() {
  translate([u_mm(1),u_mm(1),0])
    circle(d=u_mm(3), $fn=180);
}

module circle_board() { // make stl
  board(layout, depth=5, thickness=thickness)
    circle_case();
}

module circle_board_bottom_case() { // make stl
  bottom_case(layout, plate="board", margin=5, thickness=thickness)
    circle_case();
}

module circle_top_case() { // make stl
  top_case(layout, depth=5, thickness=thickness)
    circle_case();
}

module circle_top_plate() { // make stl
  top_plate(layout)
    circle_case();
}

module circle_top_plate_drawing() { // make svg
  top_plate_drawing(layout)
    circle_case();
}

module circle_bottom_case() { // make stl
  bottom_case(layout, margin=5, thickness=thickness)
    circle_case();
}

module circle_pcb_outline() { // make svg
  pcb_outline(layout)
    circle_case();
}

module circle_pcb_traces() { // make svg
  pcb_traces(layout)
    circle_case();
}

module circle_pcb_drill() { // make svg
  pcb_drill(layout)
    circle_case();
}

// Render parts
color("green")
  circle_top_case();
color("yellow")
  circle_top_plate();
color("purple")
  circle_bottom_case();
difference() {
  union() {
    color("red")
      linear_extrude(0.5)
        circle_pcb_outline();
    translate([0,0,-0.25])
      color("blue")
        linear_extrude(1)
          circle_pcb_traces();
  }
  translate([0,0,-0.5])
    linear_extrude(2)
      circle_pcb_drill();
}
