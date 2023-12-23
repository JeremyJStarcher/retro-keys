include <variables.scad>
use <utilities.scad>
use <circuits.scad>

function key_width(key) = (key[0] == undef ? 1 : key[0]) + (key[1] == undef ? 0 : key[1]);
function width_row(row) = len(row) == 0 ? 0 : key_width(row[0]) + width_row(pop(row));
function width_board(rows) = len(rows) == 0 ? 0 : (
  let (current = width_row(rows[0]))
  let (next = width_board(pop(rows)))
    current > next ? current : next);

function key_height(key) = (key[2] == undef ? 0 : key[2]);
function height_row(row) = len(row) == 0 ? [0,0] : (
  let(other_rows = height_row(pop(row)))
  let(current = key_height(row[0]) + other_rows[0])
  let(maximum = current > other_rows[1] ? current : other_rows[1])
  [current, maximum]);
function height_board_rec(rows) = len(rows) == 0 ? 0 : (
  let (current = height_row(reverse(rows[0]))[1])
  let (next = height_board_rec(pop(rows)))
    current > next ? current : next);
function height_board(rows) = 
  let (height_rec = height_board_rec(rows))
    len(rows) + (height_rec > 0 ? height_rec : 0);

module case(rows, style="mx", margin=5, thickness=5, depth=0, radius=2, rest=0, circuits=[], _inherit_children="unset") {
  total_thickness = thickness + depth + height_for_style(style);
  z_offset = depth + height_for_style(style);
  if($children != 0 && (_inherit_children == "unset" || _inherit_children > 0)) {
    translate([0, 0, -z_offset])
      linear_extrude(total_thickness)
        offset(margin)
          children();
  } else {
    width=u_mm(width_board(rows))+margin*2;
    height=u_mm(height_board(rows))+margin*2+rest;
    translate([-margin, -margin, -z_offset]){
      translate([radius, 0, 0])
        cube([width-radius*2, height,total_thickness]);
      translate([0, radius, 0])
        cube([width, height-radius*2,total_thickness]);
      translate([radius, radius, 0])
        cylinder(total_thickness,radius,radius, $fn=60);
      translate([width-radius, radius, 0])
        cylinder(total_thickness,radius,radius, $fn=60);
      translate([width-radius, height-radius, 0])
        cylinder(total_thickness,radius,radius, $fn=60);
      translate([radius, height-radius, 0])
        cylinder(total_thickness,radius,radius, $fn=60);
    }
    if(len(circuits) > 0)
      translate([0, 0, -z_offset])
        linear_extrude(total_thickness)
          offset(margin)
            circuits_pcb_outline(circuits);
  }
}
