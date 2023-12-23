module trrs_post(d=1.2) {
  translate([0,-d/4,0]) {
    circle(d=d, $fn=20);
    translate([-d/2,0,0]) {
      square([d,(d/2-.2)]);
    }
    translate([0,(d/2-.2),0]) {
      circle(d=d, $fn=20);
    }
  }
}

module trrs_pcb_drill(side="left") {
  translate([2.8,1.5]) {
    circle(d=2, $fn=20);
  }
  translate([2.8,8.5]) {
    circle(d=2, $fn=20);
  }
  translate([0.5,11.3,0]) {
    trrs_post();
  }
  translate([5.1,3.2,0]) {
    trrs_post();
  }
  translate([5.1,6.2,0]) {
    trrs_post();
  }
  translate([5.1,10.2,0]) {
    trrs_post();
  }
  if(side != "none"){
    offset = side == "left" ? 7.6 : -2;
    translate([offset,11.3]) {
      circle(d=1.2, $fn=20);
    }
    translate([offset,8.3]) {
      circle(d=1.2, $fn=20);
    }
    translate([offset,5.3]) {
      circle(d=1.2, $fn=20);
    }
    translate([offset,2.2]) {
      circle(d=1.2, $fn=20);
    }
  }
}

module trrs_pcb_traces(side="left") {
  translate([-1,9.7,0]){
    difference() {
      square([3,3]);
      if(side == "right") {
        translate([3,-1.8]) {
          rotate(45) {
            square(2);
          }
        }
      }
    }
  }
  translate([3.6,1.2,0]){
    difference() {
      square([3,3.5]);
      if(side == "left") {
        translate([3,2.3]) {
          rotate(45) {
            square(2);
          }
        }
      }
    }
  }
  translate([3.6,4.8,0]){
    difference() {
        square([3,3.5]);
        if(side == "left") {
          translate([3,2.3]) {
            rotate(45) {
              square(2);
            }
          }
        }
    }
  }
  translate([3.6,8.4,0]){
    difference() {
      square([3,3.2]);
      if(side == "left") {
        translate([3,1.8]) {
          rotate(45) {
            square(2);
          }
        }
      }
    }
  }
  if(side != "none"){
    translate([side == "left" ? 7.6 : -2,0,0]){
      translate([0,11.3]) {
        circle(d=3, $fn=20);
      }
      translate([0,8.3]) {
        circle(d=2.9, $fn=20);
      }
      translate([0,5.3]) {
        circle(d=3, $fn=20);
      }
      translate([0,2.2]) {
        circle(d=3, $fn=20);
      }
    }
    translate([side == "left" ? 5.6 : -2,0,0]){
      left_trace = side == "left" ? 2.5 : 7.6;
      translate([0,2.2]) {
        square([left_trace,1.5]);
      }
      translate([0,5.1]) {
        square([left_trace,1.5]);
      }
      if(side == "left") {
        translate([0,8.7]) {
          square([left_trace,0.9]);
        }
      }
      else {
        translate([0,8]) {
          square([4,1.6]);
        }
        translate([4,9]) {
          square([4,1.6]);
        }
        translate([2.8,9.4]) {
          rotate(-45) {
            square([1,1.7]);
          }
        }
      }
    }
    translate([side == "left" ? 0.5 : -2,0,0]){
      right_trace = side == "left" ? 7.1 : 2;
      translate([0,11.7]) {
        square([right_trace,1.3]);
      }
      translate([0,12]) {
        circle(1, $fn=20);
      }
      translate([right_trace,11.8]) {
        circle(1, $fn=20);
      }
    }
  }
}

module trrs_pcb_outline(side="left") {
  translate([-1,0,0]) {
    square([7.6,13.1]);
  }
  if(side != "none"){
    translate([side == "left" ? 5.6 : -3.5, 0]) {
      square([4,13.1]);
    }
  }
}

module trrs_space_outline(side="left") {
  translate([0,0,-5.3]) {
    linear_extrude(7){
      translate([-2,-1,0])
        square([9.6,15.1]);
      translate([0,-12.1,0])
        square([5.6,12.1]);
      if(side != "none")
        translate([side == "left" ? 5.6 : -4.5, -1])
          square([5,15.1]);
    }
  }
  translate([3,-2,-2.6]) {
    rotate([90,0,0]) {
      cylinder(d=10, h=30, $fn=100);
    }
  }
}
