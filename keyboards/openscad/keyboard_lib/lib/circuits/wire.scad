module guage(guage=12) {
  fn=20;
  if(guage == 8) {
    circle(d=3.25, $fn=fn);
  } else if (guage == 10) {
    circle(d=2.59, $fn=fn);
  } else if (guage == 12) {
    circle(d=2.06, $fn=fn);
  } else if (guage == 14) {
    circle(d=1.57, $fn=fn);
  } else if (guage == 16) {
    circle(d=1.3, $fn=fn);
  }
}

module wire_pcb_drill(guage=12) {
  offset(0.1)
    guage(guage);
}

module wire_pcb_traces(guage=12) {
  offset(0.75)
    guage(guage);
}

module wire_pcb_outline(guage=12) {
  offset(1.5)
    guage(guage);
}

module wire_space_outline(guage=12) {
  linear_extrude(10)
    offset(0.1)
      guage(guage);
}
