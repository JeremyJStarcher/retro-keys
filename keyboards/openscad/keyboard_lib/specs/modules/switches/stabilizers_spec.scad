include <../../../lib/switches/stabilizers.scad>
include <../../../lib/variables.scad>

stab(2);
translate([0,u_mm(1.4)])
  linear_extrude(1)
    stab_holes(2);
translate([0,u_mm(2)])
  stab(6.25);
translate([0,u_mm(3.4)])
  linear_extrude(1)
    stab_holes(6.25);
translate([0,u_mm(4)])
  stab(7);
translate([0,u_mm(5.4)])
  linear_extrude(1)
    stab_holes(7);
