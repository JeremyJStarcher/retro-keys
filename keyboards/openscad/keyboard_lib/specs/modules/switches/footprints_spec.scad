include <../../../lib/switches/footprints.scad>
include <../../../lib/utilities.scad>

styles = ["mx", "redragon", "choc_v1"];
sizes = [[1,1],[2.25,1],[6.25,1],[1,2]];

module test(styles, sizes) {
  if(len(sizes) > 0) {
    for(style=[0:len(styles)-1]) {
      echo(style, " Style");
      translate([0,u_mm(style*2.5)])
        pcb_switch_space_outline(width=sizes[0][0], height=sizes[0][1], style=styles[style], cnc=false);
    }
    translate([u_mm(sizes[0][0]+1),0])
      test(styles, pop(sizes));
  }
}

test(styles, sizes);
