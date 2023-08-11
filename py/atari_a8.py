from pathlib import Path
from dataclasses import dataclass
from process_keyboard import ProcessConfiguration
from process_keyboard import ProcessKeyboard


@dataclass
class KeyboardPaths:
    base_path: Path

    def __post_init__(self):
        self.qmk_layout = self.base_path / "qmkinfo.json"
        self.raw_layout = self.base_path / "raw-layout-autogen.raw"
        self.pcb = self.base_path / "kicad" / "atari-keyboard.kicad_pcb"
        self.schematic = self.base_path / "kicad" / "keyboard.kicad_sch"
        self.openscad_position = self.base_path / "keycaps" / "keyboard-position.scad"
        self.case_position = self.base_path / "case" / "case-position.scad"
        self.jlc_bom = self.base_path / "kicad" / "gerbers" / "jlc_bom.csv"
        self.jlc_cpl = self.base_path / "kicad" / "gerbers" / "jlc_cpl.csv"
        self.kicad_3dmodel = Path("..") / ".." / "kicad-lib" / "3d-models"
        self.kicad_keycap_vrml = Path("..") / "keycaps" / "vrml"


if __name__ == "__main__":
    base_path = Path("../keyboards/atari-a8")
    paths = KeyboardPaths(base_path)

    config = ProcessConfiguration()
    config.qmk_layout_filename = paths.qmk_layout
    config.raw_layout_filename = paths.raw_layout
    config.pcb_filename = paths.pcb
    config.keyboard_sch_sheet_filename_name = paths.schematic
    config.openscad_position_filename = paths.openscad_position
    config.case_filename = paths.case_position
    config.jlc_bom_filename = paths.jlc_bom
    config.jlc_cpl_filename = paths.jlc_cpl
    config.matrix_starting_index = 201
    config.kicad_3dmodel_path_str = str(paths.kicad_3dmodel)
    config.kicad_keycap_vrml_path_str = str(paths.kicad_keycap_vrml)

    process = ProcessKeyboard(config)

    process.relocate_parts_and_draw_silkscreen()
    process.calc_pick_n_place()
    process.make_openscad_config_file()
    process.make_jlc_pcb_assembly_files()
    process.add_3d_models_to_pcb()
    process.generate_openscad_case_file()

    process.make_autogen_files()
