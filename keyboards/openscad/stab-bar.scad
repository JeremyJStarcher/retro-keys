len = 20; // 100;
deep = 12.5;
d = 1.61; // 1/16"
turn_radius = 2;

$fn = 100;

module outline() {
    module e() {
        translate([len/2 - d/2, deep/2, 0])
        rotate([90, 0, 0])
        cylinder(h = deep, r = d/2, center=true);
    }


     translate([0, 0, 0]) {
        rotate([0, 90, 0])
        cylinder(h = len, r = d/2, center=true);


        
        // e();
        // mirror([1, 0, 0]) e();
    }
}


outline();



module side() {

    
    translate([len/2 - turn_radius, turn_radius/2, 0])

    rotate([0, 0, 90 * 3])
    rotate_extrude( angle=90)
    translate([turn_radius/2,0,0])
    circle(r = d/4);
    
    
    color("blue")
    translate([len/2 - d/2, deep, 0])
    rotate([90, 0, 0])
    cylinder(h = deep - turn_radius/2, r = d/2);
    
}

//rotate([0, 90, 0])
//cylinder(h = len - turn_radius, r = d/2, center=true);

//side();
///mirror([1, 0, 0]) side();

//square([2,10], center=true);