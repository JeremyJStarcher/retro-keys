include <layout.scad>

module outline() {
    offset(10)
      case();
}

module topcase() {
  difference() {
    linear_extrude(15)
      outline();
    translate([0,0,5])
      top_case(layout=layout(), circuits=circuits(), depth=5, margin=11) {
        case();
      }
  }
}

outline();