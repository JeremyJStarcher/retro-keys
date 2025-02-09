

print_target = "fdm"; // "fdm"; // "resin"
print_sideways = true;
atari_front_graphic_outset = false;
$stem_support_type = "disable";

// How far to rotate the keys when they are generated
atari_rotation = print_target == "fdm" ? 0 : 0;

// how far below the "zero line" to start making the supports.
sink = -15;
// Diamater of supports at one end
support_r1 = 0.5;
// Diamater of supports at other end
support_r2 = 0.5;

// Font size of one-letter per key
// full_size = 9;
full_size = 5;

// Font size of words written on a key
long_size = 4;
// Font size if there are multiple lines on a key.
half_size = 5; // print_target == "fdm" ? 5 : 4;
grid_key_size = 4;
arrow_size = 5;



base_height = 0.4;

$keytop_thickness = 2;


// Supports for the stem, as it often comes off during printing. Reccommended for most machines
// $stem_support_type = "tines"; // [tines, brim, disabled]
// $stem_support_type = "brim"; //  "disable"; // "disable"; // "tines"

$inset_legend_depth = 1.5;
// $clearance_check = true;


// POSITIONS FOR KEYCAPS

__POS_C = 0;
__POS_N = -1;
__POS_E = 1;
__POS_S = 1;
__POS_W = -1;

POS_C = [__POS_C, __POS_C];
POS_S = [__POS_C, __POS_S];
POS_N = [__POS_C, __POS_N];
POS_E = [__POS_E, __POS_C];
POS_W = [__POS_W, __POS_C];
POS_NW = [__POS_W, __POS_N];
POS_NE = [__POS_E, __POS_N];
POS_SE = [__POS_E, __POS_S];
POS_SW = [__POS_W, __POS_S];

POS_1_OF_1 = POS_C;
POS_1_OF_2 = POS_SW;
POS_2_OF_2 = POS_NE;

POS_1_OF_3 = POS_C;
POS_2_OF_3 = POS_SW;
POS_3_OF_3 = POS_NE;

POS_TEXT_1_OF_2 = POS_S;
POS_TEXT_2_OF_2 = POS_N;

POS_GRID_KEY = POS_C;



module local_row(row=3, column = 0) {
//module g20_row(row=3, column = 0) {
  $bottom_key_width = 18.16;
  $bottom_key_height = 18.16;
  $width_difference = 2;
  $height_difference = 2;
    
  $top_tilt = 2.5;
  $top_skew = 0.75;
  $dish_type = "disable";
//  $dish_type = "spherical";
//  $dish_type = "cylindrical";

  // something weird is going on with this and legends - can't put it below 1.2 or they won't show
  $dish_depth = 1.2;
  $dish_skew_x = 0;
  $dish_skew_y = 0;
  $minkowski_radius = 1.75;
  $key_bump_depth = 0.6;
  $key_bump_edge = 2;
  //also,
  $rounded_key = true;

  $top_tilt_y = side_tilt(column);
  //extra_height =  $double_sculpted ? extra_side_tilt_height(column) : 0;
  extra_height =  3;

  $total_depth = 6 + abs((row-3) * 0.5) + extra_height;

  if (row == 5 || row == 0) {
    $top_tilt =  -18.55;
    children();
  } else if (row == 1) {
    $top_tilt = (row-3) * 7 + 2.5;
    children();
  } else if (row == 2) {
    $top_tilt = (row-3) * 7 + 2.5;
    children();
  } else if (row == 3) {
    $top_tilt = (row-3) * 7 + 2.5;
    children();
  } else if (row == 4) {
    $top_tilt = (row-3) * 7 + 2.5;
    children();
  } else {
    children();
  }
}


module atari_row(row) {
    oem_row(row) children();
    //asa_row(row) children();
    //cherry_row(row) children();
    //dcs_row(row) children();
    //dsa_row(row) children();
    //dss_row(row) children();
    //g20_row(row) children(); // LIKE
    //grid_row(row) children(); 
    //hipro_row(row) children();
    //mt3_row(row) children();
    //regular_polygon_row(row) children();
    //sa_row(row) children();
    //typewriter_row(row) children();
    //local_row(row) children();
}
//