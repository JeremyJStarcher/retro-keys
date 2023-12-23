use <../../../lib/circuits/trrs.scad>

module trrs_test(side){
difference(){
  union(){
    linear_extrude(0.5)
      projection()
        trrs_space_outline(side);
    color("green")
      linear_extrude(1)
        trrs_pcb_outline(side);
    color("red")
      linear_extrude(1.5)
        trrs_pcb_traces(side);
  }
  translate([0,0,-1])
    linear_extrude(3)
      trrs_pcb_drill(side);
  }
}

trrs_test("right");
translate([20,0])
  trrs_test("left");
translate([40,0])
  trrs_test("none");
translate([60,0])
  trrs_space_outline("right");
translate([80,0])
  trrs_space_outline("left");;
translate([100,0])
  trrs_space_outline("none");
