// use <../keyboard.scad>
use <../../openscad/keyboard_lib/keyboard.scad>


/*
#### Rows Array
A row is made up of keys like `row=[<key>, <key>, <key>, <key>]`. Each
key is relative to the key that precedes it. So if a key is lowered by
0.25u, the next key will be in line with it.

#### Keys Array
A key is made up of information about it's size and position. Like
`key=[<width>,<xpos>,<ypos>,<rotation>,<pcb options>]`.

#### Rotation Array
A rotation array is made up of information about where to rotate from and
how much to rotate. Like `rotate=[<angle degrees>, <x offset>, <y offset>]`
The x and y offset is based on the top right corner of the key, and the
rotation is clockwise when looking at the top of the board.

*/

None = undef;

layout = [
  [[],[],[],[],[],[],[],[],[],[],[],[],[],[2]],
  [[1.5],[],[],[],[],[],[],[],[],[],[],[],[],[1.5]],
  [[1.75],[],[],[],[],[],[],[],[],[],[],[],[2.25]],
  [[2.25],[],[],[],[],[],[],[],[],[],[],[2.75]],
  [[1.25],[1.25],[1.25],[6.25],[1.25],[1.25],[1.25],[1.25]]
];

layout3 =[[[1.25, 11.5, 1.25], [1.25, None, None], [1.25, None, None], [1.25, 1.25, None]], [[1, 0.25, -0.75], [1, 0.25, None], [1, 0.25, None], [1, 0.25, None], [1, 0.25, None]], [[1.25, None, 0.25], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [1.25, 1.25, None]], [[1.75, None, None], [], [], [], [], [], [], [], [], [], [], [1, None, None], [1, None, None], [1.5, None, None]], [[1.25, 16.5, -0.75]], [[2, None, -0.25], [], [], [], [1, None, None], [], [], [1, None, None], [], [], [1, None, None], [1, None, None], [1, None, None], [1.25, None, None]], [[1.25, 16.5, -0.5]], [[2, 0.5, -0.5], [], [], [], [], [], [], [], [1, None, None], [], [], [1.75, None, None], [1, None, None], [1, None, None]], [[1.25, 16.5, -0.25]], [[1, 2, -0.75], [6.25, 1.75, None], [1, 2.25, None], [], []]]
;

board(layout, cnc=false);


// This line to generates an STL for a plate
//top_plate(layout, cnc=false);

// Uncomment this line to generate a DXF for a plate
//  top_plate_drawing(layout);

// Uncomment this line to generate the top case for the keyboard
// top_case(layout, depth=7, radius=3);

// Uncomment this line to generate a bottom case for the keyboard
// bottom_case(layout, radius=3);

// This line will generate a DXF for the top of a rudamentry pcb
// pcb_traces(layout);

// This line will generate a DXF for the drill pattern of a rudamentry pcb
// pcb_drill(layout);
