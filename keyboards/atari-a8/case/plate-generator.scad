include <case-position.scad>;

GRID=19.05;

module h() {
    color("red")
    translate([GRID/2, GRID/2])
     include <plate/holes.scad>;
}


BOARD_X1 = -197.64378;
BOARD_Y1 = 248.84060;
BOARD_X2 = 159.54377;
BOARD_Y2 = 389.33440;

module void(l, w) {
    x1 = 0;
    y1 = BOARD_WIDTH;
    
    x2 = x1 + l;
    y2 = y1 - w;
    
    module dot() {
     //   linear_extrude(10)
        square([1, 1], center=true);
    }

    color("blue")
    hull()
    {
        translate([x1, y1]) dot();
        translate([x1, y2]) dot();
        translate([x2, y1]) dot();
        translate([x2, y2]) dot();
    }
}

module frame() {
    difference() {
        color("black")
        square([BOARD_LEN, BOARD_WIDTH ]);
        h();        
        #void(227, 35);
    }
}



frame();