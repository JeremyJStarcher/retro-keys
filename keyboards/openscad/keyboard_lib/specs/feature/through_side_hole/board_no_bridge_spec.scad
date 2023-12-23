use <board_spec.scad>

board(layout(), depth=4, circuits=circuit(), bridge=false, inner_margin=2){
  the_case();
}