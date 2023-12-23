use <../variables.scad>
module mts_101_pcb_drill() {
  translate([0,1.25]) {
    translate([2.5,0])
      square([3,1]);
    translate([1.25,0.5])
      circle(d=1,$fn=40);
    translate([6.75,0.5])
      circle(d=1,$fn=40);

    translate([2.5,4.75])
      square([3,1]);
    translate([1.25,5.25])
      circle(d=1,$fn=40);
    translate([6.75,5.25])
      circle(d=1,$fn=40);

    translate([4,10])
      circle(d=1,$fn=40);
    translate([1.25,10])
      circle(d=1,$fn=40);
    translate([6.75,10])
      circle(d=1,$fn=40);
  }
}

module mts_101_pcb_traces() {
  translate([0,1.25]) {
    translate([2,-0.5])
      square([4,2]);
    translate([1.25,0.5])
      circle(d=2,$fn=40);
    translate([6.75,0.5])
      circle(d=2,$fn=40);

    translate([2,4.25])
      square([4,2]);
    translate([1.25,5.25])
      circle(d=2,$fn=40);
    translate([6.75,5.25])
      circle(d=2,$fn=40);

    translate([4,10])
      circle(d=2,$fn=40);
    translate([1.25,9.5])
      square([6,1]);
    translate([1.25,10])
      circle(d=2,$fn=40);
    translate([6.75,10])
      circle(d=2,$fn=40);
  }
}

module mts_101_pcb_outline() {
  square([8,13]);
}

module mts_101_space_outline(, cnc=false) {
  translate([-0.5,-0.5,-10])
    cube([9,14, 14.4]);
  translate([4,6.5,-26]) {
    cylinder(d=6, h=18, $fn=30);
    cylinder(d=12, h=10, $fn=60);
  }
}
