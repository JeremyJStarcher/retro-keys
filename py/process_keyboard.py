import json
import csv
import os
from pathlib import Path
import re
from typing import List
from common_key_format import CommonKeyData
from ki_symbols import KiSymbols
from kicad_parser import KiCadParser
from kicad_tools import KicadTool
from kicad_tools import Layer
from kicad_tools import BoundingBox
from kle_tools import KleTools
from qmk_tools import QmkTools

BASE_THICKNESS = 3

"""Make it smaller then the ACTUAL hole so our peg isn't caught"""
# STANDOFF_HOLE_INNER_DIAMETER = (2.2 * 2) * .8
STANDOFF_HOLE_INNER_DIAMETER = 3

STANDOFF_HOLE_OUTER_DIAMETER = 3 * 2
STANDOFF_HOLE_HEIGHT = 3
CASE_HEIGHT = 6
MOUNTING_HOLE_OFFSET = 5
MOUNTING_HOLE_D = 3.2


PRINTER_X = 280
PRINTER_Y = 260

class ProcessConfiguration:
    # These paths are relative to the 'py' directory
    kle_layout_filename: Path
    qmk_layout_filename: Path
    pcb_filename: Path
    case_filename: Path
    keyboard_sch_sheet_filename_name: Path
    openscad_position_filename: Path
    jlc_bom_filename: Path
    jlc_cpl_filename: Path
    json_path_to_qmk_layout: str

    # These paths are relative to the KiCad project directory
    kicad_3dmodel_path_str: str
    kicad_keycap_vrml_path_str: str

    pcb_x_orig: float = 61
    pcb_y_orig: float = 177.75
    pcb_border: float = 10

    UNIT = 19.05

    # How much to move the diodes
    diode_offset_x = 6.5
    diode_offset_y = 5.52


class KeyInfo:
    # Logoical position, based on key units
    l_x: float = 0
    l_y: float = 0

    # Absolute position
    key_x: float = 0
    key_y: float = 0
    w: float = 0
    h: float = 0
    designator: str = ""
    label: str = ""
    skip = True
    diode_x: float = 0
    diode_y: float = 0
    hole_x: float = 0
    hole_y: float = 0
    bounding_box: BoundingBox | None = None

    def __init__(self):
        self.bbox = BoundingBox(
            float("inf"), float("inf"), float("-inf"), float("-inf")
        )

    def __repr__(self):
        l = []

        l.append("label: " + str(self.label))
        l.append("designator: " + str(self.designator))
        l.append("x: " + str(self.key_x))
        l.append("y: " + str(self.key_y))
        l.append("w: " + str(self.w))
        l.append("h: " + str(self.h))

        l.append("l_x: " + str(self.l_x))
        l.append("l_y: " + str(self.l_y))

        return "{ " + ", ".join(l) + " }"


class ProcessKeyboard:
    config: ProcessConfiguration
    common_key_format: CommonKeyData = CommonKeyData()
    layout: List[KeyInfo]

    def __init__(self, config: ProcessConfiguration):
        self.config = config
        self.__populateCommonData()
        self.layout = self.__get_layout_from_kle()

    def read_sexp(self, name: Path):
        with open(name, "r") as f:
            data = f.read()
        return data

    def read_qmk_layout_from_json_file(self, name: Path) -> dict:
        with open(name, "r") as f:
            data = f.read()
        d_dict = json.loads(data)
        return d_dict

    def __populateCommonData(self) -> None:
        with open(self.config.qmk_layout_filename, "r") as qmk_data_file:

            qmk_data = qmk_data_file.read()
            qmk = json.loads(qmk_data)
            qmk_tools = QmkTools(qmk=qmk, json_path_to_qmk_layout=self.config.json_path_to_qmk_layout)  # type: ignore

            with open(self.config.kle_layout_filename, "r") as kle_data_file:
                kle_data = kle_data_file.read()
                kle = json.loads(kle_data)
                kle_tools = KleTools(kle=kle)

                self.common_key_format.update_from_kle(kle_tools)
                self.common_key_format.update_from_qmk(qmk_tools)

                self.common_key_format.convert_kle_location_to_qmk()

    def __get_bare_reference_id(self, s: str):
        """
        Strip off the prefix
        SW227
        and D227

        Both just become "227"
        """

        new_string = re.sub(r"^[a-zA-Z]+", "", s)
        return new_string

    def set_designators(self, keys: List[KeyInfo]):
        filtered = list(filter(lambda key: not key.skip, keys))

        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.to_list()

        tool = KicadTool()
        value_references = tool.get_all_symbol_value_references(schematic)

        if len(value_references.keys()) != 0:
            for item in filtered:
                references = value_references[item.label]
                item.designator = self.__get_bare_reference_id(references[0])

    def __get_layout_from_kle(self) -> List[KeyInfo]:
        keys: List[KeyInfo] = []

        KEYSWITCH_FIX_X = -11.565
        KEYSWITCH_FIX_Y = -3.946

        for key_name in self.common_key_format.get_key_names():
            key = self.common_key_format.get_from_common_keys_or_new(key_name)

            keyInfo = KeyInfo()

            keyInfo.skip = key.is_decal
            keyInfo.label = key.name

            keyInfo.w = key.w
            keyInfo.h = key.h

            xfix: float = -1
            if keyInfo.w == 1.0:
                # print("**1.0**")
                xfix = 0

            if keyInfo.w == 1.5:
                # print("**1.5**")
                xfix = 0

            if keyInfo.w == 1.25:
                # print("**1.25**")
                xfix = 0.125

            if keyInfo.w == 1.75:
                # print("**1.75**")
                xfix = 0.375

            if keyInfo.w == 2:
                # print("**2.0**")
                xfix = 0.5

            if keyInfo.w == 2.25:
                # print("**2.25**")
                xfix = 0.625

            if keyInfo.w == 6.25:
                # print("**6.250**")
                xfix = 2.625

            if xfix == -1:
                raise Exception(
                    "Unknown width of" + str(keyInfo.w) + " found " + keyInfo.label
                )

            keyInfo.l_x = key.qmk_location.x
            keyInfo.l_y = key.qmk_location.y

            x = (keyInfo.l_x + (KeyInfo.w / 2)) * self.config.UNIT
            y = (keyInfo.l_y + (KeyInfo.h / 2)) * self.config.UNIT

            x += self.config.pcb_x_orig
            y += self.config.pcb_y_orig

            ww = (keyInfo.w - 1) * self.config.UNIT
            hh = (keyInfo.h - 1) * self.config.UNIT

            # print("keyInfo: w, h", keyInfo.h, keyInfo.w, ww, hh)

            keyInfo.key_x = x + ww / 2
            keyInfo.key_y = y + hh / 2

            keyInfo.diode_x = keyInfo.key_x + self.config.diode_offset_x
            keyInfo.diode_y = keyInfo.key_y + self.config.diode_offset_y

            # The math for figuring out the actual bounding box is off, so manually correct for
            # various key sizes.  (By hand/trial and error)

            x1 = (keyInfo.key_x - keyInfo.w / 2) - ww / 2 + KEYSWITCH_FIX_X
            # y1 = (keyInfo.key_y - keyInfo.h / 2) - hh / 2 + KEYSWITCH_FIX_Y
            # x2 = x1 + self.config.UNIT + ww
            # y2 = y1 + self.config.UNIT + hh

            x1 += xfix

            keyInfo.hole_x = keyInfo.key_x + 10
            keyInfo.hole_y = keyInfo.key_y + 10

            keys.append(keyInfo)

        self.set_designators(keys)
        return keys

    def add_schematic_lib_symbols(self) -> None:
        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.to_list()
        tool = KicadTool()

        print(schematic)
        key_parser.print_list(schematic, 0)

        schematic_lib_symbols = tool.find_object_by_atom(schematic, "lib_symbols")
        schematic_symbols = tool.find_objects_by_atom(
            schematic_lib_symbols, "symbol", 1
        )
        scematic_existing_names = [x[1] for x in schematic_symbols]

        load_lib_symbols = KiSymbols.get_lib_symbols()
        load_symbols = tool.find_objects_by_atom(load_lib_symbols, "symbol", 1)
        load_incoming_names = [x[1] for x in load_symbols]

        new_names = list(set(load_incoming_names).difference(scematic_existing_names))

        for symbol in load_symbols:
            if symbol[1] in new_names:
                schematic_lib_symbols.append(symbol)

        l = key_parser.list_to_sexp(schematic)
        out = "\r\n".join(l)

        with open(self.config.keyboard_sch_sheet_filename_name, "w") as f:
            f.write(out)

    def add_keyswitches_to_schematic(self) -> None:
        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)

        key_schematic = key_parser.to_list()

        tool = KicadTool()

        matrix_min_x = 32000
        matrix_min_y = 32000
        matrix_max_x = -matrix_min_x
        matrix_max_y = -matrix_min_y

        start_base = 200

        base_designator = start_base

        tool.remove_atoms(key_schematic, "symbol")
        tool.remove_atoms(key_schematic, "wire")
        tool.remove_atoms(key_schematic, "junction")

        for key_name in self.common_key_format.get_key_names():
            key = self.common_key_format.get_from_common_keys_or_new(key_name)

            mx = int(float(key.matrix[0]))
            my = int(float(key.matrix[1]))

            matrix_max_x = max(matrix_max_x, mx)
            matrix_max_y = max(matrix_max_y, my)

            matrix_min_x = min(matrix_min_x, mx)
            matrix_min_y = min(matrix_min_y, my)

        for y in range(matrix_min_y, matrix_max_y + 1):
            for x in range(matrix_min_x, matrix_max_x + 1):

                for key_name in self.common_key_format.get_key_names():
                    key = self.common_key_format.get_from_common_keys_or_new(key_name)

                    if key.is_decal:
                        continue

                    kmx = int(float(key.matrix[1]))
                    kmy = int(float(key.matrix[0]))

                    if kmx == x and kmy == y:

                        tool.add_keyswitch_to_schematic(
                            str(base_designator),
                            key.name,
                            key_schematic,
                            x,
                            y,
                        )

                        base_designator += 1

        key_list = key_parser.list_to_sexp(key_schematic)
        key_out = "\r\n".join(key_list)

        with open(self.config.keyboard_sch_sheet_filename_name, "w") as f:
            f.write(key_out)

    def relocate_parts_and_draw_silkscreen(self) -> None:

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.to_list()

        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.to_list()

        tool = KicadTool()

        bbox = BoundingBox(-1, -1, -1, -1)

        for item in self.layout:

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            tool.set_object_location(
                pcb, "SW" + item.designator, item.key_x, item.key_y, 0
            )

            switch = tool.find_footprint_by_reference(pcb, "SW" + item.designator)
            at = tool.find_at_by_reference(pcb, "SW" + item.designator)
            tool.set_hidden_footprint_text_by_reference(
                pcb, "SW" + item.designator, "value", False
            )

            tool.move_text_to_layer(
                pcb, "SW" + item.designator, "value", Layer.F_Silkscreen
            )
            tool.copy_to_back_silkscreen(pcb, "SW" + item.designator, "value")

            item.bounding_box = tool.get_bounding_box_of_layer_lines(
                switch, Layer.User_Drawings
            )

            assert item.bounding_box is not None

            tool.add_bounding_box(pcb, item.bounding_box, 0.3, Layer.F_Silkscreen)
            tool.add_bounding_box(pcb, item.bounding_box, 0.3, Layer.B_Silkscreen)

            bbox.update_xy(item.bounding_box.x1, item.bounding_box.y1)
            bbox.update_xy(item.bounding_box.x2, item.bounding_box.y2)

            tool.set_object_location(
                pcb, "D" + item.designator, item.diode_x, item.diode_y, -90
            )

            hx, hy = self.get_standoff_location(schematic, tool, item)

            tool.draw_keepout_zone(pcb, hx, hy, STANDOFF_HOLE_OUTER_DIAMETER)
            tool.draw_circle(pcb, Layer.Edge_Cuts, hx, hy, STANDOFF_HOLE_INNER_DIAMETER)

        bbox.add_border(self.config.pcb_border)
        tool.add_bounding_box(pcb, bbox, 0.3, Layer.Edge_Cuts)

        bbox.add_border(-MOUNTING_HOLE_OFFSET)
        tool.set_object_location(pcb, "H101", bbox.x1, bbox.y1, 0)
        tool.set_object_location(pcb, "H102", bbox.x1, bbox.y2, 0)
        tool.set_object_location(pcb, "H103", bbox.x2, bbox.y1, 0)
        tool.set_object_location(pcb, "H104", bbox.x2, bbox.y2, 0)

        l = pcb_parser.list_to_sexp(pcb)
        out = "\r\n".join(l)

        with open(self.config.pcb_filename, "w") as f:
            f.write(out)

    def get_standoff_location(self, schematic, tool, item):
        hx = (
            item.bounding_box.x1
            + 0.0
            + tool.get_symbol_property_as_float(
                schematic, "SW" + item.designator, "PCB_X", 0
            )
        )
        hy = (
            item.bounding_box.y1
            + 1.5
            + tool.get_symbol_property_as_float(
                schematic, "SW" + item.designator, "PCB_Y", 0
            )
        )

        return hx, hy

    def calc_pick_n_place(self):

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.to_list()

        tool = KicadTool()

        for item in self.layout:

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            diode = tool.find_footprint_by_reference(pcb, "D" + item.designator)
            # print(diode)

    def make_openscad_config_file(self):
        out = []

        for item in self.layout:

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

                oo = [
                    str(item.l_x),
                    str(item.l_y),
                    str(item.key_x),
                    str(item.key_y),
                ]

                out.append("KEY_" + item.label + " = [" + ", ".join(oo) + "];")

        out = "\r\n".join(out)

        with open(self.config.openscad_position_filename, "w") as f:
            f.write(out)

    def make_jlc_pcb_assembly_files(self):
        def q(s):
            return str(s)

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.to_list()

        tool = KicadTool()

        diodesRefs = []
        prints = tool.find_objects_by_atom(pcb, "footprint", 1)
        for p in prints:
            # print(p)

            o = tool.find_objects_by_atom(p, "fp_text", float("inf"))
            filtered = filter(
                lambda fp: (fp[1] == "reference") and (fp[2].startswith('"D')), o
            )
            lf = list(filtered)
            if len(lf) == 1:
                ref = list(lf)[0][2]
                ref = ref.replace('"', "")
                diodesRefs.append(ref)

        diodesRefs.sort()

        bom_headers = ["Comment", "Designator", "Footprint", "LCSC Part #"]
        cpl_headers = [
            "Designator",
            "Val",
            "Package",
            "Mid X",
            "Mid Y",
            "Rotation",
            "Layer",
        ]

        bom_refs = []
        cpl_rows = []

        for dRef in diodesRefs:
            bom_refs.append(dRef)

            at = tool.find_at_by_reference(pcb, dRef)

            x = float(at[1])
            y = float(at[2])
            r = float(at[3])

            cpl_row = [
                q(dRef),
                q("1N4148W"),
                q("SOD-123"),
                q(str(x) + "mm"),
                q(str(-y) + "mm"),  # The y coordinate system is inverted, of course.
                q(r + 180),
                q("top"),
            ]

            cpl_rows.append(cpl_row)

        bom_row = ["1N4148W", ",".join(bom_refs), "SOD-123", "C176288"]

        directory = Path(self.config.jlc_bom_filename).parent
        directory.mkdir(parents=True, exist_ok=True)

        with open(self.config.jlc_bom_filename, "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(bom_headers)

            # write the data
            writer.writerow(bom_row)

        directory = Path(self.config.jlc_cpl_filename).parent
        directory.mkdir(parents=True, exist_ok=True)

        with open(self.config.jlc_cpl_filename, "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(cpl_headers)

            # write the data
            writer.writerows(cpl_rows)

    def add_3d_models_to_pcb(self):

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.to_list()

        tool = KicadTool()

        for item in self.layout:
            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            diodeFootprint = tool.find_footprint_by_reference(
                pcb, "D" + item.designator
            )
            tool.remove_atoms(diodeFootprint, "model")
            tool.add_sd123_model(diodeFootprint, self.config.kicad_3dmodel_path_str)

            switchFootprint = tool.find_footprint_by_reference(
                pcb, "SW" + item.designator
            )
            tool.remove_atoms(switchFootprint, "model")
            tool.add_switch_model(switchFootprint, self.config.kicad_3dmodel_path_str)

            url = f"{self.config.kicad_keycap_vrml_path_str}/key_{item.label.lower()}_cap.wrl"
            tool.add_keycap_model(switchFootprint, url)

            url = f"{self.config.kicad_keycap_vrml_path_str}/key_{item.label.lower()}_legend.wrl"
            tool.add_keycap_model(switchFootprint, url)

        l = pcb_parser.list_to_sexp(pcb)
        out = "\r\n".join(l)

        with open(self.config.pcb_filename, "w") as f:
            f.write(out)

    def generate_openscad_case_file(self) -> None:
        def bboxToPolygon(bbox: BoundingBox) -> str:
            s = f" polygon(points=[ \
                [{bbox.x1},{bbox.y1}],\
                [{bbox.x1},{bbox.y2}],\
                [{bbox.x2},{bbox.y2}],\
                [{bbox.x2},{bbox.y1}]\
            ]);"
            return s

        def bbox_to_openscad_src(label: str, bbox: BoundingBox) -> str:
            return "[" + f'"{label}", {bbox.x1}, {bbox.y1}, {bbox.x2}, {bbox.y2}' + "]"

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.to_list()

        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.to_list()

        tool = KicadTool()

        code: List[str] = []
        standoffLocations: List[List[float]] = []
        bboxes: List[str] = []

        bbox = BoundingBox(-1, -1, -1, -1)

        for _item in self.layout:

            item: KeyInfo = _item

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            switch = tool.find_footprint_by_reference(pcb, "SW" + item.designator)

            item.bounding_box = tool.get_bounding_box_of_layer_lines(
                switch, Layer.User_Drawings
            )

            assert item.bounding_box is not None

            hx, rhy = self.get_standoff_location(schematic, tool, item)

            # Handle the flipped y axis
            hy = -rhy

            # OpenSCAD flips the y-axis
            item.bounding_box.y1 = -item.bounding_box.y1
            item.bounding_box.y2 = -item.bounding_box.y2

            standoffLocations.append([hx, hy])
            bboxes.append(bbox_to_openscad_src(item.label, item.bounding_box))

            bbox.update_xy(item.bounding_box.x1, item.bounding_box.y1)
            bbox.update_xy(item.bounding_box.x2, item.bounding_box.y2)

        bbox.add_border(self.config.pcb_border)

        len = abs(bbox.x2 - bbox.x1)
        wid = abs(bbox.y2 - bbox.y1)
        xorg = -bbox.x1 - len / 2
        yorg = -bbox.y1 - wid / 2

        code.append("include <../../openscad/utils.scad>;")

        code.append(f"CASE_PIECES = 2;")
        code.append(f"CASE_PIECE = 1;")

        code.append(f"BASE_THICKNESS = {BASE_THICKNESS};")

        code.append(f"BOARD_X1 = {xorg};")
        code.append(f"BOARD_Y1 = {yorg};")
        code.append(f"BOARD_X2 = {xorg + len};")
        code.append(f"BOARD_Y2 = {yorg + wid};")
        code.append(f"BOARD_LEN = {len};")
        code.append(f"BOARD_WIDTH = {wid};")
        code.append(f"CASE_HEIGHT = {CASE_HEIGHT};")

        code.append(f"STANDOFF_HOLE_INNER_DIAMETER = {STANDOFF_HOLE_INNER_DIAMETER};")
        code.append(f"STANDOFF_HOLE_OUTER_DIAMETER = {STANDOFF_HOLE_OUTER_DIAMETER};")
        code.append(f"STANDOFF_HOLE_HEIGHT = {STANDOFF_HOLE_HEIGHT};")
        code.append(f"MOUNTING_HOLE_D = {MOUNTING_HOLE_D};")
        code.append(f"MOUNTING_HOLE_OFFSET = {MOUNTING_HOLE_OFFSET};")

        code.append("keyStandoffs = [")
        for x, y in standoffLocations:
            code.append(f"[{x},{y}],")
        code.append("];")

        code.append("keyBoundingBoxes = [")
        for bb in bboxes:
            code.append(bb + ",")
        code.append("];")

        code.append("main(BOARD_WIDTH, BOARD_LEN, CASE_PIECES, CASE_PIECE);")

        out = os.linesep.join(code)

        with open(self.config.case_filename, "w") as f:
            f.write(out)

    def __print_formatted(self, title: str, numbers: List[float]):
        formatted_numbers: List[str] = []

        for n in numbers:
            fmt = f"{n:2.2f}"
            if n >= 0:
                fmt = " " + fmt
            formatted_numbers.append(fmt)

        ff = ", ".join(formatted_numbers)

        print(title + ":" + ff)


if __name__ == "__main__":
    pass
