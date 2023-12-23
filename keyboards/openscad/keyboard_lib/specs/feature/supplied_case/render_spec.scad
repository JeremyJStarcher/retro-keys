use <base.scad>

parts=[
  ["top_case", "#2a1506"],
  ["top_plate", "silver"],
  ["bottom_case", "#8b4513"],
  ["pcb_render", "green"]
];

render_mockup(layout(), parts=parts, inner_margin=3, depth=5, radius=5);