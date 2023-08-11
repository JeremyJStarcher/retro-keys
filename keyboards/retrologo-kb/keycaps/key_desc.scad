include <../../openscad/KeyV2/includes.scad>
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
    flegend("SHIFT", [0,0], long_size)
    oem_row(4)
    preKey()
    key();
}

module key_z() {
    tu(KEY_Z)
    graphicsKey(1, "Z", "ctrl-z") {
    }
}

module key_x() {
    tu(KEY_X)
    graphicsKey(1, "X", "ctrl-x") {
    }
}


module key_c() {
    tu(KEY_C)
    graphicsKey(1, "C", "ctrl-c") {
    }
}

module key_v() {
    tu(KEY_V)
    graphicsKey(1, "V", "ctrl-v") {
    }
}

module key_b() {
    tu(KEY_B)
    graphicsKey(1, "B", "ctrl-b") {
    }
}

module key_n() {
    tu(KEY_N)
    graphicsKey(1, "N", "ctrl-n") {
    }
}


module key_m() {
    tu(KEY_M)
    graphicsKey(1, "M", "ctrl-m") {
    }
}


module key_comma() {
    tu(KEY_COMMA)
    graphicsKey(1, ",",  "ctrl-comma") {
    }
}

module key_period() {
    tu(KEY_PERIOD)
    graphicsKey(1, ".", "ctrl-period"){
    }
}

module key_slash() {
    tu(KEY_SLASH)
    graphicsKey(1, "/",  "ctrl-period");
}

module key_rshift() {
    tu(KEY_RSHIFT)
    u(1.75)
    flegend("SHIFT", [0,0], long_size)
    oem_row(1)
    preKey()
    key();
}


/// ROW 3


module key_control() {
    tu(KEY_CONTROL)
    u(2)
    stabilized()
    flegend("CONTROL", [0,0], long_size)
    oem_row(1)
    preKey()
    key();
}

module key_a() {
    tu(KEY_A)
    graphicsKey(1, "A", "ctrl-a") {
    }
}

module key_s() {
    tu(KEY_S)
    graphicsKey(1, "S", "ctrl-s") {
    }
}

module key_d() {
    tu(KEY_D)
    graphicsKey(1, "D", "ctrl-d") {
    }
}

module key_f() {
    $key_bump = true;

    tu(KEY_F)
    graphicsKey(1, "F", "ctrl-f") {
    }
}

module key_g() {
    tu(KEY_G)
    graphicsKey(1, "G", "ctrl-g") {
    }
}

module key_h() {
    tu(KEY_H)
    graphicsKey(1, "H", "ctrl-h") {
    }
}

module key_j() {
    $key_bump = true;

    tu(KEY_J)
    graphicsKey(1, "J", "ctrl-j") {
    }
}

module key_k() {
    tu(KEY_K)
    graphicsKey(1, "K", "ctrl-k") {
    }
 }

module key_l() {
    tu(KEY_L)
    graphicsKey(1, "L", "ctrl-l") {
    }
}

module key_semi() {
    tu(KEY_SEMI)
    graphicsKey(1, ";", "ctrl-semi"){
    }
}


module key_plus() {
    tu(KEY_PLUS)
    graphicsKey1(3, "+", chr(34), ARROW_LEFT, "ctrl-comma");
}


module key_astrix() {
    tu(KEY_ASTRIX)
    graphicsKey(1, "*",  "ctrl-comma");
}


module key_caps() {
    tu(KEY_CAPS)
    u(1.25)
    flegend("CAPS", [0,0], long_size)
    oem_row(1)
    preKey()
    key();
}

// ← ↑ ↓ →

// ROW 2

module key_tab() {
    tu(KEY_TAB)
    u(1.75)
    flegend("TAB", [0,1], long_size)
    flegend("CLR", [1,-1], long_size)
    flegend("SET", [-1,-1], long_size)
    oem_row(1)
    preKey()
    key();
}

module key_q() {
    tu(KEY_Q)
    graphicsKey(1, "Q", "ctrl-q") {
    }
}

module key_w() {
    tu(KEY_W)
    graphicsKey(1, "W", "ctrl-w") {
    }
}

module key_e() {
    tu(KEY_E)
    graphicsKey(1, "E", "ctrl-e") {
    }
}

module key_r() {
    tu(KEY_R)
    graphicsKey(1, "R", "ctrl-e") {
   }
}

module key_t() {
    tu(KEY_T)
    graphicsKey(1, "T", "ctrl-t") {
    }
}

module key_y() {
    tu(KEY_Y)
    graphicsKey(1, "Y", "ctrl-y") {
    }
}

module key_u() {
    tu(KEY_U)
    graphicsKey(1, "U", "ctrl-u") {
    }
}

module key_i() {
    tu(KEY_I)
    graphicsKey(1, "I", "ctrl-i") {
    }
}

module key_o() {
    tu(KEY_O)
    graphicsKey(1, "O", "ctrl-i") {
    }
}

module key_p() {
    tu(KEY_P)
    graphicsKey(1, "P", "ctrl-p") {
    }
}


// ← ↑ ↓ →
module key_dash() {
    tu(KEY_DASH)
    graphicsKey(1, "-",  "ctrl-comma");
}

module key_equal() {
    tu(KEY_EQUAL)
    graphicsKey(1, "=",  "ctrl-comma");
}


module key_return() {
    tu(KEY_RETURN)
    u(1.5)
    flegend("RETURN", [0,0], long_size)
    oem_row(1)
    preKey()
    key();
}

//////////////////////////////////////

module key_esc() {
    tu(KEY_ESC)
    u(1.25)
    flegend("ESC", [0,0], long_size)
    oem_row(1)
    preKey()
    key();
}

module key_1() {
    tu(KEY_1)
    graphicsKey(1, "1", "ctrl-comma");
}

module key_2() {
    tu(KEY_2)
    graphicsKey(1, "2",  "ctrl-comma");
}

module key_3() {
    tu(KEY_3)
    graphicsKey(1, "3", "ctrl-comma");
}

module key_4() {
    tu(KEY_4)
    graphicsKey(1, "4",  "ctrl-comma");
}

module key_5() {
    tu(KEY_5)
    graphicsKey(1, "5",  "ctrl-comma");
}

module key_6() {
    tu(KEY_6)
    graphicsKey(1, "6",  "ctrl-comma");
}

module key_7() {
    tu(KEY_7)
    graphicsKey(1, "7",  "ctrl-comma");
}

module key_8() {
    tu(KEY_8)
    graphicsKey(1, "8", "ctrl-comma");
}

module key_9() {
    tu(KEY_9)
    graphicsKey(1, "9",  "ctrl-comma");
}

module key_0() {
    tu(KEY_0)
    graphicsKey(1, "0",  "ctrl-comma");
}


module key_lt() {
    tu(KEY_LT)
    graphicsKey(1, "<",  "ctrl-comma");
}

module key_gt() {
    tu(KEY_GT)
    graphicsKey(1, ">",  "ctrl-comma");
}

module key_bs() {
    tu(KEY_BS)
    u(2)
    stabilized()
    flegend("BACK SP", [0,1], half_size)
    flegend("DELETE", [0,-1], half_size)
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
    gridKey("POWER");
}


/////////////////////////////////////
module key_space() {
    $inverted_dish = $dish_type != "disable";
    $dish_type = $dish_type != "disable" ? "sideways cylindrical" : "disable";

    tu(KEY_SPACE)
    u(6.25) stabilized(mm=50)
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
