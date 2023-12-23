include <../../../lib/switches/rgb.scad>
include <../../../lib/variables.scad>


module test_rgb(width=1, height=1, connections=["hole", "hole", "hole", "hole"]) {
  difference(){
    color("blue")
      linear_extrude(1)
        rgb_pcb_traces(width=width, height=height, connections=connections);
    translate([0,0,-1])
      linear_extrude(3)
        rgb_pcb_drill(width=width, height=height, connections=connections);
  }
}

test_rgb();
translate([u_mm(1), 0])
  test_rgb(2);
translate([0, u_mm(1)])
  test_rgb(2.75);

translate([0,u_mm(2)]){
  test_rgb(connections=["none", "none", "none", "hole"]);
  translate([u_mm(1), 0])
    test_rgb(2, connections=["none", "none", "none", "hole"]);
  translate([0, u_mm(1)])
    test_rgb(2.75, connections=["none", "none", "none", "hole"]);
}

translate([0,u_mm(4)]){
  test_rgb(connections=["none", "none", "hole", "none"]);
  translate([u_mm(1), 0])
    test_rgb(2, connections=["none", "none", "hole", "none"]);
  translate([0, u_mm(1)])
    test_rgb(2.75, connections=["none", "none", "hole", "none"]);
}

translate([0,u_mm(6)]){
  test_rgb(connections=["none", "none", "none", "none"]);
  translate([u_mm(1), 0])
    test_rgb(2, connections=["none", "none", "none", "none"]);
  translate([0, u_mm(1)])
    test_rgb(2.75, connections=["none", "none", "none", "none"]);
}