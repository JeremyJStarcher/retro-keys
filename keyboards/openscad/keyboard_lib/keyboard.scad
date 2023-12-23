include <lib/variables.scad>
use <lib/case.scad>
use <lib/switches.scad>
use <lib/circuits.scad>

// Generate a 3d printable keyboard case with integrated plate for export to stl
module board(layout, style="mx", margin=5, thickness=5, cnc=false, depth=0, radius=0, circuits=[], inner_margin=0, inner_height=0, bridge=true, _inherit_children="unset") {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  difference() {
    case(layout, style=style, margin=margin, thickness=thickness, depth=depth, radius=radius, circuits=circuits, _inherit_children=final_children) {
        children();
    };
    translate([0, 0, height_for_style(style) + inner_height]) {
      case(layout, style=style, margin=inner_margin, thickness=thickness+depth+height_for_style(style), depth=0, radius=radius, circuits=circuits, _inherit_children=final_children){
        children();
      }
    }
    switches(layout, style=style, margin=margin, cnc=cnc, thickness=thickness, depth=depth);
    if(len(circuits) > 0) {
      circuits_space_outline(circuits);
      linear_extrude(!bridge ? thickness+100 : 0) {
        projection() {
          circuits_space_outline(circuits);
        }
      }
    }
  }
}

// Generate a plate model for export to stl
module top_plate(layout, style="mx", cnc=true, margin=-0.5, radius=0, inner_margin=0, thickness=1.5, circuits=[], _inherit_children="unset") {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  board(layout, style=style, cnc=cnc, margin=margin, radius=radius, inner_margin=inner_margin, circuits=circuits, thickness=thickness - height_for_style(style), depth=0, _inherit_children=final_children) {
    children();
  };
}

// Generate a top plate projection for export to dxf
module top_plate_drawing(layout, style="mx", margin=0, cnc=true, radius=0, circuits=[], _inherit_children="unset") {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  projection() {
    board(layout, style=style, cnc=cnc, circuits=circuits, radius=radius, margin=margin, thickness=1.5 - height_for_style(style), depth=0, _inherit_children=final_children) {
      children();
    };
  }
}

// Generate a top case without an integrated plate
module top_case(layout, style="mx", margin=5, thickness=5, inner_margin=0, depth=0, radius=0, bridge=true, circuits=[], _inherit_children="unset") {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  board(layout, style=style, margin=margin, inner_margin=inner_margin, thickness=thickness, depth=depth, bridge=bridge, radius=radius, circuits=circuits, inner_height=-height_for_style(style)-0.01, _inherit_children=final_children) {
    children();
  };
}

// Generate a bottom case for use with either the one pice board or top
// plus plate cases
module bottom_case(layout, style="mx", plate=1.5, margin=5, inner_margin=0, thickness=5, radius=0, circuits=[], _inherit_children="unset") {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  plate_thickness = plate == "board" ? height_for_style(style) : plate;
  translate([0,0,thickness+height_for_style(style)]) {
    case(layout, style=style, margin=margin, thickness=2 - height_for_style(style), radius=radius, circuits=circuits, _inherit_children=final_children) {
      children();
    }
    translate([0,0,-thickness-height_for_style(style) + plate_thickness]) {
      difference(){
        case(layout, style=style, margin=inner_margin, thickness=thickness-plate_thickness, radius=radius, circuits=circuits, _inherit_children=final_children) {
          children();
        }
        translate([0,0,-6]) {
          linear_extrude(thickness+height_for_style(style)) {
            offset(0.5) {
              pcb_outline(layout, circuits=circuits, _inherit_children=final_children) {
                children();
              }
            }
          }
        }
        if(len(circuits) > 0) {
          translate([0,0,-(thickness+height_for_style(style)+1)]) {
            linear_extrude(thickness+height_for_style(style)+1) {
              projection() {
                circuits_space_outline(circuits);
              }
            }
          }
        }
      }
    }
  }
}

// Generates small pcbs under each key/switch to aid hand wiring (single sided)
// This is a drawing, so it should be used to generate a dxf
module pcb_traces(layout, bit=0, slices=1, style="mx", rgb=true, circuits=[], _current_slice=1) {
  difference() {
    offset((slices-_current_slice)*bit) {
      switches(layout, style=style, rgb=rgb, type="traces");
      circuits_pcb_traces(circuits);
    }
    if(_current_slice < slices) {
      pcb_traces(layout, bit=bit, slices=slices, style=style, rgb=rgb, circuits=circuits, _current_slice=_current_slice+1);
    }
  }
}

// Generates small pcbs under each key/switch to aid hand wiring (top of double sided)
// This is a drawing, so it should be used to generate a dxf
module pcb_traces_top(layout, bit=0, slices=1, style="mx", rgb=true, circuits=[], _current_slice=1) {
  difference() {
    offset((slices-_current_slice)*bit) {
      switches(layout, style=style, rgb=rgb, type="traces_top");
      circuits_pcb_traces(circuits);
    }
    if(_current_slice < slices) {
      pcb_traces(layout, bit=bit, slices=slices, style=style, rgb=rgb, circuits=circuits, _current_slice=_current_slice+1);
    }
  }
}

// Generates small pcbs under each key/switch to aid hand wiring (bottom of double sided)
// This is a drawing, so it should be used to generate a dxf
module pcb_traces_bottom(layout, bit=0, slices=1, style="mx", rgb=true, circuits=[], _current_slice=1) {
  difference() {
    offset((slices-_current_slice)*bit) {
      switches(layout, style=style, rgb=rgb, type="traces_bottom");
      circuits_pcb_traces_bottom(circuits);
    }
    if(_current_slice < slices) {
      pcb_traces_bottom(layout, bit=bit, slices=slices, style=style, rgb=rgb, circuits=circuits, _current_slice=_current_slice+1);
    }
  }
}

// Generates pcbs drill location under each key/switch to aid hand wiring
// This is a drawing, so it should be used to generate a dxf
module pcb_drill(layout, style="mx", rgb=true, circuits=[], single=true) {
  type = single ? "drill" : "drill_double";
  switches(layout, style=style, rgb=rgb, type=type);
  circuits_pcb_drill(circuits);
}

// Generates an outline of the pcb
// This is a drawing, so it should be used to generate a dxf
module pcb_outline(layout, bit=0, style="mx", circuits=[], _inherit_children="unset") {
  offset(bit/2) {
    switches(layout, style=style, type="outline");
    circuits_pcb_outline(circuits);
    if($children != 0 && (_inherit_children == "unset" || _inherit_children > 0)) {
      offset(-4) {
        children();
      }
    }
  }
}

// Generates a render of the pcb
// Used to prototype or visualize the part in advance
module pcb_render(layout, style="mx", rgb=true, circuits=[], _inherit_children="unset", single=true) {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  difference() {
    union() {
      color("green") {
        linear_extrude(1) {
          pcb_outline(layout, style=style, circuits=circuits, _inherit_children=final_children) {
            children();
          }
        }
      }
      if(single){
        color("red") {
          translate([0,0,-0.5]) {
            linear_extrude(1) {
              pcb_traces(layout, rgb=rgb, style=style, circuits=circuits);
            }
          }
        }
      }
      if(!single){
        color("red") {
          translate([0,0,-0.5]) {
            linear_extrude(1) {
              pcb_traces_top(layout, rgb=rgb, style=style, circuits=circuits);
            }
          }
        }
      }
      if(!single){
        color("yellow") {
          translate([0,0,0.5]) {
            linear_extrude(1) {
              pcb_traces_bottom(layout, rgb=rgb, style=style, circuits=circuits);
            }
          }
        }
      }
    }
    translate([0,0,-1]) {
      linear_extrude(3) {
        pcb_drill(layout, style=style, circuits=circuits, rgb=rgb, single=single);
      }
    }
  }
}

// Generic function for generating models that takes an argument for part
// type. Useful when the part is used in a function, allowing for different
// parts to be swapped out
module part(type, layout, style="mx", rgb=true, inner_margin=0, cnc=false, margin=5, depth=0, plate=1.5, thickness=5, radius=0, circuits=[], _inherit_children="unset") {
  final_children = _inherit_children == "unset" ? $children : _inherit_children;
  if(type == "bottom_case")
    bottom_case(layout, style=style, plate=plate, inner_margin=inner_margin, margin=margin, thickness=thickness, radius=radius, _inherit_children=final_children)
      children();
  if(type == "top_case")
    top_case(layout, style=style, margin=margin, depth=depth, inner_margin=inner_margin, thickness=thickness, radius=radius, _inherit_children=final_children)
      children();
  if(type == "board")
    board(layout, style=style, margin=margin, depth=depth, inner_margin=inner_margin, thickness=thickness, radius=radius, _inherit_children=final_children)
      children();
  if(type == "top_plate")
    top_plate(layout, style=style, cnc=cnc, thickness=plate, margin=inner_margin, radius=radius, _inherit_children=final_children)
      children();
  if(type == "top_plate_drawing")
    top_plate_drawing(layout, style=style, cnc=cnc, margin=inner_margin, radius=radius, _inherit_children=final_children)
      children();
  if(type == "pcb_drill")
    pcb_drill(layout, style=style, rgb=rgb, circuits=circuits);
  if(type == "pcb_traces")
    pcb_traces(layout, style=style, rgb=rgb, circuits=circuits);
  if(type == "pcb_outline")
    pcb_outline(layout, style=style, circuits=circuits, _inherit_children=final_children)
      children();
  if(type == "pcb_render")
    pcb_render(layout, style=style, circuits=circuits, _inherit_children=final_children)
      children();
}

// Used to render a mockup of a given design. Default has top case, plate,
// bottom case, and pcb. Parts can be customized and colors can be added.
module render_mockup(layout, parts=[["top_case", "#2a1506"],["top_plate", "silver"],["bottom_case", "#8b4513"],["pcb_render", "green"]], style="mx", cnc=false, inner_margin=0, margin=5, depth=0, plate=1.5, thickness=5, radius=0, circuits=[]) {
  for(part = parts) {
    color(part[1]) {
      part(part[0], layout, style=style, margin=margin, depth=depth, inner_margin=inner_margin, thickness=thickness, radius=radius, _inherit_children=$children){
        children();
      }
    }
  }
}
