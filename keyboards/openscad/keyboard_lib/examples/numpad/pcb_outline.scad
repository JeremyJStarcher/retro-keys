include <layout.scad>
rotate(90)
  pcb_outline(layout=layout(), circuits=circuits()) {
    case();
  };
