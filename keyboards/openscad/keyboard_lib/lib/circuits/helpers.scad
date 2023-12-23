function bu(u) = u * 2.54;

module breadboard_row(number, orientation="vertical") {
  children();
  if(number > 1) {
    if(orientation == "vertical") {
      translate([0,bu(1),0])
        breadboard_row(number-1, orientation=orientation) {
          children();
        }
    } else {
      translate([bu(1),0,0])
        breadboard_row(number-1, orientation=orientation){
          children();
        }
    }
  }
}