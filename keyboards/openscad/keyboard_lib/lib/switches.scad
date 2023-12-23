use <utilities.scad>
include <switches/mx.scad>
include <switches/choc_v1.scad>

module rotate_translate(rotation, xpos, ypos) {
  if(rotation[0] == undef || rotation[0] == 0) {
    translate([u_mm(xpos), u_mm(ypos), 0]) {
      children();
    }
  } else {
    xoff = rotation[1] == undef ? 0 : rotation[1];
    yoff = rotation[2] == undef ? 0 : rotation[2];
    angle = rotation[0] == undef ? 0 : rotation[0];
    translate([u_mm(xpos - xoff), u_mm(ypos - yoff), 0])
      rotate(angle)
        translate([u_mm(xoff), u_mm(yoff), 0])
          children();
  }
}

module switch(type, style="mx", rgb=true, xpos=0, ypos=0, width=1, cnc=false, rotation=[0,0,0], connections=["hole","hole","hole","hole"], last_xpos=0, last_ypos=0) {
  rotate_translate(rotation, xpos, ypos) {
    if(type == "outline")
      pcb_switch_outline(width=width);
    if(style == "mx") {
      if(type == "key")
        pcb_switch_space_outline(width=width, cnc=cnc, style="mx");
      if(type == "traces")
        switch_mx_pcb_traces(width=width, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections, last_xpos=last_xpos, last_ypos=last_ypos);
      if(type == "traces_top")
        switch_mx_pcb_traces(width=width, single=false, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections, last_xpos=last_xpos, last_ypos=last_ypos);
      if(type == "traces_bottom")
        switch_mx_pcb_traces_bottom(width=width, rgb=rgb, xpos=xpos, ypos=ypos, connections=connections, last_xpos=last_xpos, last_ypos=last_ypos);
      if(type == "drill")
        switch_mx_pcb_drill(width=width, rgb=rgb, connections=connections);
      if(type == "drill_double")
        switch_mx_pcb_drill(width=width, single=false, rgb=rgb, connections=connections);
    }

    if(style == "choc_v1") {
      if(type == "key")
        pcb_switch_space_outline(width=width, cnc=cnc, style="choc_v1");
      if(type == "traces")
        switch_choc_v1_pcb_traces(width=width);
      if(type == "traces_top")
        switch_choc_v1_pcb_traces(width=width);
      if(type == "traces_bottom")
        assert(false, "traces_bottom is incompatible with choc_v1");
      if(type == "drill")
        switch_choc_v1_pcb_drill(width=width);
      if(type == "drill_double")
        switch_choc_v1_pcb_drill(width=width, single=false);
    }

    if(style == "redragon") {
      if(type == "key")
        pcb_switch_space_outline(width=width, cnc=cnc, style="redragon");
      if(type == "traces")
        switch_mx_pcb_traces(width=width, rgb=rgb);
      if(type == "traces_top")
        switch_mx_pcb_traces(width=width, single=false, rgb=rgb);
      if(type == "traces_bottom")
        switch_mx_pcb_traces_bottom(width=width, rgb=rgb);
      if(type == "traces")
        switch_mx_pcb_traces(width=width, rgb=rgb);
      if(type == "drill")
        switch_mx_pcb_drill(width=width);
      if(type == "drill_double")
        switch_mx_pcb_drill(width=width, single=false);
    }
  }
}

module switch_row(keys, style="mx", rgb=true, margin=5, thickness=10, depth=0, cnc=false, type="key", last_row=[], last_xpos=0, previous_xpos=0, last_ypos=0, previous_ypos=0) {
  width = keys[0][0] == undef ? 1 : keys[0][0];
  xpos = keys[0][1] == undef ? 0 : keys[0][1];
  ypos = keys[0][2] == undef ? 0 : keys[0][2];
  rotation = keys[0][3] == undef ? [0,0,0] : keys[0][3];
  connections = keys[0][4] == undef ? ["hole","hole","hole","hole"] : keys[0][4];
  last_ypos = last_row[0][2] == undef ? last_ypos - previous_ypos : last_row[0][2]+last_ypos - previous_ypos;
  last_xpos = last_row[0][1] == undef ? last_xpos - previous_xpos : last_row[0][1]+last_xpos - previous_xpos;
  switch(type, style=style, rgb=rgb, xpos=xpos, ypos=ypos, width=width, cnc=cnc, rotation=rotation, connections=connections, last_xpos=last_xpos, last_ypos=last_ypos);
  if(len(keys) > 1) {
    translate([xpos*key_size+width*key_size, ypos*key_size, 0])
      switch_row(pop(keys), style=style, rgb=rgb, margin=margin, thickness=thickness, depth=depth, cnc=cnc, type=type, last_row = pop(last_row), last_xpos=last_xpos, previous_xpos=xpos, last_ypos=last_ypos, previous_ypos=ypos);
  }
}

module switches(switches, style="mx", rgb=true, margin=5, thickness=10, depth=0, cnc=false, type="key", last_row=[]) {
  if(len(switches) != 0) {
    switch_row(switches[0], style=style, rgb=rgb, margin=margin, thickness=thickness, depth=depth, cnc=cnc, type=type, last_row=last_row);
    if(len(switches) > 1) {
      last_row = switches[0];
      translate([0, key_size, 0])
        switches(pop(switches), style=style, rgb=rgb, margin=margin, depth=depth, thickness=thickness, cnc=cnc, type=type, last_row=last_row);
    }
  }
}
