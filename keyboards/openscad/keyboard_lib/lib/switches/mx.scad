include <../variables.scad>
include <stabilizers.scad>
include <footprints.scad>
include <base.scad>
include <rgb.scad>

module switch_mx_pcb_drill(width=1, height=1, rgb=true, single=true, connections=["hole","hole","hole","hole"]) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  translate([hole_offset(width), half_height]) {
    stab_holes(width);
  }

  switch_base_pcb_drill(width=width, height=height, single=single, rgb=rgb, connections=connections) {
    circle(d=4,$fn=40);
    translate([-3.8,-2.5,0])
      circle(d=1.7,$fn=40);
    translate([2.5,-5,0])
      circle(d=1.7,$fn=40);
    translate([5,0,0])
      circle(d=1.75,$fn=40);
    translate([-5,0,0])
      circle(d=1.75,$fn=40);

    // Column
    translate([-1.2,-3,0])
      circle(d=1,$fn=40);
    translate([5,-2,0])
      circle(d=1,$fn=40);
    if(single){
      translate([6,-3.7,0])
        circle(d=1,$fn=40);
      if(rgb) {
        translate([5,1.7,0])
          circle(d=1,$fn=40);
      } else {
        translate([6,-8.3,0])
          circle(d=1,$fn=40);
      }
    }
  }
}

module switch_mx_pcb_traces(width=1, height=1, rgb=true, single=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"], last_xpos=0, last_ypos=0) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  switch_base_pcb_traces(width=width, height=height, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections, last_xpos=last_xpos, last_ypos=last_ypos, single=single) {
    translate([-3.8,-2.5,0])
      circle(d=4,$fn=40);
    translate([2.5,-5,0])
      circle(d=4,$fn=40);

    // Row
    v_left = connections[3] == "none" ? 1 : half_width;
    v_right = connections[2] == "none" ? 1 : half_width-5;
    translate([1-v_left,-5.9,0])
      square([v_left+v_right+3,0.8]);

    // Column
    translate([-1.2,-3,0])
      circle(d=2.5,$fn=40);
    translate([5,-2,0])
      circle(d=2.5,$fn=40);
    if(single){
      translate([6,-3.7,0])
        circle(d=2.5,$fn=40);
      difference() {
        translate([5,0,0])
          circle(d=3.55,$fn=40);
        translate([5,-2,0])
          square(4);
      }
      if(rgb) {
        translate([5,1.7,0])
          circle(d=2.3,$fn=40);
      } else {
        translate([4.2,1])
          square([0.8, half_height-2]);
        translate([-1,half_height-1.5])
          square([6,0.8]);
        translate([6,-8.3,0])
          circle(d=2.5,$fn=40);
        translate([-1.3,-8.7,0])
          square([7,0.8]);
      }
    }
  }
}

module switch_mx_pcb_traces_bottom(width=1, height=1, rgb=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"], last_xpos=0, last_ypos=0) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  switch_base_pcb_traces_bottom(width=width, height=height, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections, last_xpos=last_xpos, last_ypos=last_ypos) {
    translate([-3.8,-2.5,0])
      circle(d=4,$fn=40);
    translate([2.5,-5,0])
      circle(d=4,$fn=40);

    // Column
    translate([-1.2,-3,0])
      circle(d=2.5,$fn=40);
    translate([5,-2,0])
      circle(d=2.5,$fn=40);
    difference(){
      translate([2.5,-5,0])
        circle(d=5.9,$fn=40);
      translate([2.5,-5,0])
        circle(d=4.1,$fn=40);
      translate([0.3,-7,0])
        rotate(45)
          square(6);
    }
    translate([3.85,-3.45])
      square([0.8, 1]);

    t_height = connections[0] == "none" ? 1 : half_height-7.8;
    echo("h", 2-half_height, t_height);
    translate([-1.3,-t_height-6.8])
      square([0.8, t_height]);
    translate([-1.3,-7.2])
      square([2.2,0.8]);
    difference() {
      translate([5,0,0])
        circle(d=3.35,$fn=40);
      translate([5,-2,0])
        square(4);
    }
    b_height = connections[1] == "none" ? 2 : half_height-2;
    translate([4.2,1])
      square([0.8, b_height]);
    if(connections[1] != "none")
      translate([-1,half_height-1.5])
        square([6,0.8]);
  }
}

module switch_mx_pcb_outline(width=1, height=1) {
  pcb_switch_outline(width=width, height=height);
}
