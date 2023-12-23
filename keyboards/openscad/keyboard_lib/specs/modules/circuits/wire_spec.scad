use <../../../lib/circuits/wire.scad>

module wire_test(guage=12){
  difference(){
    union(){
      linear_extrude(0.5)
        projection()
          wire_space_outline(guage);
      color("green")
        linear_extrude(1)
          wire_pcb_outline(guage);
      color("red")
        linear_extrude(1.5)
          wire_pcb_traces(guage);
    }
    translate([0,0,-1])
      linear_extrude(3)
        wire_pcb_drill(guage);
  }

  translate([22,0]) {
    wire_space_outline(guage);
  }
}

wire_test(8);

translate([0,10])
  wire_test(10);

translate([0,20])
  wire_test(12);

translate([0,30])
  wire_test(14);

translate([0,40])
  wire_test(16);