module tube(or, ir, h) {
    difference() {
        cylinder(h = h, r = or);
        translate([0, 0, -h/2])
        cylinder(h = h*2, r = ir);
    }
}
