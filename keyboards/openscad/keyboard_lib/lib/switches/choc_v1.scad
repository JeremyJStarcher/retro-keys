include <../variables.scad>
include <stabilizers.scad>
include <footprints.scad>

module switch_choc_v1_pcb_drill(width=1, height=1) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  translate([half_width,half_height,0]) {
    circle(d=3.5, $fn=30);

    translate([-5.5,0])
      circle(d=2, $fn=30);
    translate([3,3.8])
      circle(d=1, $fn=30);
    translate([-4, 3.8])
      circle(d=1, $fn=30);
    translate([-4,1.25-half_height])
      circle(d=1, $fn=30);
    translate([-4, half_height-3])
      circle(d=1, $fn=30);

    translate([5.5,0])
      circle(d=2, $fn=30);
    translate([0,5.9])
      circle(d=1.3, $fn=30);
    translate([5,3.8])
      circle(d=1.3, $fn=30);
    translate([1-half_width, half_height-1])
      circle(d=1, $fn=30);
    translate([half_width-1, half_height-1])
      circle(d=1, $fn=30);
  }
}

module switch_choc_v1_pcb_traces(width=1, height=1) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  translate([half_width,half_height,0]) {
    translate([5,3.8])
      circle(d=2.8, $fn=30);
    translate([3,3.8])
      circle(d=2.5, $fn=30);
    translate([-4, 3.8])
      circle(d=2.5, $fn=30);
    translate([-4.5, 2-half_height])
      square([1, u_mm(height)-4]);
    translate([-4,1.25-half_height])
      circle(d=2.5, $fn=30);
    translate([-4, half_height-3])
      circle(d=2.5, $fn=30);

    translate([0,5.9])
      circle(d=2.8, $fn=30);
    translate([-0.5, 5.9])
      square([1, half_height-6.9]);
    translate([1-half_width, half_height-1.5])
      square([half_width*2-2, 1]);
    translate([1-half_width, half_height-1])
      circle(d=2.5, $fn=30);
    translate([half_width-1, half_height-1])
      circle(d=2.5, $fn=30);
  }
}

module switch_choc_v1_pcb_outline(width=1, height=1) {
  pcb_switch_outline(width=width, height=height);
}
