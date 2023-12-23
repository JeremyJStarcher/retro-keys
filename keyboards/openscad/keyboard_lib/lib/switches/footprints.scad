include <../variables.scad>
include <stabilizers.scad>

module pcb_switch_outline(width=1, height=1) {
  stab_extra = width >= 2 ? 2 : 0;
  translate([0,-stab_extra])
    square([u_mm(width)+0.01, u_mm(height)+0.01+stab_extra]);
}

module pcb_switch_space_outline(width=1, height=1, style="mx", cnc=false) {
  offset = height_for_style(style);
  stab_extra = width >= 2 ? 2 : 0;
  translate([-1,-1-stab_extra,2.834-offset])
    cube([u_mm(width) + 2, u_mm(height) + 2 + stab_extra, 1.166+offset]);
  translate([u_mm(width/2),u_mm(height/2)]) {
    translate([-7.5,-7.5,1.5-offset])
      cube([15,15,5]);
    translate([-7,-7,-10])
      cube([14,14,10]);
    translate([u_mm(-width/2)-0.5,u_mm(-height/2)-0.5,-20-offset])
      cube([u_mm(width)+1,u_mm(height)+1, 20]);
  }
  translate([hole_offset(width), hole_offset(height),-10])
    stab(width);
}
