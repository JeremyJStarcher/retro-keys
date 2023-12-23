include <../variables.scad>

module rgb_row_trace_connection(width, height, xpos, ypos, rgb, connections) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  if(connections[3] == "connect") {
    translate([1-half_width,8.875,0]){
      circle(d=0.8,$fn=40);
      offset(0.4)
        polygon(points=[[0,-0.01],[0,0.01],[u_mm(-xpos)-2, u_mm(-ypos)+0.01],[u_mm(-xpos)-2, u_mm(-ypos)-0.01]]);
    }
    translate([1-half_width,4.9,0]){
      circle(d=0.8,$fn=40);
      offset(0.4)
        polygon(points=[[0,-0.01],[0,0.01],[u_mm(-xpos)-2, u_mm(-ypos)+0.01],[u_mm(-xpos)-2, u_mm(-ypos)-0.01]]);
    }
    translate([1-half_width,3.3,0]){
      circle(d=0.8,$fn=40);
      offset(0.4)
        polygon(points=[[0,-0.01],[0,0.01],[u_mm(-xpos)-2, u_mm(-ypos)+0.01],[u_mm(-xpos)-2, u_mm(-ypos)-0.01]]);
    }
  }
  if(connections[2] == "connect") {
    translate([half_width-1,8.875,0]) {
      circle(d=0.8,$fn=40);
    }
    translate([half_width-1,4.9,0]) {
      circle(d=0.8,$fn=40);
    }
    translate([half_width-1,3.3,0]){
      circle(d=0.8,$fn=40);
    }
  }
}

module rgb_pcb_drill(width=1, height=1, rgb=true, connections=["hole","hole","hole","hole"]) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  translate([half_width,half_height,0]) {
    if(rgb == true) {
      // LED Hole
      translate([-1.875,3.4])
        square([3.75,3]);

      // LED D
      if(connections[3] == "hole")
        translate([1.3-half_width,8,0])
          circle(d=1,$fn=40);
      if(connections[2] == "hole")
        translate([half_width-1.3,8,0])
          circle(d=1,$fn=40);

      // LED G
      if(connections[3] == "hole")
        translate([1.3-half_width,5.4,0])
          circle(d=1,$fn=40);
      if(connections[2] == "hole")
        translate([half_width-1.3,5.4,0])
          circle(d=1,$fn=40);

      // LED V
      if(connections[3] == "hole")
        translate([1.3-half_width,2.8,0])
          circle(d=1,$fn=40);
      if(connections[2] == "hole")
        translate([half_width-1.3,2.8,0])
          circle(d=1,$fn=40);
    }

    children();
  }
}

module rgb_pcb_hole_traces(width=1, height=1, rgb=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"]) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  translate([half_width,half_height,0]) {
    if(rgb == true) {
      // LED D
      if(connections[3] == "hole")
        translate([1.3-half_width,8,0])
          circle(d=2.5,$fn=40);
      if(connections[2] == "hole")
        translate([half_width-1.3,8,0])
          circle(d=2.5,$fn=40);

      // LED G
      if(connections[3] == "hole")
        translate([1.3-half_width,5.4,0])
          circle(d=2.5,$fn=40);
      if(connections[2] == "hole")
        translate([half_width-1.3,5.4,0])
          circle(d=2.5,$fn=40);

      // LED V
      if(connections[3] == "hole")
        translate([1.3-half_width,2.8,0])
          circle(d=2.5,$fn=40);
      if(connections[2] == "hole")
        translate([half_width-1.3,2.8,0])
          circle(d=2.5,$fn=40);
    }

    children();
  }
}

module rgb_pcb_traces(width=1, height=1, rgb=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"]) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  rgb_pcb_hole_traces(width=width, height=height, rgb=rgb, connections=connections) {
    if(rgb == true) {
      rgb_row_trace_connection(width=width, height=height, xpos=xpos, ypos=ypos, rgb=rgb, connections=connections);
      v_left = connections[3] == "none" ? 1 : half_width-5;
      // LED G
      translate([1.25,5])
        square([2,2]);
      translate([2.7,8.5,0]) {
        length = connections[2] == "none" ? 2 : half_width-3.7; 
        square([length,0.75]);
      }
      translate([2.7,6.8])
        square([0.8,2.4]);
      translate([-3.5,6.2])
        square([7,0.8]);
      translate([-3.5,6.8])
        square([0.8,2.4]);
      translate([-4-v_left,8.5,0])
        square([v_left+1,0.75]);

      // LED D
      translate([-4-v_left,4.5,0])
        square([v_left,0.8]);
      translate([-4.5,4.5,0])
        square([0.8,1.3]);
      translate([-4.5,5,0])
        square([1.3,0.8]);
      translate([2,4,0])
        square([2,0.8]);
      translate([4,4,0])
        square([0.8,1.3]);
      translate([4,4.5,0]) {
        length = connections[2] == "none" ? 0 : half_width-5; 
        square([length,0.75]);
      }
      translate([-3.375,5])
        square([2,1.1]);
      translate([1.25,3.75])
        square([2,1.1]);

      // LED V
      v_right = connections[2] == "none" ? 0 : half_width-5.25;
      translate([-4-v_left,2.9,0])
        square([v_right+v_left+8.875,0.8]);
      translate([-3.375,3.5])
        square([2,1.35]);
    }

    children();
  }
}
