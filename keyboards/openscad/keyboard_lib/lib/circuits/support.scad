module support_pcb_drill(mm=2) {
  offset(0.1)
    circle(d=mm, $fn=20);
}

module support_pcb_traces(mm=2) {
}

module support_pcb_outline(mm=2) {
  offset(2)
    circle(d=mm, $fn=20);
}

module support_space_outline(mm=2) {
  linear_extrude(10)
    offset(0.1)
      circle(d=mm, $fn=20);
}
