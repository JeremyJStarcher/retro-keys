function circuit() = [[8,0,0,0,"pro_micro"],[9.1,0,0,0,"trrs_right"],];

function layout() = [
  [[6.26], [1,1,1,[20,1,2]]],
  [[2.25],[1.75],[1.25],[]]
];

module the_case() {
  translate([-u_mm(1), -u_mm(1)])
    square([u_mm(10), u_mm(5)]);
}

include <../../../keyboard.scad>
