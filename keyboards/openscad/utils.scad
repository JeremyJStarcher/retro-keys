CASE_CORNER_R = 5;

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
        translate([ -blen / 2, -bwidth / 2, 0 ]) cylinder(h = height, r = CASE_CORNER_R);
    }
}

module mountingHoles(blen, bwidth, offset, height)
{
    mirror4() translate([ -blen / 2 + offset, -bwidth / 2 + offset, 0 ])
        cylinder(h = height * 10, r = MOUNTING_HOLE_D / 2);
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

module standOffs()
{
    for (standoff = keyStandoffs)
    {
        x = standoff[0];
        y = standoff[1];

        translate([ x, y, BASE_THICKNESS ]) color("black")
            tube(STANDOFF_HOLE_OUTER_DIAMETER, STANDOFF_HOLE_INNER_DIAMETER, STANDOFF_HOLE_HEIGHT);
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

        translate([ 0, 0, BASE_THICKNESS ]) color("blue")
        {
            line(x1, y1, x2, y1);
            line(x1, y2, x2, y2);
            line(x1, y1, x1, y2);
            line(x2, y1, x2, y2);
        }

        cx = (x1 + x2) / 2;
        cy = (y1 + y2) / 2;
        color("green") translate(v = [ cx, cy, BASE_THICKNESS ]) linear_extrude(height = 1)
            text(box[0], valign = "center", halign = "center", size = 3);
    }
}

module centerCubeXy(wid, len, height)
{
    translate([ -wid / 2, -len / 2, BASE_THICKNESS ]) cube([ wid, len, height ]);
}

module body()
{
    difference()
    {
        CASE_BORDER = 2;
        bottomCase(BOARD_LEN, BOARD_WID, 0, CASE_HEIGTH);
        translate([ 0, 0, -BASE_THICKNESS ]) centerCubeXy(BOARD_LEN + CASE_BORDER, BOARD_WID + CASE_BORDER, CASE_HEIGTH * 3);
    }
    translate([ 0, 0, -0.00 ]) centerChildren() caseBoundBox();

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