from dataclasses import dataclass
from decimal import Decimal, getcontext
import json
import csv
import os
from pathlib import Path
import re
from typing import Callable, List
from common_key_format import CommonKeyData
from ki_symbols import KiSymbols
from kicad_parser import KiCadParser
from kicad_tools import KicadTool, QueryRecursionLevel
from kicad_tools import Layer
from kicad_tools import BoundingBox
from kle_tools import KleTools
from qmk_tools import QmkTools
from sexptype import SexpType, makeDecimal, makeString

BASE_THICKNESS = 3

"""Make it smaller then the ACTUAL hole so our peg isn't caught"""
# STANDOFF_HOLE_INNER_DIAMETER = (2.2 * 2) * .8
STANDOFF_HOLE_INNER_DIAMETER = Decimal(1.5)
STANDOFF_HOLE_OUTER_DIAMETER = Decimal(3)
STANDOFF_HOLE_HEIGHT = Decimal(3)
CASE_HEIGHT = 6
MOUNTING_HOLE_OFFSET = 5
MOUNTING_HOLE_D = 3.2


PRINTER_X = 280
PRINTER_Y = 260


class KeyInfo:
    # Logical position, based on key units
    l_x: Decimal = Decimal(0)
    l_y: Decimal = Decimal(0)

    # Absolute position
    key_x: Decimal = Decimal(0)
    key_y: Decimal = Decimal(0)
    w: Decimal = Decimal(0)
    h: Decimal = Decimal(0)
    designator: str = ""
    label: str = ""
    skip = True
    diode_x: Decimal = Decimal(0)
    diode_y: Decimal = Decimal(0)
    hole_x: Decimal = Decimal(0)
    hole_y: Decimal = Decimal(0)
    bounding_box: BoundingBox | None = None

    def __init__(self):
        getcontext().prec = 8

        self.bbox = BoundingBox()

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


@dataclass
class RunWrappedOptions:
    pcb: SexpType
    schematic: SexpType
    tool: KicadTool
    keys: List[KeyInfo]


RunWrappedType = Callable[[RunWrappedOptions], None]


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

    UNIT = Decimal(19.05)

    pcb_x_orig = Decimal(2 * UNIT)
    pcb_y_orig = Decimal(9 * UNIT)
    pcb_border = Decimal(UNIT / 2)

    # How much to move the diodes
    diode_offset_x = Decimal(UNIT / 2)
    diode_offset_y = (
        Decimal(UNIT / 8) + 2
    )  # A little breathing room for the support screws


class ProcessKeyboard:
    config: ProcessConfiguration
    common_key_format: CommonKeyData = CommonKeyData()
    layout: List[KeyInfo]

    def __init__(self, config: ProcessConfiguration):
        self.config = config
        self.__populateCommonData()
        self.layout = self.__get_layout_from_kle()

    def read_sexp(self, name: Path) -> str:
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

    def __get_bare_reference_id(self, s: str) -> str:
        """
        Strip off the prefix
        SW227
        and D227

        Both just become "227"
        """

        new_string = re.sub(r"^[a-zA-Z]+", "", s)
        return new_string

    def set_designators(self, keys: List[KeyInfo]) -> None:
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

        for key_name in self.common_key_format.get_key_names():
            key = self.common_key_format.get_from_common_keys_or_new(key_name)

            keyInfo = KeyInfo()

            keyInfo.skip = key.is_decal
            keyInfo.label = key.name

            keyInfo.w = key.w
            keyInfo.h = key.h

            keyInfo.l_x = key.qmk_location.x
            keyInfo.l_y = key.qmk_location.y

            x = (keyInfo.l_x + (KeyInfo.w / 2)) * self.config.UNIT
            y = (keyInfo.l_y + (KeyInfo.h / 2)) * self.config.UNIT

            x += self.config.pcb_x_orig
            y += self.config.pcb_y_orig

            ww = (keyInfo.w - 1) * self.config.UNIT
            hh = (keyInfo.h - 1) * self.config.UNIT

            keyInfo.key_x = x + ww / 2
            keyInfo.key_y = y + hh / 2

            keyInfo.diode_x = keyInfo.key_x + self.config.diode_offset_x
            keyInfo.diode_x = keyInfo.key_x + keyInfo.w * self.config.UNIT / 2

            keyInfo.diode_y = keyInfo.key_y + self.config.diode_offset_y

            keyInfo.hole_x = keyInfo.key_x + 10
            keyInfo.hole_y = keyInfo.key_y + 10

            keys.append(keyInfo)

        self.set_designators(keys)
        return keys

    def add_schematic_lib_symbols(self, options: RunWrappedOptions) -> None:
        schematic = options.schematic
        tool = options.tool

        # print(schematic)
        # key_parser.print_list(schematic, 0)

        schematic_lib_symbols = tool.find_object_by_atom(
            schematic, "lib_symbols", QueryRecursionLevel.HERE
        )
        schematic_symbols = tool.find_objects_by_atom(
            schematic_lib_symbols, "symbol", QueryRecursionLevel.HERE
        )
        scematic_existing_names = [x[1] for x in schematic_symbols]

        load_lib_symbols = KiSymbols.get_lib_symbols()
        load_symbols = tool.find_objects_by_atom(
            load_lib_symbols, "symbol", QueryRecursionLevel.HERE
        )
        load_incoming_names = [x[1] for x in load_symbols]

        new_names = list(set(load_incoming_names).difference(scematic_existing_names))

        for symbol in load_symbols:
            if symbol[1] in new_names:
                schematic_lib_symbols.append(symbol)

    def add_schematic_connections(self, options: RunWrappedOptions) -> None:
        key_schematic = options.schematic
        tool = options.tool

        matrix: list[list[int]] = []

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

            matrix.append([])

            for x in range(matrix_min_x, matrix_max_x + 1):
                matrix[y].append(-1)

                for key_name in self.common_key_format.get_key_names():
                    key = self.common_key_format.get_from_common_keys_or_new(key_name)

                    if key.is_decal:
                        continue

                    kmx = int(float(key.matrix[1]))
                    kmy = int(float(key.matrix[0]))

                    if kmx == x and kmy == y:
                        matrix[y].pop()
                        matrix[y].append(base_designator)

                        tool.add_keyswitch_to_schematic(
                            str(base_designator),
                            key.name,
                            key_schematic,
                            x,
                            y,
                            key.w,
                        )

                        base_designator += 1

        tool.add_wires_to_schematic(key_schematic, matrix)

    def run_wrapped(self, funcs: list[RunWrappedType]):
        # Prepare and load data
        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.to_list()

        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.to_list()

        tool = KicadTool()

        filtered_list = [obj for obj in self.layout if obj.designator != ""]
        options = RunWrappedOptions(pcb, schematic, tool, filtered_list)

        for func in funcs:
            func(options)

        ## Save data
        pcb_list = pcb_parser.list_to_sexp(pcb)
        out = "\r\n".join(pcb_list)

        with open(self.config.pcb_filename, "w") as f:
            f.write(out)

        key_list = key_parser.list_to_sexp(schematic)
        key_out = "\r\n".join(key_list)

        with open(self.config.keyboard_sch_sheet_filename_name, "w") as f:
            f.write(key_out)

    def relocate_parts_and_draw_silkscreen(self, options: RunWrappedOptions) -> None:
        pcb = options.pcb
        schematic = options.schematic
        tool = options.tool

        bbox = BoundingBox()

        zones = tool.find_objects_by_atom(pcb, "zone", QueryRecursionLevel.HERE)
        for zone in zones:
            keepout_flag = tool.find_object_by_atom(
                zone, "keepout", QueryRecursionLevel.HERE
            )
            if keepout_flag != None:
                pcb.remove(zone)

        shapes = tool.find_objects_by_atom(pcb, "gr_circle", QueryRecursionLevel.HERE)
        for shape in shapes:
            pcb.remove(shape)

        shapes = tool.find_objects_by_atom(pcb, "gr_rect", QueryRecursionLevel.HERE)
        for shape in shapes:
            pcb.remove(shape)

        for item in options.keys:

            tool.set_object_location(
                pcb, "SW" + item.designator, item.key_x, item.key_y, Decimal(0)
            )

            switch = tool.find_footprint_by_reference(pcb, "SW" + item.designator)
            at = tool.find_footprint_at_by_reference(pcb, "SW" + item.designator)
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
                pcb, "D" + item.designator, item.diode_x, item.diode_y, Decimal(-90)
            )

            hx, hy = self.get_standoff_location(schematic, tool, item)

            tool.draw_keepout_zone(pcb, hx, hy, STANDOFF_HOLE_OUTER_DIAMETER)
            tool.draw_circle(
                pcb, Layer.Edge_Cuts, hx, hy, STANDOFF_HOLE_INNER_DIAMETER, "solid"
            )

        bbox.add_border(self.config.pcb_border)
        tool.add_bounding_box(pcb, bbox, 0.3, Layer.Edge_Cuts)

        bbox.add_border(Decimal(-MOUNTING_HOLE_OFFSET))
        tool.set_object_location(pcb, "H101", bbox.x1, bbox.y1, Decimal(0))
        tool.set_object_location(pcb, "H102", bbox.x1, bbox.y2, Decimal(0))
        tool.set_object_location(pcb, "H103", bbox.x2, bbox.y1, Decimal(0))
        tool.set_object_location(pcb, "H104", bbox.x2, bbox.y2, Decimal(0))

    def get_standoff_location(
        self, schematic: SexpType, tool: KicadTool, item: KeyInfo
    ) -> tuple[Decimal, Decimal]:
        if item.bounding_box is None:
            raise Exception("get_standoff_location called with invalid bounding box")

        hx = item.bounding_box.x1
        hy = item.bounding_box.y1

        return hx, hy

    def calc_pick_n_place(self, options: RunWrappedOptions) -> None:
        pcb = options.pcb
        tool = options.tool

        for item in options.keys:
            diode = tool.find_footprint_by_reference(pcb, "D" + item.designator)

    def make_openscad_config_file(self, options: RunWrappedOptions) -> None:
        out = []

        for item in options.keys:
            oo = [
                str(item.l_x),
                str(item.l_y),
                str(item.key_x),
                str(item.key_y),
            ]

            out.append("KEY_" + item.label + " = [" + ", ".join(oo) + "];")

        outtxt = "\r\n".join(out)

        with open(self.config.openscad_position_filename, "w") as f:
            f.write(outtxt)

    def make_jlc_pcb_assembly_files(self, options: RunWrappedOptions) -> None:
        def q(s):
            return str(s)

        pcb = options.pcb
        tool = options.tool

        diodesRefs = []
        prints = tool.find_objects_by_atom(pcb, "footprint", QueryRecursionLevel.HERE)
        for p in prints:

            o = tool.find_objects_by_atom(p, "fp_text", QueryRecursionLevel.DEEP)
            filtered = filter(
                lambda fp: (isinstance(fp[2], str) and fp[1] == "reference")
                and (fp[2].startswith('"D')),
                o,
            )

            lf = list(filtered)
            if len(lf) == 1:
                ref1 = list(lf)[0][2]
                ref = makeString(ref1).replace('"', "")
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

            at = tool.find_footprint_at_by_reference(pcb, dRef)

            x = makeDecimal(at[1])
            y = makeDecimal(at[2])
            r = makeDecimal(at[3])

            cpl_row = [
                q(dRef),
                q("1N4148W"),
                q("SOD-123"),
                q(str(x) + "mm"),
                q(str(-y) + "mm"),  # The y coordinate system is inverted, of course.
                q(str(r + 180)),
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

    def add_3d_models_to_pcb(self, options: RunWrappedOptions) -> None:
        pcb = options.pcb
        tool = options.tool

        for item in options.keys:

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

    def generate_openscad_case_file(self, options: RunWrappedOptions) -> None:
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

        pcb = options.pcb
        schematic = options.schematic
        tool = options.tool

        code: list[str] = []
        standoffLocations: List[List[Decimal]] = []
        bboxes: list[str] = []

        bbox = BoundingBox()

        for item in options.keys:
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


if __name__ == "__main__":
    pass
