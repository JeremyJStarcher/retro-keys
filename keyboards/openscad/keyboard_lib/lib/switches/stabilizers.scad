module stab_hole_render(distance){
  translate([14+distance+3.375,6.99,0]) {
    circle(d=3.175, $fn=40);
    translate([0,-15.24,0])
      circle(d=4.064, $fn=40);
  }
  translate([-6.75-distance+3.375,6.99,0]) {
    circle(d=3.175, $fn=40);
    translate([0,-15.24,0])
      circle(d=4.064, $fn=40);
  }
}

module stab_holes(width) {
  if (width >= 7) {
    stab_hole_render(39.6);
  } else if (width >= 6) {
    stab_hole_render(39.6);
  } else if(width >= 2) {
    stab_hole_render(1.6);
  }
}

module stab_render(distance, cnc=false, height=5.334) {
  translate([14+distance,1.47,0]){
    // Right Side Large Hole
    cube([6.75,12.3,10]);

    // Add 1/16" corner holes for milling
    if(cnc){
      translate([0.56,0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
      translate([6.75-0.56,0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
      translate([0.56,12.3-0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
      translate([6.75-0.56,12.3-0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
    }
    translate([5.75,3.23,0]){
      // Side hole for notch
      cube([1.825,3.175,10]);
      translate([1.825,1.59,0])
        if(cnc)
          resize([1.59,3.175,10])
            cylinder(h=10,d=1.59,$fn=20);
    }
    translate([1.725,11.3,0]){
      // Top Notch
      cube([3.3,2.2,10]);
      if(cnc)
        translate([1.65,2.2,0])
          resize([3.3,1,10])
            cylinder(h=10,d=1,$fn=20);
    }
    // Thin out for clip
    translate([-1,-1,10-height+1.5])
      cube([8.75,14.3,height-1.5]);
  }
  translate([-6.75-distance,1.47,0]){
    // Left Side Large Hole
    cube([6.75,12.3,10]);
    translate([-0.825,3.23,0]){
      // Side hole for notch
      cube([1.825,3.175,10]);
      if(cnc)
        translate([0,1.59,0])
          resize([1.59,3.175,10])
            cylinder(h=10,d=1.59,$fn=20);

    }
    translate([1.725,11.3,0]){
      // Top Notch
      cube([3.3,2.2,10]);
      if(cnc)
        translate([1.65,2.2,0])
          resize([3.3,1,10])
            cylinder(h=10,d=1,$fn=20);
    }
    if(cnc){
      translate([0.56,0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
      translate([6.75-0.56,0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
      translate([0.56,12.3-0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
      translate([6.75-0.56,12.3-0.56,0])
        cylinder(h=10,d=1.59,$fn=20);
    }
    // Thin out for clip
    translate([-1,-1,10-height+1.5])
      cube([8.75,14.3,height-1.5]);
  }
  // Center shaft for bar
  translate([-distance-2,4.7,0]){
    cube([distance*2+20,4.6,10]);
  }
}

module stab(key_width, cnc=false) {
  if (key_width >= 7) {
    stab_render(39.6, cnc=cnc);
  } else if (key_width >= 6) {
    stab_render(39.6, cnc=cnc);
  } else if(key_width >= 2) {
    stab_render(1.6, cnc=cnc);
  }
}
