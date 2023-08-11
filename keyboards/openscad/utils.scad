use <./josl/josl/cuts/comb.scad>
use <./josl/josl/cuts/leftright.scad>
use <./josl/josl/cuts/puzzle.scad>
use <./josl/josl/cuts/zigzag.scad>

STANDOFF_STYLE = "pin"; // "void"

module main(BOARD_WIDTH, BOARD_LEN, CASE_PIECES, CASE_PIECE)
{
    // $fs = $preview ? 1 : 0.3;
    // $fa = $preview ? 3 : 0.3;

    //$fn = 100;

    // Radius of the case corner
    CASE_CORNER_R = 3;
    PCB_THICKNESS = 1.6;
    SCREW_HEAD_GAP = 3;
    SCREW_HEAD_R = 3;
    LAYER_HEIGHT = 0.2;

    // HOw much of a gap between the PCB and the case
    CASE_GAP = 2;

    function puzzleApart() = max(BOARD_WIDTH, BOARD_LEN);

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
        mirror4()                                                      //
            translate([ -blen / 2 + offset, -bwidth / 2 + offset, 0 ]) //
            cylinder(h = height * 10, r = MOUNTING_HOLE_D / 2);

        // Drop down below the zero line to make sure there is no interference
        mirror4() //
            translate([ -blen / 2 + offset, -bwidth / 2 + offset, -SCREW_HEAD_GAP ])
        { //
            cylinder(h = SCREW_HEAD_GAP * 2, r = SCREW_HEAD_R + 1);
            //  cylinder(h = SCREW_HEAD_GAP *2, r2 = SCREW_HEAD_R+1, r1=MOUNTING_HOLE_D / 2);
        }
    }

    module mountingStandoffs(blen, bwidth, offset, d, height)
    {
        // The real radius gets put in during voids
        color("red") mirror4() translate([ -blen / 2 + offset, -bwidth / 2 + offset, 0 ]) tube(d + 2, .1, height);
    }

    module bodyVoids()
    {
        mountingHoles(BOARD_LEN, BOARD_WIDTH, MOUNTING_HOLE_OFFSET, STANDOFF_HOLE_HEIGHT);

        if (STANDOFF_STYLE != "pin") {
            centerChildren() standOffs(false);
        }
    }

    module line(x1, y1, x2, y2)
    {
        hull()
        {
            translate([
                x1,
                y1,
            ]) cube(.4);
            translate([
                x2,
                y2,
            ]) cube(.4);
        }
    }

    module standOffs(isSolid)
    {

        $fa = 1;
        $fs = 1;

        for (standoff = keyStandoffs)
        {
            x = standoff[0];
            y = standoff[1];

            translate([ x, y, 0 ])
            {
                if (isSolid)
                {
                    color("black")                                //
                        cylinder(                                 //
                            r = STANDOFF_HOLE_OUTER_DIAMETER / 2, //
                            h = STANDOFF_HOLE_HEIGHT);

                    if (STANDOFF_STYLE == "pin") {
                     *   color("yellow")                           //
                        cylinder(                                 //
                            r = STANDOFF_HOLE_INNER_DIAMETER / 2, //
                            h = STANDOFF_HOLE_HEIGHT+2);
                    }
                }

                if (!isSolid)
                {
                    color("magenta")                              //
                        translate([ 0, 0, BASE_THICKNESS ])       //                              //
                        cylinder(                                 //
                            r = STANDOFF_HOLE_INNER_DIAMETER / 2, //
                            h = STANDOFF_HOLE_HEIGHT + PCB_THICKNESS);
                }
            }
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

            translate([ 0, 0, 0 ]) color("blue")
            {
                line(x1, y1, x2, y1);
                line(x1, y2, x2, y2);
                line(x1, y1, x1, y2);
                line(x2, y1, x2, y2);
            }

            cx = (x1 + x2) / 2;
            cy = (y1 + y2) / 2;

            // Grab just the first two characters since the whole name won't fit
            // in a readable font
            char1 = is_string(box[0][0]) ? box[0][0] : "";
            char2 = is_string(box[0][1]) ? box[0][1] : "";
            label = str(char1, char2);

            color("green") translate(v = [ cx, cy, 0 ]) linear_extrude(height = LAYER_HEIGHT)
                text(label, valign = "center", halign = "center", size = 9);
        }
    }

    module centerCubeXy(wid, len, height)
    {
        translate([ -wid / 2, -len / 2, BASE_THICKNESS ]) cube([ wid, len, height ]);
    }

    module body()
    {
        outside_len = BOARD_LEN + CASE_CORNER_R + CASE_GAP;
        outside_width = BOARD_WIDTH + CASE_CORNER_R + CASE_GAP;

        lip_len = outside_len - (CASE_CORNER_R);
        lip_width = outside_width - (CASE_CORNER_R);

        difference()
        {
            union()
            {
                color("cyan") bottomCase(outside_len, outside_width, 0, CASE_HEIGHT);
                translate([ 0, 0, BASE_THICKNESS ]) color("navy") bottomCase(lip_len, lip_width, 0, CASE_HEIGHT);
            }

            translate([ 0, 0, -BASE_THICKNESS ])
                centerCubeXy(BOARD_LEN + CASE_GAP, BOARD_WIDTH + CASE_GAP, CASE_HEIGHT * 3);
        }

        // Put the bottom of the case in.
        color("white") //
            bottomCase(outside_len, outside_width, 0, BASE_THICKNESS);

        translate([ 0, 0, BASE_THICKNESS ]) centerChildren()
        {
            standOffs(true);
            keyBoundingBoxes();
        }
        translate([ 0, 0, BASE_THICKNESS ])
            mountingStandoffs(BOARD_LEN, BOARD_WIDTH, MOUNTING_HOLE_OFFSET, MOUNTING_HOLE_D, STANDOFF_HOLE_HEIGHT);
    }

    module keyboardCaseBottom()
    {
        difference()
        {
            body();
            bodyVoids();
        }
    }

    module hideyCube(side, len, width)
    {
        ap = puzzleApart();
        cube([ ap, ap, 100 ], center = true);
    }

    module cutIt(side, len, width)
    {
        $CUT_WIDTH = width;
        ap = puzzleApart();

        factor = 4;

        xOffset = +len / factor + ap / 2;
        xOffsetFixed = xOffset * (side == "r" ? 1 : -1);

        intersection()
        {
            translate([ xOffsetFixed, 0, 0 ]) children();
            hideyCube(side, len, width);
        }
    }

    module split()
    {
        slice = 25;
        list1 = [for (i = [-$CUT_WIDTH:slice:$CUT_WIDTH]) i];
        play = 0.1;

        Puzzle(y = list1, apart = puzzleApart(), play = play)
        {
            children();
        }
    }

    function partial(list, start, end) = [for (i = [start:end]) list[i]];

    module main2()
    {
        // keyboardCaseBottom();

        module cutInto4(c1, c2)
        {
            cutIt(c2, BOARD_LEN / 2, BOARD_WIDTH) //
                split()                           //
                cutIt(c1, BOARD_LEN, BOARD_WIDTH) //
                split()                           //
                keyboardCaseBottom();
        }

        module cutInto2(c1)
        {
            cutIt(c1, BOARD_LEN, BOARD_WIDTH) //
                split()                       //
                keyboardCaseBottom();
        }

        if (CASE_PIECES == 2)
        {
            if (CASE_PIECE == 1)
            {
                cutInto2("l");
            }
            if (CASE_PIECE == 2)
            {
                cutInto2("r");
                // add tabs here
            }
        }

        if (CASE_PIECES == 4)
        {
            if (CASE_PIECE == 1)
            {
                cutInto4("l", "l");
            }

            if (CASE_PIECE == 2)
            {
                cutInto4("l", "r");
            }

            if (CASE_PIECE == 3)
            {
                cutInto4("r", "l");
            }

            if (CASE_PIECE == 4)
            {
                cutInto4("r", "r");
            }
        }
    }

    main2();

    lst = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]; // a list of numbers
    lst2 = [ "red", "yellow", "blue" ];  // a list of strings
    lst3 = [ false, true, undef ];       // a list of booleans

    // https://eribuijs.blogspot.com/2017/10/openscad-lists-and-list-manipulation.html

    // echo(partial(lst, 1, 8));
}