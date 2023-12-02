#!/usr/bin/env python

from pathlib import Path
from dataclasses import dataclass
from typing import List
from process_keyboard import ProcessConfiguration
from process_keyboard import ProcessKeyboard
import sys, getopt


def getProcessConfiguration():
    base_path = Path("../keyboards/atari-a8")

    config = ProcessConfiguration()

    # Master input file, source of all truth.
    config.kle_layout_filename = base_path / "keyboard-layout.json"

    config.qmk_layout_filename = base_path / "qmkinfo.json"

    config.pcb_filename = base_path / "kicad" / "atari-keyboard.kicad_pcb"
    config.keyboard_sch_sheet_filename_name = base_path / "kicad" / "keyboard.kicad_sch"

    config.openscad_position_filename = base_path / "keycaps" / "keyboard-position.scad"
    config.case_filename = base_path / "case" / "case-position.scad"
    config.jlc_bom_filename = base_path / "kicad" / "gerbers" / "jlc_bom.csv"
    config.jlc_cpl_filename = base_path / "kicad" / "gerbers" / "jlc_cpl.csv"

    config.kicad_3dmodel_path_str = str(Path("..") / ".." / "kicad-lib" / "3d-models")
    config.kicad_keycap_vrml_path_str = str(
        Path("..") / "keycaps" / "keycap-models" / "vrml"
    )
    config.json_path_to_qmk_layout = "layouts.LAYOUT.layout"

    return config


def schematic():
    config = getProcessConfiguration()
    process = ProcessKeyboard(config)
    process.run_wrapped(
        [
            # process.log_symbols,
            process.clear_schematic,
            process.add_schematic_lib_symbols,
            process.add_schematic_connections,
        ]
    )


def pcb():
    config = getProcessConfiguration()
    process = ProcessKeyboard(config)

    process.run_wrapped(
        [
            process.relocate_parts_and_draw_silkscreen,
            process.calc_pick_n_place,
            process.make_openscad_config_file,
            process.make_jlc_pcb_assembly_files,
            process.add_3d_models_to_pcb,
            process.generate_openscad_case_file,
        ]
    )


def main(argv: List[str]):
    config = getProcessConfiguration()
    process = ProcessKeyboard(config)

    run_schematic = False
    run_pcb = False

    opts, args = getopt.getopt(argv, "hsp", ["schematic", "pcb"])
    for opt, arg in opts:
        if opt == "-h":
            print("atari_a8.py [-s|--schematic] to update the schematic")
            print(
                "  This places schematic symbols according to the qmk_info.json file (for the matrix)"
            )
            print("  and the keyboard_layout.json for the footprints and key names.")

            print(
                "atari_a8.py [-p|--pcb] arrange the footprints on the PCB (keyboard_layout.json)"
            )
            print(
                "  Note: This does not ADD the footprints to the PCB.  If the schematic changes, delete all"
            )
            print(
                "  all non-locked footprints and manually re-add them in kicad. THEN run this."
            )
            sys.exit()
        elif opt in ("-s", "--schematic"):
            run_schematic = True
        elif opt in ("-p", "--pcb"):
            run_pcb = True

    if run_schematic == False and run_pcb == False:
        print("Nothing to do")
        sys.exit()

    if run_schematic and run_pcb:
        print("Can't do the schematic and PCB in one pass")
        sys.exit()

    if run_pcb:
        print("Updating the PCB")
        pcb()

    if run_schematic:
        print("Updating the schematic")
        schematic()


if __name__ == "__main__":
    main(sys.argv[1:])
