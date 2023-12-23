include <../../../lib/switches.scad>

layout = [
  [[2,0,0,[],["hole", "connect", "connect", "hole"]],[1,0,0,[],["hole", "connect", "connect", "connect"]],[1,0,0,[],["hole", "connect", "connect", "connect"]],[1,0,0,[],["hole", "connect", "hole", "connect"]]],
  [[1,0,0,[],["connect", "connect", "connect", "hole"]],[2,0,0,[],["connect", "connect", "connect", "connect"]],[1,0,0,[],["connect", "connect", "connect", "connect"]],[1,0,0,[],["connect", "connect", "hole", "connect"]]],
  [[1,0,0,[],["connect", "hole", "connect", "hole"]],[1,0,0,[],["connect", "hole", "connect", "connect"]],[2,0,0,[],["connect", "hole", "connect", "connect"]],[1,0,0,[],["connect", "hole", "hole", "connect"]]]
];

module test_top() {
  switches(layout, type="traces_top");
}
module test_bottom() {
  switches(layout, type="traces_bottom");
}

difference(){
  union(){
    color("blue")
      linear_extrude(1)
        switches(layout, type="outline");
    color("red")
      translate([0,0,0.75])
        linear_extrude(1)
          switches(layout, type="traces_top");
    color("orange")
      translate([0,0,-0.75])
        linear_extrude(1)
          switches(layout, type="traces_bottom");
  }
  translate([0,0,-1])
    linear_extrude(3)
      switches(layout, type="drill_double");
}
