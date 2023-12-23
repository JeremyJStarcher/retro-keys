// openspecad --only-functions
include <../../lib/variables.scad>

// Test u_mm
assert(u_mm(1) == key_size, "1u conversion should equal key size (19.05)");
echo("u_mm successful!");

// Test hole_offset
assert(hole_offset(2) == 12.05, "hole offset did not match expected size for 2u");
echo("hole_offset successful!");

// Test height_for_style
assert(height_for_style("choc_v1") == 2.2, "height_for_style returns a value when given a valid style");
assert(height_for_style("non-existant") == "invalid style", "height for style must be given a valid style");
echo("height_for_style successful!");
