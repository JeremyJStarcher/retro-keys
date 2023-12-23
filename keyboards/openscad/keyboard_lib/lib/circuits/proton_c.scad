use <helpers.scad>

module proton_c_pcb_drill(size="full") {
  translate([bu(0.5),bu(1.5),0]) {
    translate([0,bu(1)])
      breadboard_row(4, "horizontal"){
        circle(d=1, $fn=20);
        translate([0,bu(1)])
          circle(d=1, $fn=20);
      }
    translate([bu(4),bu(1)])
      breadboard_row(2)
        circle(d=1, $fn=20);
    translate([bu(4),bu(3)])
      breadboard_row(2)
        circle(d=1, $fn=20);
    circle(d=1, $fn=20);
    translate([bu(1),0,0])
      circle(d=1, $fn=20);
    translate([bu(5),0,0])
      circle(d=1, $fn=20);
    translate([bu(6),0,0])
      circle(d=1, $fn=20);
    breadboard_row(12) {
      circle(d=1, $fn=20);
      translate([bu(1),0,0])
        circle(d=1, $fn=20);
      translate([bu(5),0,0])
        circle(d=1, $fn=20);
      translate([bu(6),0,0])
        circle(d=1, $fn=20);
    }
    if(size == "full")
      translate([0,bu(13)])
        breadboard_row(6) {
          circle(d=1, $fn=20);
          translate([bu(1),0,0])
            circle(d=1, $fn=20);
          translate([bu(5),0,0])
            circle(d=1, $fn=20);
          translate([bu(6),0,0])
            circle(d=1, $fn=20);
    }
  }
}

module proton_c_pcb_traces(size="full") {
  translate([bu(0.5),bu(1.5),0]) {
    translate([0,bu(1)])
      breadboard_row(4, "horizontal"){
        circle(d=2.4, $fn=20);
        translate([-1,0])
          square([2,bu(1)]);
        translate([0,bu(1)])
          circle(d=2.4, $fn=20);
      }
    translate([0,bu(1)])
      breadboard_row(2) {
        translate([bu(5),0])
          circle(d=2.4, $fn=20);
        translate([bu(5),-1,0])
          square([bu(1),2]);
        translate([bu(6),0,0])
          circle(d=2.4, $fn=20);
      }
    translate([bu(4),bu(1)]){
      translate([-0.75,-1])
        square([1.5,bu(2)-2]);
      breadboard_row(2)
        circle(d=2.4, $fn=20);
      translate([0,-0.75])
        square([bu(2),1.5]);
    }
    translate([bu(4),bu(3)]){
      translate([-0.75,-1])
        square([1.5,bu(2)-2]);
      breadboard_row(2)
        circle(d=2.4, $fn=20);
      translate([0,-0.75])
        square([bu(2),1.5]);
    }
    circle(d=2.4, $fn=20);
    translate([0,-1,0])
      square([bu(1),2]);
    translate([bu(1),0,0])
      circle(d=2.4, $fn=20);
    translate([bu(5),0])
      circle(d=2.4, $fn=20);
    translate([bu(5),-1,0])
      square([bu(1),2]);
    translate([bu(6),0,0])
      circle(d=2.4, $fn=20);
    translate([0,bu(3)])
      breadboard_row(9) {
        circle(d=2.4, $fn=20);
        translate([0,-1,0])
          square([bu(1),2]);
        translate([bu(1),0,0])
          circle(d=2.4, $fn=20);
        translate([bu(5),0])
          circle(d=2.4, $fn=20);
        translate([bu(5),-1,0])
          square([bu(1),2]);
        translate([bu(6),0,0])
          circle(d=2.4, $fn=20);
      }
    if(size == "full")
      translate([0,bu(13)])
        breadboard_row(6) {
          circle(d=2.4, $fn=20);
          translate([0,-1,0])
            square([bu(1),2]);
          translate([bu(1),0,0])
            circle(d=2.4, $fn=20);
          translate([bu(5),0])
            circle(d=2.4, $fn=20);
          translate([bu(5),-1,0])
            square([bu(1),2]);
          translate([bu(6),0,0])
            circle(d=2.4, $fn=20);
        }
  }
}

module proton_c_pcb_outline(size="full") {
  translate([0,bu(1)])
  square([bu(7), bu(size == "full" ? 19 : 12)]);
}

module proton_c_space_outline(size="full") {
  translate([0,0,-4]) {
    linear_extrude(6) {
      translate([-bu(0.5),-bu(0.5)])
        square([bu(8), bu(size == "full" ? 21 : 14)]);
    }
    linear_extrude(5) {
      translate([bu(0.5),-bu(15),0])
        square([bu(6),bu(25)]);
    }
  }
}
