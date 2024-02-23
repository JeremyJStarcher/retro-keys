include <case-position.scad>;

GRID=19.05;

module h() {
    color("cyan")
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

    // Carve out the area for the control board
    color("blue")
    hull()
    {
        translate([x1, y1]) dot();
        translate([x1, y2]) dot();
        translate([x2, y1]) dot();
        translate([x2, y2]) dot();
    }
    
}

module mounting_hole_void() {
    translate([BOARD_X1 + BOARD_LEN/2, BOARD_Y1 + BOARD_WIDTH/2 ])
    for (hole = mountingHoles){
        //  [247.65000, 188.11875, 1.5, 3],

        color("red")
        translate([hole[0], (hole[1]) ])
            circle(r = hole[2], $fn=30);
        
    }
}

module top_plate() {
    difference() {
        color("black")
        square([BOARD_LEN, BOARD_WIDTH ]);
        h();        
        mounting_hole_void();
        void(227, 35);
    }
}

module bottom_plate() {
    difference() {
        color("black")
        square([BOARD_LEN, BOARD_WIDTH ]);
        
        mounting_hole_void();
        //h();        
       // void(227, 35);
    }
}


//top_plate();
bottom_plate();
