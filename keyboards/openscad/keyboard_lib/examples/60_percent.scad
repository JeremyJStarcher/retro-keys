use <../keyboard.scad>

layout = [
  [[],[],[],[],[],[],[],[],[],[],[],[],[],[2]],
  [[1.5],[],[],[],[],[],[],[],[],[],[],[],[],[1.5]],
  [[1.75],[],[],[],[],[],[],[],[],[],[],[],[2.25]],
  [[2.25],[],[],[],[],[],[],[],[],[],[],[2.75]],
  [[1.25],[1.25],[1.25],[6.25],[1.25],[1.25],[1.25],[1.25]]
];

// This line to generates an STL for a plate
//top_plate(layout, cnc=false);

// Uncomment this line to generate a DXF for a plate
 top_plate_drawing(layout);

// Uncomment this line to generate the top case for the keyboard
// top_case(layout, depth=7, radius=3);

// Uncomment this line to generate a bottom case for the keyboard
// bottom_case(layout, radius=3);

// This line will generate a DXF for the top of a rudamentry pcb
// pcb_traces(layout);

// This line will generate a DXF for the drill pattern of a rudamentry pcb
// pcb_drill(layout);
