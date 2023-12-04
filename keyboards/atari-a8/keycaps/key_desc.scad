

include <../../openscad//KeyV2/includes.scad>
include <atarikeys.scad>
use <key_include.scad>
include <keyboard-position.scad>


ARROW_UP = "↑";
ARROW_LEFT = "←";
ARROW_DOWN =  "↓";
ARROW_RIGHT =  "→";


/// ROW 4

module tu(a) {
    if ($set_location) {
        // translate_u(a[0], -a[1]) children();
        translate([a[2], -a[3], 0]) children();
    } else {
        children();
    }
}


module key_lshift() {
    tu(KEY_LSHIFT)
    u(2.25)
    stabilized()
    flegend("SHIFT", POS_1_OF_1, long_size)
    oem_row(4)
    preKey()
    key();
}

module key_z() {
    tu(KEY_Z)
    graphicsKey(4, "Z", "ctrl-z") {
        gLine12();
        gLine3();
    }
}

module key_x() {
    tu(KEY_X)
    graphicsKey(4, "X", "ctrl-x") {
        gLine9();
        gLine3();
        gLine12();
    }
}


module key_c() {
    tu(KEY_C)
    graphicsKey(4, "C", "ctrl-c") {
        gLine9();
        gLine12();
    }
}

module key_v() {
    tu(KEY_V)
    graphicsKey(4, "V", "ctrl-v") {
        gLineLeft();
    }
}

module key_b() {
    tu(KEY_B)
    graphicsKey(4, "B", "ctrl-b") {
        gLineRight();
    }
}

module key_n() {
    tu(KEY_N)
    graphicsKey(4, "N", "ctrl-n") {
        gLineBottom();
    }
}


module key_m() {
    tu(KEY_M)
    graphicsKey(4, "M", "ctrl-m") {
        gLineTop();
    }
}


module key_comma() {
    tu(KEY_COMMA)
    graphicsKey2(4, ",", "[", "ctrl-comma") {
        gCharacter("♥");
    }
}

module key_period() {
    tu(KEY_PERIOD)
    graphicsKey2(4, ".", "]", "ctrl-period"){
        gCharacter("♦");
    }
}

module key_slash() {
    tu(KEY_SLASH)
    graphicsKey2(4, "/", "?", "ctrl-period");
}

module key_rshift() {
    tu(KEY_RSHIFT)
    u(1.75)
    flegend("SHIFT", POS_1_OF_1, long_size)
    oem_row(4)
    preKey()
    key();
}


/// ROW 3


module key_control() {
    tu(KEY_CONTROL)
    u(2)
    stabilized()
    flegend("CONTROL", POS_1_OF_1, long_size)
    oem_row(3)
    preKey()
    key();
}

module key_a() {
    tu(KEY_A)
    graphicsKey(3, "A", "ctrl-a") {
        gLine6();
        gLine12();
        gLine3();
    }
}

module key_s() {
    tu(KEY_S)
    graphicsKey(3, "S", "ctrl-s") {
        gLine6();
        gLine12();
        gLine3();
        gLine9();
    }
}

module key_d() {
    tu(KEY_D)
    graphicsKey(3, "D", "ctrl-d") {
        gLine6();
        gLine12();
        gLine9();
    }
}

module key_f() {
    $key_bump = true;

    tu(KEY_F)
    graphicsKey(3, "F", "ctrl-f") {
        hull() {
        translate([3, -1, 3])
        cube([1, gCut, 1]);

        translate([-4, -1, -4])
        cube([1, gCut, 1]);
        }
    }
}

module key_g() {
    tu(KEY_G)
    graphicsKey(3, "G", "ctrl-g") {
        hull() {
        translate([-4, -1, 3])
        cube([1, gCut, 1]);

        translate([3, -1, -4])
        cube([1, gCut, 1]);
        }
    }
}

module key_h() {
    tu(KEY_H)
    graphicsKey(3, "H", "ctrl-h") {
        hull() {
            translate([4, -1, 4])
            cube([.1, gCut, .1]);

            translate([-4, -1, -4])
            cube([.1, gCut, .1]);

            translate([3, -1, -4])
            cube([1, gCut, 1]);
        }
    }
}

module key_j() {
    $key_bump = true;

    tu(KEY_J)
    graphicsKey(3, "J", "ctrl-j") {
        hull() {
            translate([-4, -1, 4])
            cube([.1, gCut, .1]);

            translate([4, -1, -4])
            cube([.1, gCut, .1]);

            translate([-4, -1, -4])
            cube([1, gCut, 1]);
        }
    }
}

module key_k() {
    tu(KEY_K)
    graphicsKey(3, "K", "ctrl-k") {
        translate([0, -1, 0])
        cube([4, gCut, 4]);
    }
 }

module key_l() {
    tu(KEY_L)
    graphicsKey(3, "L", "ctrl-l") {
        translate([-4, -1, 0])
        cube([4, gCut, 4]);
    }
}

module key_semi() {
    tu(KEY_SEMI)
    graphicsKey2(3, ";", ":", "ctrl-semi"){
        gCharacter("♠️");
    }
}


module key_plus() {
    tu(KEY_PLUS)
    graphicsKey3(3, "+", chr(92), ARROW_LEFT, "ctrl-comma");
}


module key_astrix() {
    tu(KEY_ASTRIX)
    graphicsKey3(3, "*", "^", ARROW_RIGHT, "ctrl-comma");
}


module key_caps() {
    tu(KEY_CAPS)
    u(1.25)
    flegend("CAPS", POS_1_OF_1, long_size)
    oem_row(3)
    preKey()
    key();
}

// ← ↑ ↓ →

// ROW 2

module key_tab() {
    tu(KEY_TAB)
    u(1.75)
    flegend("TAB", POS_S, long_size)
    flegend("CLR", POS_NW, long_size)
    flegend("SET", POS_NE, long_size)
    oem_row(2)
    preKey()
    key();
}

module key_q() {
    tu(KEY_Q)
    graphicsKey(2, "Q", "ctrl-q") {
       gLine3();
       gLine6();
    }
}

module key_w() {
    tu(KEY_W)
    graphicsKey(2, "W", "ctrl-w") {
       gLine3();
       gLine6();
       gLine9();
    }
}

module key_e() {
    tu(KEY_E)
    graphicsKey(2, "E", "ctrl-e") {
       gLine6();
       gLine9();
    }
}

module key_r() {
    tu(KEY_R)
    graphicsKey(2, "R", "ctrl-e") {
       gLine9();
       gLine3();
   }
}

module key_t() {
    tu(KEY_T)
    graphicsKey(2, "T", "ctrl-t") {
        translate([0, 1, 0])
        rotate([90, 0, 0])
        cylinder(h = gCut, r = 3);
    }
}

module key_y() {
    tu(KEY_Y)
    graphicsKey(2, "Y", "ctrl-y") {
        translate([-4, -1, -4])
        cube([4, gCut, 8]);
    }
}

module key_u() {
    tu(KEY_U)
    graphicsKey(2, "U", "ctrl-u") {
        translate([-4, -1, -4])
        cube([8, gCut, 4]);
    }
}

module key_i() {
    tu(KEY_I)
    graphicsKey(2, "I", "ctrl-i") {
        translate([0, -1, -4])
        cube([4, gCut, 4]);
    }
}

module key_o() {
    tu(KEY_O)
    graphicsKey(2, "O", "ctrl-i") {
        translate([-4, -1, -4])
        cube([4, gCut, 4]);
    }
}

module key_p() {
    tu(KEY_P)
    graphicsKey(2, "P", "ctrl-p") {
        gCharacter("♣️");
    }
}


// ← ↑ ↓ →
module key_dash() {
    tu(KEY_DASH)
    graphicsKey3(2, "-", "_", ARROW_UP, "ctrl-comma");
}

module key_equal() {
    tu(KEY_EQUAL)
    graphicsKey3(2, "=", "|", ARROW_DOWN, "ctrl-comma");
}


module key_return() {
    tu(KEY_RETURN)
    u(1.5)
    flegend("RETURN", POS_1_OF_1, long_size)
    oem_row(2)
    preKey()
    key();
}

//////////////////////////////////////

module key_esc() {
    tu(KEY_ESC)
    u(1.25)
    flegend("ESC", POS_1_OF_1, long_size)
    oem_row(1)
    preKey()
    key();
}

module key_1() {
    tu(KEY_1)
    graphicsKey2(1, "1", "!", "ctrl-comma");
}

module key_2() {
    tu(KEY_2)
    graphicsKey2(1, "2", "\"", "ctrl-comma");
}

module key_3() {
    tu(KEY_3)
    graphicsKey2(1, "3", "#", "ctrl-comma");
}

module key_4() {
    tu(KEY_4)
    graphicsKey2(1, "4", "$", "ctrl-comma");
}

module key_5() {
    tu(KEY_5)
    graphicsKey2(1, "5", "%", "ctrl-comma");
}

module key_6() {
    tu(KEY_6)
    graphicsKey2(1, "6", "&", "ctrl-comma");
}

module key_7() {
    tu(KEY_7)
    graphicsKey2(1, "7", "'", "ctrl-comma");
}

module key_8() {
    tu(KEY_8)
    graphicsKey2(1, "8", "@", "ctrl-comma");
}

module key_9() {
    tu(KEY_9)
    graphicsKey2(1, "9", "(", "ctrl-comma");
}

module key_0() {
    tu(KEY_0)
    graphicsKey2(1, "0", ")", "ctrl-comma");
}


module key_lt() {
    tu(KEY_LT)
    graphicsKey2(1, "<", "CLR", "ctrl-comma");
}

module key_gt() {
    tu(KEY_GT)
    graphicsKey2(1, ">", "INS", "ctrl-comma");
}

module key_bs() {
    tu(KEY_BS)
    u(2)
    stabilized()
    flegend("BACK SP", POS_TEXT_1_OF_2, half_size)
    flegend("DELETE", POS_2_OF_2, half_size)
    oem_row(1)
    preKey()
    key();
}

/////////////////


module key_reset() {
    tu(KEY_RESET)
    gridKey("RESET");
}

module key_menu() {
    tu(KEY_MENU)
    gridKey("MENU");
}

module key_turbo() {
    tu(KEY_TURBO)
    gridKey("TURBO");
}

module key_start() {
    tu(KEY_START)
    gridKey("START");
}

module key_select() {
    tu(KEY_SELECT)
    gridKey("SELECT");
}

module key_option() {
    tu(KEY_OPTION)
    gridKey("OPTION");
}

module key_help() {
    tu(KEY_HELP)
    gridKey("HELP");
}

module key_inv() {
    tu(KEY_INV)
    gridKey("INV");
}

module key_break() {
    tu(KEY_BREAK)
    gridKey("BREAK");
}

module key_power() {
    tu(KEY_POWER)
    // gridKey("POWER");

    graphicsKey(2, "PWR", "ctrl-p") {
        gCharacter("");
    }

}


/////////////////////////////////////
module key_space() {
    $inverted_dish = $dish_type != "disable";
    $dish_type = $dish_type != "disable" ? "sideways cylindrical" : "disable";

    tu(KEY_SPACE)
    u(6.25) stabilized(mm=50)
    preKey()
    key();
}


module key_c_up() {
    tu(KEY_C_UP)
    arrowKey(2, ARROW_UP, "ctrl-y");
}

module key_c_left() {
    tu(KEY_C_LEFT)
    arrowKey(2, ARROW_LEFT, "ctrl-y");
}

module key_c_down() {
    $key_bump = true;
    tu(KEY_C_DOWN)
    arrowKey(2, ARROW_DOWN, "ctrl-y");
 }

module key_c_right() {
    tu(KEY_C_RIGHT)
    arrowKey(2, ARROW_RIGHT, "ctrl-y");
 }


module key_fn() {
    tu(KEY_FN)
    graphicsKey2(1, "FN", "", "ctrl-y");
}


module fullkeyboard() {
    if (true) {
        key_lshift();
        key_z();
        key_x();
        key_c();
        key_v();
        key_b();
        key_n();
        key_m();
        key_comma();
        key_period();
        key_slash();
        key_rshift();
    }

    if (true) {
        key_control();
        key_a();
        key_s();
        key_d();
        key_f();
        key_g();
        key_h();
        key_j();
        key_k();
        key_l();
        key_semi();
        key_plus();
        key_astrix();
        key_caps();
    }

    if (true) {
        key_tab();
        key_q();
        key_w();
        key_e();
        key_r();
        key_t();
        key_y();
        key_u();
        key_i();
        key_o();
        key_p();
        key_dash();
        key_equal();
        key_return();
    }


    if (true) {
        key_esc();
        key_1();
        key_2();
        key_3();
        key_4();
        key_5();
        key_6();
        key_7();
        key_8();
        key_9();
        key_0();
        key_lt();
        key_gt();
        key_bs();
    }

    if (true) {
        key_reset();
        key_menu();
        key_turbo();
        key_start();
        key_select();
        key_option();
        key_help();
        key_inv();
        key_break();
    }

    if (true) {
        key_space();

        key_c_up();
        key_c_down();
        key_c_left();
        key_c_right();

        key_fn();
    }
}
