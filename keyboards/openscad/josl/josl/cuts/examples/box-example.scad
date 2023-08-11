//
// Cut a simply cube.
//
// (C) 2019 Johannes Ernst.
// License: see package.
//

use <../comb.scad>
use <../puzzle.scad>
use <../zigzag.scad>
use <../leftright.scad>

module MyPart() {
    translate( [ -50, 0, 0 ] ) {
        cube( [ 100, 100, 5 ] );
    }
}

// Uncomment this for a comb cut
// Cut at the default locations
// Comb() {
//     MyPart();
// }

// Uncomment this for a comb cut
// Cut at the specified locations
// Comb( y=[ 20, 40, 80 ] ) {
//     MyPart();
// }

// Uncomment this for a zig-zag cut
// ZigZag( y = [ 10, 30 ] ) {
//     MyPart();
// }

// Uncomment this for a puzzle cut
Puzzle( y = [ 10, 50, 80 ] ) {
    
    MyPart();
}


%    MyPart();
