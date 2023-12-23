use <../../../lib/circuits/trace.scad>

module manual_trace_test(location){
  difference(){
    union(){
      color("blue")
        linear_extrude(1)
          manual_trace_pcb_outline(location);
      color("red")
        translate([0,0,0.75])
          linear_extrude(1)
            manual_trace_pcb_traces(location);
      color("orange")
        translate([0,0,-0.75])
          linear_extrude(1)
            manual_trace_pcb_traces_bottom(location);
    }
    translate([0,0,-1])
      linear_extrude(3)
        manual_trace_pcb_drill(location);
  }
}

manual_trace_test([0,0,0,0,"",[[-10,0],[-20,0],[-10,-20],[0,-10],[0,0],[0,10],[10,20],[20,0],[10,0],[10,-10],[5,-20]],"both","holes"]);

translate([30,0])
  manual_trace_test([0,0,0,0,"",[[0,0],[0,20]],"top","hole_end"]);
translate([40,0])
  manual_trace_test([0,0,0,0,"",[[0,0],[0,20]],"bottom","hole_begin"]);
translate([50,0])
  manual_trace_test([0,0,0,0,"",[[0,0],[0,20]],"both","none"]);
