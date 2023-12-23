include <../../../lib/switches.scad>

module test_pcbs(layout) {
  difference(){
    union(){
      linear_extrude(0.5)
        switches(layout, type="pcb_switch_space_outline");
      color("blue")
        linear_extrude(1)
          switches(layout, type="pcb_switch_outline");
      color("red")
        linear_extrude(1.5)
          switches(layout, type="switch_mx_pcb_traces");
    }
    translate([0,0,-1])
      linear_extrude(3)
        switches(layout, type="switch_mx_pcb_drill");
  }
}

module test_basic_2_keys_2_switches() {
  layout = [[[],[]],[[],[]]];
  switches(layout);
  translate([u_mm(3),0])
    test_pcbs(layout);
}

module test_spaced_layout() {
  layout = [
    [[],[1,0.25,0.25],[1,0.25,-0.25]],
    [[1,0.25,0.25],[],[]],
    [[1,0,0.5],[1,0.25,-0.25],[1,0.25,0.25]]
  ];
  switches(layout);
  translate([u_mm(4),0])
    test_pcbs(layout);
}

module test_multi_u_layout() {
  layout = [
    [[6.25]],
    [[2.25], [], [1,0.75], [1.25]]
  ];
  switches(layout);
  translate([u_mm(7),0])
    test_pcbs(layout);
}

module test_empty() {
  switches([]);
}

test_empty();

test_basic_2_keys_2_switches();

translate([0,u_mm(3)])
  test_spaced_layout();

translate([0,u_mm(7)])
  test_multi_u_layout();
