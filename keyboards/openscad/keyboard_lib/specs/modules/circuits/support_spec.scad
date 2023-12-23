use <../../../lib/circuits/support.scad>

module support_test(mm=3){
  difference(){
    union(){
      linear_extrude(0.5)
        projection()
          support_space_outline(mm);
      color("green")
        linear_extrude(1)
          support_pcb_outline(mm);
      color("red")
        linear_extrude(1.5)
          support_pcb_traces(mm);
    }
    translate([0,0,-1])
      linear_extrude(3)
        support_pcb_drill(mm);
  }

  translate([22,0]) {
    support_space_outline(mm);
  }
}

support_test(3);

translate([0,10])
  support_test(4);

translate([0,20])
  support_test(6);
