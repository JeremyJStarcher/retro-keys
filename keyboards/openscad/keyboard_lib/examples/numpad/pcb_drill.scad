include <layout.scad>

rotate(90)
  pcb_drill(layout=layout(), circuits=circuits()) {
    case();
  };
