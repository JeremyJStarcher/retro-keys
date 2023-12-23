use <base.scad>

difference(){
  union(){
    color("blue")
      linear_extrude(0.5)
        pcb_outline(layout=layout(), circuits=circuit())
          the_case();
    color("red")
      linear_extrude(1)
        pcb_traces(layout=layout(), circuits=circuit(), rgb=false);
  }
  translate([0,0,-1])
    linear_extrude(3)
      pcb_drill(layout=layout(), circuits=circuit());
}
