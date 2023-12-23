use <../variables.scad>
use <../switches/base.scad>

module 1u_centered() {
  translate([u_mm(0.5),u_mm(0.5)])
    children();
}

module ec11_pcb_drill(single=false, connections=["hole","hole","hole","hole"]) {
  switch_base_pcb_drill(rgb=false, connections=connections) {
    // Key Column
    translate([-3,0,0])
      circle(d=1,$fn=40);

    // Key Row
    translate([7,2.5])
      circle(d=1, $fn=20);

    if(single) {
      translate([4.25,-3,0])
        circle(d=1, $fn=20);
      translate([-3,-3.25,0])
        circle(d=1,$fn=40);
    }
    translate([4.25,0,0])
      circle(d=1, $fn=20);

    translate([7,-2.5])
      circle(d=1, $fn=20);

    if(connections[3] == "hole"){
      translate([-5.5,2.5])
        circle(d=1, $fn=20);
      translate([-5.5,0])
        circle(d=1, $fn=20);
      translate([-5.5,-2.5])
        circle(d=1, $fn=20);
    }
    translate([-7.5,-2.5])
      circle(d=1, $fn=20);
    translate([-7.5,2.5])
      circle(d=1, $fn=20);
    translate([-7.5,0])
      circle(d=1, $fn=20);

    translate([-1.3,-6.25])
      square([2.6,1.5]);
    translate([-1.3,4.75])
      square([2.6,1.5]);
  }
}

module ec11_pcb_traces(single=false, connections=["hole","hole","hole","hole"]) {
  switch_base_pcb_traces(single=single, rgb=false, connections=connections) {
    // Key Row
    if(single){
      translate([2,2.2])
        square([4.5,0.8]);
      r_len = connections[0] != "none" ? u_mm(0.5)-1 : 6;
      l_len = connections[1] != "none" ? u_mm(0.5)-1 : 6;
      translate([2,-r_len])
        square([0.8,r_len+l_len]);
      if(connections[0] != "none")
        translate([-2,1-u_mm(0.5)])
          square([4,0.8]);
      if(connections[1] != "none")
        translate([-2.1,u_mm(0.5)-1.6])
          square([4.9,0.8]);
    }
    translate([7,2.5])
      circle(d=2.5,$fn=40);

    // Key Column
    if(connections[3] != "none")
      translate([1-u_mm(0.5),-6])
        square([u_mm(0.5)-4,1]);
    translate([-3.25,-6])
      square([0.8,5]);
    translate([-3,0])
      circle(d=2.5,$fn=40);

    if(single){
      translate([-3,-3.25])
        circle(d=2.5,$fn=40);
      translate([4.25,-3])
        circle(d=2.5,$fn=40);
    } else {
      translate([-3,-3.25])
        square([7.8,0.8]);
    }

    translate([7,-2.5])
      circle(d=2.5,$fn=40);
    translate([4.25,0]) {
      circle(d=2.5,$fn=40);
      rotate(-45)
        square([5,0.8]);
    }

    translate([4,-6])
      square([0.8,3]);
    if(connections[2] != "none")
      translate([4,-6])
        square([4.5,0.8]);

    if(connections[3] == "hole"){
      translate([-5.5,2.5])
        circle(d=2.25, $fn=20);
      translate([-5.5,0])
        circle(d=2.25, $fn=20);
      translate([-5.5,-2.5])
        circle(d=2.25, $fn=20);
    }
    translate([-7.5,-2.5])
      circle(d=2.25, $fn=20);
    translate([-7.5,2.5])
      circle(d=2.25, $fn=20);
    translate([-7.5,0])
      circle(d=2.25, $fn=20);
  }
}

module ec11_pcb_traces_bottom(connections=["hole","hole","hole","hole"]) {
  switch_base_pcb_traces_bottom(rgb=false, connections=connections) {
    // Key Row
    translate([2,2.2])
      square([4.5,0.8]);
    r_len = connections[0] != "none" ? u_mm(0.5)-1 : 6;
    l_len = connections[1] != "none" ? u_mm(0.5)-1 : 6;
    translate([2,-r_len])
      square([0.8,r_len+l_len]);
    
    if(connections[0] != "none")
      translate([-1.3,1-u_mm(0.5)])
        square([4,0.8]);
    if(connections[1] != "none")
      translate([-1,u_mm(0.5)-1.4])
        square([3.8,0.8]);
    translate([7,2.5])
      circle(d=2.5,$fn=40);

    // Key Column
    translate([-3,0])
      circle(d=2.5,$fn=40);

    translate([7,-2.5])
      circle(d=2.5,$fn=40);
    translate([4.25,0]) {
      circle(d=2.5,$fn=40);
    }

    if(connections[3] == "hole"){
      translate([-5.5,2.5])
        circle(d=2.25, $fn=20);
      translate([-5.5,0])
        circle(d=2.25, $fn=20);
      translate([-5.5,-2.5])
        circle(d=2.25, $fn=20);
    }
    translate([-7.5,-2.5])
      circle(d=2.25, $fn=20);
    translate([-7.5,2.5])
      circle(d=2.25, $fn=20);
    translate([-7.5,0])
      circle(d=2.25, $fn=20);
  }
}

module ec11_pcb_outline() {
  square([u_mm(1), u_mm(1)]);
}

module ec11_space_outline() {
  translate([-0.5,-0.5, -6])
    cube([u_mm(1)+1, u_mm(1)+1, 8]);
  1u_centered() {
    translate([0,0,-15])
      linear_extrude(15)
        circle(d=7, $fn=30);
    translate([0,0,-25])
      linear_extrude(15)
        circle(d=19, $fn=80);
  }
}