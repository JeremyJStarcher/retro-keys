import json
import csv
import os
from typing import List
from kicad_parser import KiCadParser
from kicad_tools import KicadTool
from kicad_tools import Layer
from kicad_tools import BoundingBox

STANDOFF_HOLE_INNER_DIAMETER = 2.2
STANDOFF_HOLE_OUTER_DIAMETER = 4
STANDOFF_HOLE_HEIGHT = 3
CASE_HEIGTH = 10
MOUNTING_HOLE_OFFSET = 5
MOUNTING_HOLE_D = 3.2


class ProcessConfiguration:
    # These paths are relative to the 'py' directory
    qmk_layout_filename: str
    pcb_filename: str
    case_filename: str
    keyboard_sch_sheet_filename_name: str
    openscad_position_filename: str
    jlc_bom_filename: str
    jlc_cpl_filename: str

    # These paths are relative to the KiCad project directory
    kicad_3dmodel_path: str
    kicad_keycap_vrml_path: str

    matrix_starting_index: int
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
    matrix_r: float = 0
    matrix_c: float = 0
    designator: str = ""
    label: str = ""
    skip = True
    diode_x: float = 0
    diode_y: float = 0
    hole_x: float = 0
    hole_y: float = 0
    boundingBox: BoundingBox | None = None

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

        l.append("matrix_c: " + str(self.matrix_c))
        l.append("matrix_r: " + str(self.matrix_r))

        return "{ " + ", ".join(l) + " }"


class ProcessKeyboard:
    config: ProcessConfiguration

    def __init__(self, config: ProcessConfiguration):
        self.config = config

    def read_sexp(self, name: str):
        with open(name, "r") as f:
            data = f.read()
        return data

    def read_json(self, name: str):
        with open(name, "r") as f:
            data = f.read()
        d_dict = json.loads(data)
        return d_dict["layouts"]["LAYOUT"]["layout"]

    def setdesignators(self, startingIndex: int, keys: list):
        filtered = list(filter(lambda key: not key.skip, keys))

        # Just make sure that "xx" and "yy" are far greater than your grid.
        # Any spots that are unused will be skipped, just like there are no
        # references assigned to empty spots on your schematic grid.

        idx = startingIndex
        for col in range(10):
            for row in range(10):

                items = filter(
                    lambda zkey: (zkey.matrix_r == row) and (zkey.matrix_c == col),
                    filtered,
                )

                ll = list(items)
                if len(ll) > 0:
                    key = ll[0]
                    key.designator = str(idx)
                    idx += 1

    def get_layout(self) -> list:
        info = self.read_json(self.config.qmk_layout_filename)
        keys = []

        KEYSWITCH_FIX_X = -11.565
        KEYSWITCH_FIX_Y = -3.946

        for key in info:

            keyInfo = KeyInfo()

            keyInfo.skip = key.get("x") == -1
            keyInfo.label = key.get("label")

            keyInfo.w = float(key.get("w", 1))
            keyInfo.h = float(key.get("h", 1))

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

            keyInfo.l_x = key.get("x")
            keyInfo.l_y = key.get("y")

            x = (float(key.get("x")) + (KeyInfo.w / 2)) * self.config.UNIT
            y = (float(key.get("y")) + (KeyInfo.h / 2)) * self.config.UNIT

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
            y1 = (keyInfo.key_y - keyInfo.h / 2) - hh / 2 + KEYSWITCH_FIX_Y
            x2 = x1 + self.config.UNIT + ww
            y2 = y1 + self.config.UNIT + hh

            x1 += xfix

            keyInfo.hole_x = keyInfo.key_x + 10
            keyInfo.hole_y = keyInfo.key_y + 10

            matrix = key.get("matrix")
            keyInfo.matrix_c = matrix[0]
            keyInfo.matrix_r = matrix[1]

            keys.append(keyInfo)

        self.setdesignators(self.config.matrix_starting_index, keys)
        return keys

    def run_it(self) -> None:

        layout = self.get_layout()

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.toList()

        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.toList()

        tool = KicadTool()

        bbox = BoundingBox(-1, -1, -1, -1)

        for _item in layout:

            item: KeyInfo = _item

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            tool.setObjectLocation(
                pcb, "SW" + item.designator, item.key_x, item.key_y, 0
            )

            switch = tool.findFootprintByReference(pcb, "SW" + item.designator)
            at = tool.findAtByReference(pcb, "SW" + item.designator)
            tool.setHiddenFootprintTextByReference(
                pcb, "SW" + item.designator, "value", False
            )

            tool.moveTextToLayer(
                pcb, "SW" + item.designator, "value", Layer.F_Silkscreen
            )
            tool.copyToBackSilkscreen(pcb, "SW" + item.designator, "value")

            item.boundingBox = tool.getBoundingBoxOfLayerLines(
                switch, Layer.User_Drawings
            )

            assert item.boundingBox is not None

            tool.addBoundingBox(pcb, item.boundingBox, 0.3, Layer.F_Silkscreen)
            tool.addBoundingBox(pcb, item.boundingBox, 0.3, Layer.B_Silkscreen)

            bbox.update_xy(item.boundingBox.x1, item.boundingBox.y1)
            bbox.update_xy(item.boundingBox.x2, item.boundingBox.y2)

            tool.setObjectLocation(
                pcb, "D" + item.designator, item.diode_x, item.diode_y, -90
            )

            hx, hy = self.get_standoff_location(schematic, tool, item)

            tool.drawKeepoutZone(pcb, hx, hy, 3)
            tool.drawCircle(pcb, Layer.Edge_Cuts, hx, hy, STANDOFF_HOLE_INNER_DIAMETER)

        bbox.addBorder(self.config.pcb_border)
        tool.addBoundingBox(pcb, bbox, 0.3, Layer.Edge_Cuts)

        bbox.addBorder(-MOUNTING_HOLE_OFFSET)
        tool.setObjectLocation(pcb, "H101", bbox.x1, bbox.y1, 0)
        tool.setObjectLocation(pcb, "H102", bbox.x1, bbox.y2, 0)
        tool.setObjectLocation(pcb, "H103", bbox.x2, bbox.y1, 0)
        tool.setObjectLocation(pcb, "H104", bbox.x2, bbox.y2, 0)

        l = pcb_parser.listToSexp(pcb)
        out = "\r\n".join(l)

        with open(self.config.pcb_filename, "w") as f:
            f.write(out)

    def get_standoff_location(self, schematic, tool, item):
        hx = (
            item.boundingBox.x1
            + 0.0
            + tool.getSymbolPropertyAsFloat(
                schematic, "SW" + item.designator, "PCB_X", 0
            )
        )
        hy = (
            item.boundingBox.y1
            + 1.5
            + tool.getSymbolPropertyAsFloat(
                schematic, "SW" + item.designator, "PCB_Y", 0
            )
        )

        return hx, hy

    def calcPnP(self):
        layout = self.get_layout()

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.toList()

        tool = KicadTool()

        for item in layout:

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            diode = tool.findFootprintByReference(pcb, "D" + item.designator)
            # print(diode)

    def makeOpenScad(self):
        layout = self.get_layout()
        out = []

        for item in layout:

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

    def makeJlcPcb(self):
        def q(s):
            return str(s)

        layout = self.get_layout()

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.toList()

        tool = KicadTool()

        diodesRefs = []
        prints = tool.findObjectsByNoun(pcb, "footprint", 1)
        for p in prints:
            # print(p)

            o = tool.findObjectsByNoun(p, "fp_text", float("inf"))
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

            at = tool.findAtByReference(pcb, dRef)

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

        with open(self.config.jlc_bom_filename, "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(bom_headers)

            # write the data
            writer.writerow(bom_row)

        with open(self.config.jlc_cpl_filename, "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(cpl_headers)

            # write the data
            writer.writerows(cpl_rows)

    def setModels(self):
        layout = self.get_layout()

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.toList()

        tool = KicadTool()

        for item in layout:
            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            diodeFootprint = tool.findFootprintByReference(pcb, "D" + item.designator)
            tool.removeNouns(diodeFootprint, "model")
            tool.addSD123Model(diodeFootprint, self.config.kicad_3dmodel_path)

            switchFootprint = tool.findFootprintByReference(pcb, "SW" + item.designator)
            tool.removeNouns(switchFootprint, "model")
            tool.addSwitchModel(switchFootprint, self.config.kicad_3dmodel_path)

            url = (
                f"{self.config.kicad_keycap_vrml_path}key_{item.label.lower()}_cap.wrl"
            )
            tool.addKeycapModel(switchFootprint, url)

            url = f"{self.config.kicad_keycap_vrml_path}key_{item.label.lower()}_insert.wrl"
            tool.addKeycapModel(switchFootprint, url)

        l = pcb_parser.listToSexp(pcb)
        out = "\r\n".join(l)

        with open(self.config.pcb_filename, "w") as f:
            f.write(out)

    def generateOpenscadCase(self) -> None:
        def bboxToPolygon(bbox: BoundingBox) -> str:
            s = f" polygon(points=[ \
                [{bbox.x1},{bbox.y1}],\
                [{bbox.x1},{bbox.y2}],\
                [{bbox.x2},{bbox.y2}],\
                [{bbox.x2},{bbox.y1}]\
            ]);"
            return s

        def BboxToOpenScadItem(label: str, bbox: BoundingBox) -> str:
            return "[" + f'"{label}", {bbox.x1}, {bbox.y1}, {bbox.x2}, {bbox.y2}' + "]"

        layout = self.get_layout()

        pcb_sexp = self.read_sexp(self.config.pcb_filename)
        pcb_parser = KiCadParser(pcb_sexp)
        pcb = pcb_parser.toList()

        key_sch_sexp = self.read_sexp(self.config.keyboard_sch_sheet_filename_name)
        key_parser = KiCadParser(key_sch_sexp)
        schematic = key_parser.toList()

        tool = KicadTool()

        code: List[str] = []
        standoffLocations: List[List[float]] = []
        bboxes: List[str] = []

        bbox = BoundingBox(-1, -1, -1, -1)

        for _item in layout:

            item: KeyInfo = _item

            if item.designator == "":
                print("skipping " + item.label)
                continue
            else:
                print("Searching for " + item.label + " " + item.designator)

            switch = tool.findFootprintByReference(pcb, "SW" + item.designator)

            item.boundingBox = tool.getBoundingBoxOfLayerLines(
                switch, Layer.User_Drawings
            )

            assert item.boundingBox is not None

            # OpenSCAD flips the y-axis
            item.boundingBox.y1 = -item.boundingBox.y1
            item.boundingBox.y2 = -item.boundingBox.y2

            hx, rhy = self.get_standoff_location(schematic, tool, item)

            # Handle the flipped y axis
            hy = rhy - (
                tool.getSymbolPropertyAsFloat(
                    schematic, "SW" + item.designator, "PCB_Y", 0
                )
                * 2
            )

            standoffLocations.append([hx, hy])
            bboxes.append(BboxToOpenScadItem(item.label, item.boundingBox))

            bbox.update_xy(item.boundingBox.x1, item.boundingBox.y1)
            bbox.update_xy(item.boundingBox.x2, item.boundingBox.y2)

        bbox.addBorder(self.config.pcb_border)

        len = abs(bbox.x2 - bbox.x1)
        wid = abs(bbox.y2 - bbox.y1)
        xorg = -bbox.x1 - len / 2
        yorg = -bbox.y1 - wid / 2

        code.append("include <../../openscad/utils.scad>;")

        code.append("BASE_THICKNESS = 3;")

        code.append(f"BOARD_X1 = {xorg};")
        code.append(f"BOARD_Y1 = {yorg};")
        code.append(f"BOARD_X2 = {xorg + len};")
        code.append(f"BOARD_Y2 = {yorg + wid};")
        code.append(f"BOARD_LEN = {len};")
        code.append(f"BOARD_WID = {wid};")
        code.append(f"CASE_HEIGTH = {CASE_HEIGTH};")

        code.append(f"STANDOFF_HOLE_INNER_DIAMETER = {STANDOFF_HOLE_INNER_DIAMETER};")
        code.append(f"STANDOFF_HOLE_OUTER_DIAMETER = {STANDOFF_HOLE_OUTER_DIAMETER};")
        code.append(f"STANDOFF_HOLE_HEIGHT = {STANDOFF_HOLE_HEIGHT};")
        code.append(f"MOUNTING_HOLE_D = {MOUNTING_HOLE_D};")
        code.append(f"MOUNTING_HOLE_OFFSET = {MOUNTING_HOLE_OFFSET};")

        code.append("module caseBoundBox() {")
        code.append('color("white") linear_extrude(BASE_THICKNESS)')
        code.append(bboxToPolygon(bbox))
        code.append("}")

        code.append("keyStandoffs = [")
        for x, y in standoffLocations:
            code.append(f"[{x},{y}],")
        code.append("];")

        code.append("keyBoundingBoxes = [")
        for bb in bboxes:
            code.append(bb + ",")
        code.append("];")

        code.append("main();")

        out = os.linesep.join(code)

        with open(self.config.case_filename, "w") as f:
            f.write(out)


if __name__ == "__main__":
    pass
