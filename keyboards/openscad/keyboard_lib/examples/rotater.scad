use <../keyboard.scad>
layout = [[
          [1,0,0,[15,0,-1]],
          [1,0.05,0,[25,0,-1]],
          [1,0.1,0,[35,0,-1]],
          [1,0.2,0,[45,0,-1]]
        ]];
board(layout, depth=5, radius=10)
  translate([-u_mm(0.1),-u_mm(0.3)])
    square([u_mm(5),u_mm(2)]);
