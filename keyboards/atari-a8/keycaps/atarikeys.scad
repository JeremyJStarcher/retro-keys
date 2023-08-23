include <../../openscad/KeyV2/includes.scad>
include <key_include.scad>


supportThicknes = 2;

module maybe_sideways() {
    if (print_sideways) {
        sideways() children();
    } else {
        children();
    }
}

module preKey(size, w2, h2)
{
    //$font="DejaVu Sans Mono:style=Book";
    // $font = "Liberation Mono:style=Bold";
    $font = "DejaVu Sans Mono:style=Book";

    // $support_type = "bars"; // [flared, bars, flat, disable]

    // FOR ON THE SIDE $stem_support_type = print_target == "fdm" ? "brim" : "brim";

    // $stem_support_type = "brim"; // [tines, brim, disabled]

    // For FDM printers the stem has to reach the print bed
    // or support issues get ... "strange."
    $stem_inset = print_target == "fdm" ? -0 : $stem_inset;

    // Rotate and then generate the key
    rotate([ atari_rotation, 0, 0 ])
    {
        maybe_sideways()
        children();
    }

    // The supports work by placing to points and drawing a line
    // between them.  (IE, wrapping a hull around them.)
    // The first point goes on the "sink" plane, the other point goes
    // on the plane where the rotated key now sits on.

    // Size of the key -- may be overwritten
    w = w2 == undef ? total_key_width() : w2;
    h = h2 == undef ? total_key_height() : h2;

    // Thickness of the walls -- may be overwritten
    thick = size == undef ? $wall_thickness : size;

    // Spacing between supports. Found by trail and error.
    spacing = 7;

    // Shorthand values for easy of use.
    rr1 = support_r1 / 2;
    rr2 = support_r2 / 2;

    
    module supportHeight(a, offset)
    {
        hull()
        {
            rotate([ atari_rotation, 0, 0 ])
            translate([ offset, a, 0 ])
            cube([ rr1 + thick, supportThicknes, 0.25 ]);

            translate([ offset, a, sink ]) 
            cube([ rr2 + thick, supportThicknes, 0.25 ]);
        }
        // foot(offset, a);
    }

    module supportWidth(a, offset)
    {

        hull()
        {
            tt = .25;
            
            rotate([ atari_rotation, 0, 0 ]) translate([ a, offset, 0 ]) 
            cube([ supportThicknes, rr1 + thick, tt ]);

            translate([ a, offset, sink ])
            cube([ supportThicknes, rr2 + thick, tt ]);
        }

       // foot(a, offset);
    }

    module supportWidth2(a, offset)
    {
        oversize = 5;
        resin_support = 7;

        translate([ a * .9, 0, -h ])
        {
            cube([ rr1*5, resin_support, h / 2 + 1 ]);
            translate([ -oversize / 2, -oversize / 2, 0 ]) cube([ rr1 + oversize, resin_support + oversize, 0.25 ]);
        }
    }

    // Print supports of the part is standing straight up and down
    if (print_target != "fdm" && false)
    {
        for (a = [-w / 2:spacing*2:w / 2])
        {
            color("white") supportWidth2(a, 0);
        }
    }

    // supports if the part is at an angle
    if (print_target != "fdm" && true)
    {
        for (a = [-h / 2:spacing:h / 2])
        {
            color("red") supportHeight(a, -w / 2 + rr1);
            color("black") supportHeight(a, w / 2 - rr1 - thick);
        }

        for (a = [-w / 2:spacing:w / 2])
        {
            color("white") supportWidth(a, -h / 2 + rr1);
            color("blue") supportWidth(a, h / 2 - rr1 - thick);
        }

        for (s = $stabilizers)
        {
            support_stabilizers(s[0], s[1]);
        }
        support_stabilizers(0, 0);

        // Make the "base" for the keys to adhere to the bed.
        color("lavender") translate([ -w / 2, -h / 2, sink ]) cube([ w, h, base_height ]);
    }
}

module foot(x, y)
{
    translate([ x, y, sink ]) cylinder(h = base_height, r = 1);
}

module support_stabilizers(x, y)
{
    // Offset for the supports
    ox = 2.5;
    oy = 1.5;
    sup_len = 3;

    for (m = [0:1:1])
        mirror([ m, 0, 0 ]) hull() for (m1 = [0:1:1]) mirror([ 0, m1, 0 ])
        {
            hull()
            {
                translate([ x + ox, y + oy, sink ]) cube([ support_r2, sup_len, 0.25 ]);

                translate([ x + ox, y + oy, 2 ]) cube([ support_r2, sup_len, 0.25 ]);
            }

            // translate([ox, oy, 0])
            // foot(x, y);
        }
}

module frontGraphicOutset()
{
    if ($show_legend && atari_front_graphic_outset)
    {
        // this value by trial and error
        inset = -0.2;

        maybe_sideways()
        rotate([ atari_rotation, 0, 0 ]) front_of_key() translate([ 0, inset, 0 ]) scale([ 0.75, 0.25, 0.75 ])
        {
            boundBox();
            color("red") children();
        }
    }
}


module frontGraphicCutout()
{
    if ($show_legend && !atari_front_graphic_outset)
    {
        // this value by trial and error
        inset = -0.2;


        ALL_THE_WAY_THROUGH = 3;
        PART_WAY_THROUGH = 2;

        THROUGH_SIZE = PART_WAY_THROUGH; 
 
        maybe_sideways()
        rotate([ atari_rotation, 0, 0 ]) front_of_key() translate([ 0, inset, 0 ]) scale([ 0.75, ALL_THE_WAY_THROUGH, 0.75 ])
        {
            boundBox();
            color("white") children();
        }
    }
}

module arrowKey(row, legend, svg)
{
    difference()
    {
        u(1) flegend(legend, POS_1_OF_1, arrow_size) oem_row(row) preKey() key();

        frontGraphicCutout() children();
    }

    frontGraphicOutset() children();
}

module graphicsKey(row, legend, svg)
{
    difference()
    {
        u(1) flegend(legend, POS_1_OF_1, full_size) oem_row(row) preKey() key();

        frontGraphicCutout() children();
    }

    frontGraphicOutset() children();
}

module graphicsKey2(row, legendBottom, legendTop, svg)
{
    difference()
    {
        u(1) flegend(legendBottom, POS_1_OF_2, half_size) 
        flegend(legendTop, POS_2_OF_2, half_size) oem_row(row) preKey()
            key();

        frontGraphicCutout() children();
    }
    frontGraphicOutset() children();
}

module graphicsKey3(row, legendBottom, legendTop, legendLeft, svg)
{
    difference()
    {
        u(1) flegend(legendBottom, POS_1_OF_3, half_size)
         flegend(legendTop, POS_2_OF_3, half_size)
            flegend(legendLeft, POS_3_OF_3, arrow_size) oem_row(row) preKey() key();

        frontGraphicCutout() children();
    }
    frontGraphicOutset() children();
}

gCut = 2;
module boundBox()
{
    * difference()
    {
        cube([ 10, gCut, 10 ], center = true);
        cube([ 8, gCut, 8 ], center = true);
    }
}


/*
 * These are used for drawing a bunch of the graphics characters.
 *
 * Picture a clock face.  gLine6 draws from the center of the grid
 * to the 6 o'clock position (or down)
 */

module gLine6()
{
    translate([ 0, 0, -2 ]) cube([ 2, gCut, 6 ], center = true);
}

module gLine12()
{
    translate([ 0, 0, 2 ]) cube([ 2, gCut, 6 ], center = true);
}

module gLine3()
{
    translate([ +2, 0, 0 ]) cube([ 6, gCut, 2 ], center = true);
}

module gLine9()
{
    translate([ -2, 0, 0 ]) cube([ 6, gCut, 2 ], center = true);
}

module gLineLeft()
{
    translate([ -3, 0, 0 ]) cube([ 2, gCut, 8 ], center = true);
}

module gLineRight()
{
    translate([ 3, 0, 0 ]) cube([ 2, gCut, 8 ], center = true);
}

module gLineBottom()
{
    translate([ 0, 0, -3 ]) cube([ 8, gCut, 2 ], center = true);
}

module gLineTop()
{
    translate([ 0, 0, 3 ]) cube([ 8, gCut, 2 ], center = true);
}

module gCharacter(t)
{
    translate([ 0, 1, 0 ]) rotate([ 90, 0, 0 ]) linear_extrude(height = gCut)
        text(text = t, size = 8, valign = "center", halign = "center");
}

module gridKey(legend)
{
    preKey(size = 1.75, w2 = 19.5 + 3, h2 = 19.5 + 3) gridKeyRender(legend);
}

module gridKeyRender(legend)
{
    // The walls are WAY too thin by default and I couldn't find
    // a parameter setting that would thicken the walls on these kinds of
    // buttons, so we will manually re-enforce the button ourselves.
    //
    // Slows down processing time, but -- eh --

    usize = 1.25;
    uhsize = 1.25;

    module key1()
    {
        u(usize) uh(uhsize) flegend(legend, POS_GRID_KEY, grid_key_size) grid_row(1) key();
    }

    hh = 6;
    w = total_key_width();
    h = total_key_height();

    // Draw the re-enforced walls
    color("cyan") difference()
    {
        hull() intersection()
        {
            key1();
            translate([ -50, -50, 0 ]) cube([ 100, 100, hh ]);
        }

        cube([ w, h, hh * 5 ], center = true);
    }

    // Then draw the button itself (which will redraw the thin walls)
    key1();
}

module flegend(txt, pos, size)
{
    if ($show_legend)
    {
        // s$inset_legend_depth = 100.2;

        legend(txt, pos, size) children();
    }
    else
    {
        legend("", pos, size) children();
    }
}

//  fullkeyboard();

// key_z();

if (false)
{
    key_space();
    key_c_up();
    key_c_down();
    key_c_left();
    key_c_right();
    key_fn();
}