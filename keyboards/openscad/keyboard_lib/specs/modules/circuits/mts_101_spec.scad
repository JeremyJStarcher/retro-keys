use <../../../lib/circuits/mts_101.scad>

module mts_101_test(){
  difference(){
    union(){
      // linear_extrude(0.5)
      //   projection()
      //     mts_101_space_outline();
      color("green")
        linear_extrude(1)
          mts_101_pcb_outline();
      color("red")
        linear_extrude(1.5)
          mts_101_pcb_traces();
    }
    translate([0,0,-1])
      linear_extrude(3)
        mts_101_pcb_drill();
  }
}

mts_101_test();

translate([22,0]) {
  mts_101_space_outline();
}