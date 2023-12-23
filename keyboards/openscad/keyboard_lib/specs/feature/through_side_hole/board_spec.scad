include <../../../keyboard.scad>

function circuit() = [[5,0,0,0,"pro_micro"],[6.3,0,0,0,"trrs_right"],];

function layout() = [
  [[],[],[],[],[]],
  [[1.25],[1.25],[1.25],[1.25]],
  [[1.75],[2.25],[]]
];

module the_case() {
    square([u_mm(7), u_mm(3)]);
}

board(layout(), depth=4, circuits=circuit(), inner_margin=2)
  the_case();