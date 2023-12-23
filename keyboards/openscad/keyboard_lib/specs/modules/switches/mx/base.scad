include <../../../../lib/switches/mx.scad>

module run_test(width=1, height=1, rgb=true, single=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"]) {
  difference(){
    union(){
      color("blue")
        linear_extrude(1)
          switch_mx_pcb_outline(width=width, height=height);
      color("red")
        translate([0,0,0.75])
          linear_extrude(1)
            switch_mx_pcb_traces(width=width, height=height, rgb=rgb, single=single, xpos=xpos, ypos=ypos, connections=connections);
      if(!single)
        color("orange")
          translate([0,0,-0.75])
            linear_extrude(1)
              switch_mx_pcb_traces_bottom(width=width, height=height, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections);
    }
    translate([0,0,-1])
      linear_extrude(3)
        switch_mx_pcb_drill(width=width, height=height, rgb=rgb, single=single, connections=connections);
  }
}
