from pathlib import Path
from dataclasses import dataclass
from process_keyboard import ProcessConfiguration
from process_keyboard import ProcessKeyboard


if __name__ == "__main__":
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

    process = ProcessKeyboard(config)

    process.run_wrapped(
        [
            process.add_schematic_lib_symbols,
            process.add_keyswitches_to_schematic,
        ]
    )

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
