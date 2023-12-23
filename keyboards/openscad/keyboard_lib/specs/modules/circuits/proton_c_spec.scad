use <../../../lib/circuits/proton_c.scad>

module proton_c_test(size){
  difference(){
    union(){
      linear_extrude(0.5)
        projection()
          proton_c_space_outline(size);
      color("green")
        linear_extrude(1)
          proton_c_pcb_outline(size);
      color("red")
        linear_extrude(1.5)
          proton_c_pcb_traces(size);
    }
    translate([0,0,-1])
      linear_extrude(3)
        proton_c_pcb_drill(size);
  }
}

proton_c_test("full");
translate([-22,0])
  proton_c_space_outline("full");
translate([22,0])
  proton_c_test("short");
translate([44,0])
  proton_c_space_outline("short");
