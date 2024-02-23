

print_target = "fdm"; // "fdm"; // "resin"
print_sideways = false;
atari_front_graphic_outset = true;
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

