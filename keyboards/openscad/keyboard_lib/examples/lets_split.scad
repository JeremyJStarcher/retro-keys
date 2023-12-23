use <../keyboard.scad>

// Since the two halvs are identical mirrors, this case can be one
// half that you just flip over.
layout = [
  [[],[],[],[],[],[]],
  [[],[],[],[],[],[]],
  [[],[],[],[],[],[]],
  [[],[],[],[],[],[]]
];

// Using a function, we can pass in the part type we'd like to use
// meaning we can set up the render for multiple parts in the same
// orientation
module split(mod, depth) {
  part(mod, layout, depth=depth);
  translate([u_mm(7),0,0])
    mirror([0,0,0])
      part(mod, layout, depth=7);
}

// Then when you want to generate the pieces you can do them together
split("board", depth=7);
