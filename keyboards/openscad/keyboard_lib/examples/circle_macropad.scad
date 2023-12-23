use <../keyboard.scad>

layout = [
  [[1,0,0,[],["hole","connect","connect","hole"]],[1,0,0,[],["hole","connect","hole","connect"]]],
  [[1,0,0,[],["connect","hole","connect","hole"]],[1,0,0,[],["connect","hole","hole","connect"]]]
];
pcb_render(layout, rgb=true, single=false)
  translate([u_mm(1),u_mm(1),0])
    circle(d=u_mm(3));
