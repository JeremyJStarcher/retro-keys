key_size=19.05;
hole=14;

function u_mm(u) = u*key_size;
function hole_offset(u) = (key_size-hole)/2+u_mm(u-1)/2;

// This is used to determine how much space is between the top
// of the plate and the PCB.
function height_for_style(style) = style == "mx"        ? 5.334 :
                                   style == "redragon" ? 3.75  :
                                   style == "choc_v1"   ? 2.2   :  "invalid style";
