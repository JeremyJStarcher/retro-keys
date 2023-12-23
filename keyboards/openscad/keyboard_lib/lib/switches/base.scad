include <../variables.scad>
include <rgb.scad>

// ["top", "bottom", "left", "right"]

module switch_row_trace_connection(width, height, xpos, ypos, rgb, connections) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  if(connections[3] == "connect") {
    translate([1-half_width,-5.5,0]){
      circle(d=0.8,$fn=40);
      offset(0.4)
        polygon(points=[[0,-0.01],[0,0.01],[u_mm(-xpos)-2, u_mm(-ypos)+0.01],[u_mm(-xpos)-2, u_mm(-ypos)-0.01]]);
    }
  }
  if(connections[2] == "connect") {
    translate([half_width-1,-5.5,0]) {
      circle(d=0.8,$fn=40);
    }
  }
}

module switch_column_trace_connection(width, height, xpos, ypos, rgb, connections, last_xpos=0, last_ypos=0) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  if(connections[1] == "connect") {
    translate([-u_mm((width-1)/2)-0.9,half_height-1,0]) {
      circle(d=0.8,$fn=40);
      offset(0.4)
        polygon(points=[[0,-0.01],[0,0.01],[u_mm((width-1)/2),0.01],[u_mm((width-1)/2),-0.01]]);
    }
  }
  if(connections[0] == "connect") {
    y_off = u_mm(ypos-last_ypos);
    x_off = u_mm(last_xpos-xpos);
    translate([-0.875,-1-y_off-half_height,0]) {
      offset(0.4)
        polygon(points=[[-0.01+x_off,0],[0.01+x_off,0],[0.01,2+y_off],[-0.01,2+y_off]]);
      translate([x_off-0.01,0]) {
        offset(0.4)
          polygon(points=[[0,-0.01],[0,0.01],[u_mm((width-1)/2)+1,0.01],[u_mm((width-1)/2)+1,-0.01]]);
      }
    }
  }
}

module switch_base_pcb_drill(width=1, height=1, rgb=true, single=true, connections=["hole","hole","hole","hole"]) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  rgb_pcb_drill(width=width, height=height, rgb=rgb, connections=connections) {
    // Row
    if(connections[2] == "hole")
      translate([half_width-1.3,-5.5,0])
        circle(d=1,$fn=40);
    if(connections[3] == "hole")
      translate([1.3-half_width,-5.5,0])
        circle(d=1,$fn=40);

    // Column
    if(connections[1] == "hole")
      translate([-1,half_height-1.25,0])
        circle(d=1,$fn=40);
    if(connections[0] == "hole")
      translate([-1,1.25-half_height,0])
        circle(d=1,$fn=40);

    children();
  }
}

module switch_base_pcb_traces(width=1, height=1, rgb=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"], last_xpos=0, last_ypos=0, single=true) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  rgb_pcb_traces(width=width, height=height, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections) {
    switch_row_trace_connection(width, height, xpos, ypos, rgb, connections);
    if(single && !rgb)
      switch_column_trace_connection(width, height, xpos, ypos, rgb, connections, last_xpos=last_xpos, last_ypos=last_ypos);

    // Row
    if(connections[2] == "hole")
      translate([half_width-1.3,-5.5,0])
        circle(d=2.5,$fn=40);
    if(connections[3] == "hole")
      translate([1.3-half_width,-5.5,0])
        circle(d=2.5,$fn=40);

    // Column
    if(connections[1] == "hole")
      translate([-1,half_height-1.25,0])
        circle(d=2.4,$fn=40);
    if(connections[0] == "hole")
      translate([-1,1.25-half_height,0])
        circle(d=2.4,$fn=40);

    children();
  }
}

module switch_base_pcb_traces_bottom(width=1, height=1, rgb=true, xpos=0, ypos=0, connections=["hole","hole","hole","hole"], last_xpos=0, last_ypos=0) {
  half_width = u_mm(width)/2;
  half_height = u_mm(height)/2;
  rgb_pcb_hole_traces(width=width, height=height, rgb=rgb, connections=connections) {
    switch_column_trace_connection(width, height, xpos, ypos, rgb, connections, last_xpos=last_xpos, last_ypos=last_ypos);

    // Row
    if(connections[2] == "hole")
      translate([half_width-1.3,-5.5,0])
        circle(d=2.5,$fn=40);
    if(connections[3] == "hole")
      translate([1.3-half_width,-5.5,0])
        circle(d=2.5,$fn=40);

    // Column
    if(connections[1] == "hole")
      translate([-1,half_height-1.25,0])
        circle(d=2.5,$fn=40);
    if(connections[0] == "hole")
      translate([-1,1.25-half_height,0])
        circle(d=2.5,$fn=40);

    children();
  }
}
