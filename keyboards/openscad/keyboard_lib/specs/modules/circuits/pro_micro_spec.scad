use <../../../lib/circuits/pro_micro.scad>

module pro_micro_test(holes="holes"){
  difference(){
    union(){
      linear_extrude(0.5)
        projection()
          pro_micro_space_outline();
      color("green")
        linear_extrude(1)
          pro_micro_pcb_outline();
      color("red")
        linear_extrude(1.5)
          pro_micro_pcb_traces(holes);
    }
    translate([0,0,-1])
      linear_extrude(3)
        pro_micro_pcb_drill(holes);
  }
}

pro_micro_test();
translate([25,0])
  pro_micro_space_outline();
translate([50,0])
  pro_micro_test(holes="none");
