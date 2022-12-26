from process_keyboard import ProcessConfiguration
from process_keyboard import ProcessKeyboard

if __name__ == "__main__":
    config = ProcessConfiguration()
    config.qmk_layout_filename = (
        "/home/jjs/Projects/qmk/qmk_firmware_a8/keyboards/atari_a8/info.json"
    )

    config.pcb_filename = "../keyboards/atari-a8/kicad/atari-keyboard.kicad_pcb"
    config.keyboard_sch_sheet_filename_name = (
        "../keyboards/atari-a8/kicad/keyboard.kicad_sch"
    )
    config.openscad_position_filename = (
        "../keyboards/atari-a8/keycaps/keyboard-position.scad"
    )

    config.jlc_bom_filename = "../keyboards/atari-a8/kicad/gerbers/jlc_bom.csv"
    config.jlc_cpl_filename = "../keyboards/atari-a8/kicad/gerbers/jlc_cpl.csv"
    config.matrix_starting_index = 201

    # Paths relative to the KiCad project
    config.kicad_3dmodel_path = "../../kicad-lib/3d-models/"
    config.kicad_keycap_vrml_path = "../keycaps/vrml/"

    process = ProcessKeyboard(config)

    process.run_it()
    process.calcPnP()
    process.makeOpenScad()
    process.makeJlcPcb()
    process.setModels()
