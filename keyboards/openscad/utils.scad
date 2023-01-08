module centerChildren()
{
    translate([ BOARD_X1, BOARD_Y1, 0 ]) children();
}

module tube(or, ir, h)
{
    difference()
    {
        cylinder(h = h, r = or);
        translate([ 0, 0, -h / 2 ]) cylinder(h = h * 2, r = ir);
    }
}

module mirror4()
{
    children();
    mirror([ 1, 0, 0 ]) children();
    mirror([ 0, 1, 0 ]) children();
    mirror([ 0, 1, 0 ]) mirror([ 1, 0, 0 ]) children();
}

module bottomCase(blen2, bwidth2, offset, height)
{
    blen = blen2 + offset * 2;
    bwidth = bwidth2 + offset * 2;

    hull() mirror4()
    {
        translate([ -blen / 2, -bwidth / 2, 0 ]) cylinder(h = height, r = 10);
    }
}

module mountingHoles(blen, bwidth, offset, height)
{
    mirror4() translate([ -blen / 2 + offset, -bwidth / 2 + offset, 0 ]) cylinder(h = height * 10, r = 10);
}

module mountingStandoffs(blen, bwidth, offset, d, height)
{
    // The real radius gets put in during voids
    color("red") mirror4() translate([ -blen / 2 + offset, -bwidth / 2 + offset, 0 ]) tube(d + 2, .1, height);
}

module bodyVoids()
{
    mountingHoles(BOARD_LEN, BOARD_WID, MOUNTING_HOLE_OFFSET, STANDOFF_HOLE_HEIGHT);
}

module line(x1, y1, x2, y2)
{
    hull()
    {
        translate([ x1, y1, 0 ]) cube(1);
        translate([ x2, y2, 0 ]) cube(1);
    }
}

module keyBoundingBoxes()
{
    for (box = keyBoundingBoxes)
    {
        x1 = box[1];
        y1 = box[2];
        x2 = box[3];
        y2 = box[4];

        translate([ 0, 0, BASE_THICKNESS ]) color("blue") {
            line(x1, y1, x2, y1);
            line(x1, y2, x2, y2);
            line(x1, y1, x1, y2);
            line(x2, y1, x2, y2);
        }
    }
}

module body()
{
    difference()
    {
        bottomCase(BOARD_LEN, BOARD_WID, MOUNTING_HOLE_OFFSET, CASE_HEIGTH);
          translate([ 0, 0, -CASE_HEIGTH ]) resize([ BOARD_LEN + 1, BOARD_WID + 1, CASE_HEIGTH *3 ]) centerChildren()
            caseBoundBox();
}
        translate([ 0, 0, BASE_THICKNESS ])  centerChildren()
            caseBoundBox();

    translate([ 0, 0, BASE_THICKNESS ]) centerChildren()
    {
        standOffs();
        keyBoundingBoxes();
    }
    translate([ 0, 0, BASE_THICKNESS ])
        mountingStandoffs(BOARD_LEN, BOARD_WID, MOUNTING_HOLE_OFFSET, MOUNTING_HOLE_D, STANDOFF_HOLE_HEIGHT);
}

module main()
{
    difference()
    {
        body();
        bodyVoids();
    }
}