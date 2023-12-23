include <../../../../lib/switches/choc_v1.scad>

module run_test(width=1, height=1) {
  difference(){
    union(){
      color("blue")
        linear_extrude(1)
          switch_choc_v1_pcb_outline(width=width, height=height);
      color("red")
        translate([0,0,0.75])
          linear_extrude(1)
            switch_choc_v1_pcb_traces(width=width, height=height);
    }
    translate([0,0,-4])
      linear_extrude(8)
        switch_choc_v1_pcb_drill(width=width, height=height);
  }
}
