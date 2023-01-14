use <./josl/josl/cuts/comb.scad>
use <./josl/josl/cuts/leftright.scad>
use <./josl/josl/cuts/puzzle.scad>
use <./josl/josl/cuts/zigzag.scad>

module main(BOARD_WIDTH, BOARD_LEN)
{

    // Radius of the case corner
    CASE_CORNER_R = 5;
    PCB_THICKNESS = 1.6;
    SCREW_HEAD_GAP = 3;
    SCREW_HEAD_R = 3;

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
        mirror4()                                                                    //
            translate([ -blen / 2 + offset, -bwidth / 2 + offset, -SCREW_HEAD_GAP ]) //
            cylinder(h = SCREW_HEAD_GAP *2, r = SCREW_HEAD_R);
    }

    module mountingStandoffs(blen, bwidth, offset, d, height)
    {
        // The real radius gets put in during voids
        color("red") mirror4() translate([ -blen / 2 + offset, -bwidth / 2 + offset, 0 ]) tube(d + 2, .1, height);
    }

    module bodyVoids()
    {
        mountingHoles(BOARD_LEN, BOARD_WIDTH, MOUNTING_HOLE_OFFSET, STANDOFF_HOLE_HEIGHT);
    }

    module line(x1, y1, x2, y2)
    {
        hull()
        {
            translate([
                x1,
                y1,
            ]) cube(2);
            translate([
                x2,
                y2,
            ]) cube(2);
        }
    }

    module standOffs()
    {

        $fa = 1;
        $fs = 1;

        for (standoff = keyStandoffs)
        {
            x = standoff[0];
            y = standoff[1];

            color("black") translate([ x, y, 0 ])
            {
                cylinder(r = STANDOFF_HOLE_OUTER_DIAMETER / 2, h = STANDOFF_HOLE_HEIGHT);
                cylinder(r1 = STANDOFF_HOLE_INNER_DIAMETER / 2, r2 = (STANDOFF_HOLE_INNER_DIAMETER / 2) * .9,
                         h = STANDOFF_HOLE_HEIGHT + PCB_THICKNESS);
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

            color("green") translate(v = [ cx, cy, 0 ]) linear_extrude(height = 2)
                text(label, valign = "center", halign = "center", size = 9);
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
            CASE_BORDER = 0;
            color("cyan") bottomCase(BOARD_LEN, BOARD_WIDTH, 0, CASE_HEIGHT);
            translate([ 0, 0, -BASE_THICKNESS ]) centerCubeXy(BOARD_LEN, BOARD_WIDTH, CASE_HEIGHT * 3);
        }

        // Add a little to the size to make sure it properly interfaces with the edge
        color("white") translate([ 0, 0, -BASE_THICKNESS ])
            centerCubeXy(BOARD_LEN + 1, BOARD_WIDTH + 1, BASE_THICKNESS + 1);

        translate([ 0, 0, BASE_THICKNESS ]) centerChildren()
        {
            standOffs();
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

            //       translate([ -BOARD_WIDTH / 2, -500, -500 ]) cube([ 1000, 1000, 1000 ]);
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

    module getCuts(path, len3, width)
    {

        echo(str("path ", path));

        if (len(path) == 0 || path[0] == undef)
        {
            keyboardCaseBottom();
        }
        else
        {
            head = path[0];
            tail = partial(path, 1, len(path) - 1);

            echo(str("head ", head));
            echo(str("tail ", tail));

            ll = len(path) == 1 ? len3 : len3 / (2 * len(path) - 1);

            cutIt(head, ll, BOARD_WIDTH) //
                split()                  //
                getCuts(tail, len3, width);
        }
    }

    module main2()
    {
        //  translate([ 0, 400, 0 ]) cutIt("r", BOARD_LEN, BOARD_WIDTH) split();

        //      translate([ 0, 0, -40 ]) getCuts([], BOARD_LEN, BOARD_WIDTH);

        translate([ 0, 0, 0 ]) getCuts([ "l", "l" ], BOARD_LEN, BOARD_WIDTH);

        *translate([ 0, 0, -20 ]) cutIt("l", BOARD_LEN, BOARD_WIDTH) split() keyboardCaseBottom();

        *cutIt("l", BOARD_LEN / 2, BOARD_WIDTH) //
            split()                             //
            cutIt("l", BOARD_LEN, BOARD_WIDTH)  //
            split()                             //
            keyboardCaseBottom();
    }

    main2();

    lst = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]; // a list of numbers
    lst2 = [ "red", "yellow", "blue" ];  // a list of strings
    lst3 = [ false, true, undef ];       // a list of booleans

    // https://eribuijs.blogspot.com/2017/10/openscad-lists-and-list-manipulation.html

    echo(partial(lst, 1, 8));
}