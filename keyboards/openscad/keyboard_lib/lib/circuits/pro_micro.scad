use <helpers.scad>

module pro_micro_pcb_drill(connections="holes") {
  translate([bu(0.5),bu(1.5),0]) {
    if(connections == "holes"){
      translate([bu(3),bu(1)])
        breadboard_row(3)
          circle(d=1, $fn=20);
      translate([bu(4),bu(3)])
        breadboard_row(3)
          circle(d=1, $fn=20);
    }
    breadboard_row(12) {
      circle(d=1, $fn=20);
      if(connections == "holes") {
        translate([bu(1),0,0])
          circle(d=1, $fn=20);
        translate([bu(5),0,0])
          circle(d=1, $fn=20);
      }
      translate([bu(6),0,0])
        circle(d=1, $fn=20);
    }
  }
}

module pro_micro_pcb_traces(connections="holes") {
  translate([bu(0.5),bu(1.5),0]) {
    // GRND
    if(connections == "holes"){
      translate([bu(3),bu(1)]){
        translate([-0.75,-1])
          square([1.5,bu(3)-2]);
        breadboard_row(3)
          circle(d=2.4, $fn=20);
        translate([0,-0.75])
          square([bu(2),1.5]);
      }
      translate([bu(4),bu(3)]){
        translate([-0.75,-1])
          square([1.5,bu(3)-2]);
        breadboard_row(3)
          circle(d=2.4, $fn=20);
        translate([0,-0.75])
          square([bu(2),1.5]);
      }
    }
    breadboard_row(12) {
      circle(d=2.4, $fn=20);
      if(connections == "holes") {
        translate([0,-1,0])
          square([bu(1),2]);
        translate([bu(1),0,0])
          circle(d=2.4, $fn=20);
        translate([bu(5),0])  
          circle(d=2.4, $fn=20);
        translate([bu(5),-1,0])
          square([bu(1),2]);
      }
      translate([bu(6),0,0])
        circle(d=2.4, $fn=20);
    }
  }
}

module pro_micro_pcb_outline() {
  translate([0,bu(1)])
  square([bu(7), bu(12)]);
}

module pro_micro_space_outline() {
  translate([0,0,-4]) {
    linear_extrude(6) {
      translate([-bu(0.5),-bu(0.5)])
        square([bu(8), bu(14)]);
    }
    linear_extrude(5) {
      translate([bu(0.5),-bu(15),0])
        square([bu(6),bu(25)]);
    }
  }
}
