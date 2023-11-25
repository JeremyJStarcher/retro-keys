from enum import Enum
import copy
import math

from typing import Dict, List, cast

from ki_symbols import KiSymbols

INF = float("inf")


class Layer(str, Enum):
    F_CU = '"F.Cu"'
    B_CU = '"B.Cu"'
    B_Adhesive = '"B.Adhes"'
    F_Adhesive = '"F.Adhes"'
    B_Paste = '"B.Paste"'
    F_Paste = '"F.Paste"'
    B_Silkscreen = '"B.SilkS"'
    F_Silkscreen = '"F.SilkS"'
    B_Mask = '"B.Mask"'
    F_Mask = '"F.Mask"'
    User_Drawings = '"Dwgs.User"'
    User_Comments = '"Cmts.User"'
    User_Eco1 = '"Eco1.User"'
    User_Eco2 = '"Eco2.User"'
    Edge_Cuts = '"Edge.Cuts"'
    Margin = '"Margin"'
    B_Courtyard = '"B.CrtYd"'
    F_Courtyard = '"F.CrtYd"'
    B_Fab = '"B.Fab"'
    F_Fab = '"F.Fab"'


class BoundingBox:
    def __init__(self, x1: float = -1, y1: float = -1, x2: float = -1, y2: float = -1):

        if x1 == -1:
            self.x1 = float("inf")
            self.y1 = float("inf")
            self.x2 = float("-inf")
            self.y2 = float("-inf")
        else:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

    def update_xy(self, sx: str | float, sy: str | float) -> None:
        x = float(sx)
        y = float(sy)

        self.x1 = min(self.x1, x)
        self.y1 = min(self.y1, y)
        self.x2 = max(self.x2, x)
        self.y2 = max(self.y2, y)

    def add_border(self, n: float) -> None:
        self.x1 -= n
        self.y1 -= n
        self.x2 += n
        self.y2 += n

    def __repr__(self):
        l = []

        l.append("x1: " + str(self.x1))
        l.append("y1: " + str(self.y1))
        l.append("x2: " + str(self.x2))
        l.append("y2: " + str(self.y2))

        return "{ " + ", ".join(l) + " }"


def q_string(s: str) -> str:
    return '"' + s + '"'


class KicadTool:

    # def __init__():
    #     pass

    def find_objects_by_atom(self, root: list, atom: str, maxDepth=float("inf")):
        def _find_objects_by_atom_inner(array, atom, maxDepth, depth, out):
            for e in array:
                if isinstance(e, list):
                    if (len(e) > 0) and (e[0] == atom):
                        out.append(e)

                    if depth < maxDepth:
                        _find_objects_by_atom_inner(e, atom, maxDepth, depth + 1, out)
                else:
                    pass
            return out

        return _find_objects_by_atom_inner([root], atom, maxDepth, 0, [])

    def find_object_by_atom(self, root: list, atom: str, maxDepth=float("inf")):
        objs = self.find_objects_by_atom(root, atom, maxDepth)
        if len(objs) > 1:
            raise Exception(f"Found too many {atom}")
        if len(objs) == 0:
            raise Exception(f"Found zero {atom}" + atom)
        return objs[0]

    def find_footprint_by_reference(self, root: list, ref: str) -> list:
        prints = self.find_objects_by_atom(root, "footprint", 1)

        for p in prints:
            # print(p)

            o = self.find_objects_by_atom(p, "fp_text", INF)
            filtered = filter(
                lambda fp: (fp[1] == "reference") and (fp[2] == q_string(ref)), o
            )

            lst = list(filtered)
            if len(lst) > 0:
                return p

        return []

    def _get_text_obj_by_type(self, root: list, ref: str, type: str) -> list:
        p = self.find_footprint_by_reference(root, ref)

        assert p is not None

        o = self.find_objects_by_atom(p, "fp_text", INF)
        filtered = filter(lambda fp: (fp[1] == type), o)
        obj = list(filtered)[0]
        return obj

    def set_hidden_footprint_text_by_reference(
        self, root: list, ref: str, type: str, hidden: bool
    ):
        obj = self._get_text_obj_by_type(root, ref, type)

        # If it is already there, remove it.
        if "hide" in obj:
            obj.remove("hide")

        if hidden:
            obj.append("hide")

    def move_text_to_layer(self, root: list, ref: str, type: str, layer: Layer):
        obj = self._get_text_obj_by_type(root, ref, type)

        o = self.find_objects_by_atom(obj, "layer", INF)

        lst = list(o)
        lst[0][1] = layer

    def copy_to_back_silkscreen(self, root: list, ref: str, type: str):
        p = self.find_footprint_by_reference(root, ref)
        assert p is not None

        obj = self._get_text_obj_by_type(root, ref, type)
        nn = copy.deepcopy(obj)

        layerObject = self.find_objects_by_atom(nn, "layer", INF)

        lst = list(layerObject)
        lst[0][1] = Layer.B_Silkscreen
        nn[1] = "user"

        effectsObject = self.find_objects_by_atom(nn, "effects", INF)

        effectsList = list(effectsObject)
        effectsList[0].append(["justify", "mirror"])

        p.append(nn)

    def get_all_symbol_value_references(self, root: list) -> Dict[str, List[str]]:
        ret: Dict[str, List[str]] = dict()

        symbols = self.find_objects_by_atom(root, "symbol", 1)

        for symbol in symbols:
            properties = self.find_objects_by_atom(symbol, "property", 1)

            value_property = next(
                filter(lambda fp: (fp[1] == q_string("Value")), properties), "None"
            )

            reference_property = next(
                filter(lambda fp: (fp[1] == q_string("Reference")), properties),
                "--NONE--",
            )

            if value_property and reference_property:
                value: str = value_property[2].strip('"')
                reference: str = reference_property[2].strip('"')

                if not value in ret:
                    ret[value] = []

                v = ret[value]
                v.append(reference)
        return ret

    def find_symbol_by_reference(self, root: list, ref: str):
        symbols = self.find_objects_by_atom(root, "symbol", 1)

        for symbol in symbols:
            o = self.find_objects_by_atom(symbol, "property", INF)

            filtered = filter(
                lambda fp: (fp[1] == q_string("Reference"))
                and (fp[2] == q_string(ref)),
                o,
            )

            lst = list(filtered)
            if len(lst) > 0:
                return symbol

    def get_symbol_property(self, root: list, ref: str, prop: str, default: str):
        symbol = cast(list, self.find_symbol_by_reference(root, ref))

        o = self.find_objects_by_atom(symbol, "property", INF)

        filtered = filter(lambda fp: (fp[1] == q_string(prop)), o)
        lst = list(filtered)
        if len(lst) > 0:
            return lst[0][2]
        else:
            return default

    def get_symbol_property_as_float(self, root: list, ref: str, prop: str, default):
        r = self.get_symbol_property(root, ref, prop, default)
        r = str(r)
        return float(r.strip('"'))

    def find_at_by_reference(self, root: list, ref: str) -> list:
        footprint = self.find_footprint_by_reference(root, ref)
        assert footprint is not None

        o = self.find_object_by_atom(footprint, "at", 1)

        # There are optional parameters.
        # Its harmless to fill them in and makes other code
        # a lot simplier.
        while len(o) != 4:
            o.append("0")

        return o

    def set_object_location(
        self, root: list, ref: str, x: float, y: float, rot: float = 0
    ):
        footprint = self.find_footprint_by_reference(root, ref)

        cat = self.find_at_by_reference(root, ref)

        current_rot = float(cat[3])
        # If the object is already rotated, then un-rotate it
        if current_rot != 0:
            cat[3] = float(cat[3]) - current_rot
            self.set_object_location(root, ref, x, y, -current_rot)

        all_ats = self.find_objects_by_atom(footprint, "at", INF)
        for at1 in all_ats:
            at1.append(0)  # If there isn't a rotation, add it.

            at1_x = at1[1]
            at1_y = at1[2]
            at1_rot = at1[3]

            while len(at1) > 0:
                at1.pop()

            at1.append("at")
            at1.append(at1_x)
            at1.append(at1_y)
            at1.append(int(at1_rot) + rot)

        # Set the primary location and rotation
        at = self.find_at_by_reference(root, ref)
        if at != None:
            at.append(0)
            old_rot = at[3]
            while len(at) > 0:
                at.pop()

            at.append("at")
            at.append(x)
            at.append(y)
            at.append(rot)

    def add_bounding_box(
        self, root: list, box: BoundingBox, width: float, layer: Layer
    ):
        _box = [
            "gr_rect",
            ["start", box.x1, box.y1],
            ["end", box.x2, box.y2],
            ["layer", layer],
            ["width", width],
            ["fill", "none"],
        ]

        root.append(_box)

    def get_bounding_box_of_layer_lines(self, root: list, layerName: Layer):
        lines = []

        g_lines = self.find_objects_by_atom(root, "fp_line", float("inf"))
        at = self.find_objects_by_atom(root, "at", 1)

        origin_x = float(at[0][1])
        origin_y = float(at[0][2])

        for g_line in g_lines:
            layers = self.find_objects_by_atom(g_line, "layer", float("inf"))
            for layer in layers:
                if layer[1] == layerName:
                    lines.append(g_line)

        box = BoundingBox(-1, -1, -1, -1)
        for line in lines:
            start = self.find_object_by_atom(line, "start", float("inf"))
            end = self.find_object_by_atom(line, "end", float("inf"))

            x1 = float(start[1])
            y1 = float(start[2])
            x2 = float(end[1])
            y2 = float(end[2])

            box.update_xy(x1 + origin_x, y1 + origin_y)
            box.update_xy(x2 + origin_x, y2 + origin_y)

        return box

    def draw_circle(self, root: list, layer: Layer, x: float, y: float, r: float):
        o = [
            "gr_circle",
            ["center", x, y],
            ["end", x, y - r],
            ["layer", layer],
            ["width", "0.2"],
            ["fill", "none"],
        ]

        root.append(o)

    def move_recursive(self, root: list, mx: float, my: float, mr: int):
        first_at = self.find_object_by_atom(root, "at", 1)
        while len(first_at) != 4:
            first_at.append("0")

        at_x = float(first_at[1])
        at_y = float(first_at[2])
        at_r = float(first_at[3])

        all_at = self.find_objects_by_atom(root, "at", math.inf)
        for atm in all_at:
            while len(atm) != 4:
                atm.append("0")

            atm[1] = float(atm[1]) - at_x + mx
            atm[2] = float(atm[2]) - at_y + my
            atm[3] = int(float(atm[3]) - at_r + mr)

    def get_relative_pin_position_for_schematic(
        self, root: list, obj: list, type: str, value: str
    ):
        item_lib_id = self.find_object_by_atom(obj, "lib_id")

        lib_symbols = self.find_object_by_atom(root, "lib_symbols")
        symbols = self.find_objects_by_atom(lib_symbols, "symbol", 1)

        for symbol in symbols:
            if item_lib_id[1] == symbol[1]:
                pins = self.find_objects_by_atom(symbol, "pin")

                for pin in pins:

                    match = self.find_object_by_atom(pin, type)
                    pin_value = match[1]
                    if pin_value == q_string(value):
                        pin_at = self.find_object_by_atom(pin, "at", 1)
                        n = [float(pin_at[1]), float(pin_at[2])]
                        return n
        return [0, 0]

    def add_keyswitch_to_schematic(
        self, designator: str, name: str, root: list, mx: int, my: int
    ):
        # jjz

        TOP_X = -50
        TOP_Y = -50
        STEP_X = 30
        STEP_Y = 20

        symbol_diode = KiSymbols.get_diode("D" + designator, name)
        symbol_switch = KiSymbols.get_mx_with_led("SW" + designator, name)

        cluster_x = TOP_X + (mx * STEP_X)
        cluster_y = TOP_Y + (my * STEP_Y)

        self.move_recursive(symbol_switch, cluster_x, cluster_y, 0)

        pos1 = self.get_relative_pin_position_for_schematic(
            root, symbol_switch, "number", "1"
        )
        pos2 = self.get_relative_pin_position_for_schematic(
            root, symbol_diode, "number", "1"
        )

        print(pos1, pos2)

        diode_x = cluster_x + pos2[0] - pos1[0]
        diode_y = cluster_y + pos2[1] - pos1[1]

        self.move_recursive(symbol_diode, diode_x, diode_y, 0)

        root.append(symbol_switch)
        root.append(symbol_diode)

    def draw_keepout_zone(self, root: list, nx: float, ny: float, r: float):
        def points_in_circumference(r, n=100):
            pi = math.pi

            return [
                (math.cos(2 * pi / n * x) * r, math.sin(2 * pi / n * x) * r)
                for x in range(0, n + 1)
            ]

        o = [
            "zone",
            ["net", "0"],
            ["net_name", '""'],
            ["layers", "F&B.Cu"],
            ["tstamp", "4b23aa4c-b704-4f99-b8ee-66b834c9f1a2"],
            ["name", '"FOOBAR"'],
            ["hatch", "full", "0.508"],
            ["connect_pads", ["clearance", "0"]],
            ["min_thickness", "0.254"],
            [
                "keepout",
                ["tracks", "not_allowed"],
                ["vias", "not_allowed"],
                ["pads", "not_allowed"],
                ["copperpour", "allowed"],
                ["footprints", "allowed"],
            ],
            ["fill", ["thermal_gap", "0.508"], ["thermal_bridge_width", "0.508"]],
            [
                "polygon",
                [
                    "pts",
                    # ["xy", "367.386", "203.216"],
                ],
            ],
        ]

        slot = self.find_objects_by_atom(o, "pts", INF)

        pts = points_in_circumference(r, 30)
        for point in pts:
            rr = ["xy", point[0] + nx, point[1] + ny]
            slot[0].append(rr)

        root.append(o)

    def remove_atoms(self, parent, atom):
        while True:
            atoms = self.find_objects_by_atom(parent, atom, INF)
            if len(atoms) == 0:
                break

            parent.remove(atoms[0])

    def add_sd123_model(self, parent: list, path: str):
        o = [
            "model",
            '"${KIPRJMOD}/' + str(path) + 'SOD-diodes/SOD-123.step"',
            ["offset", ["xyz", "0", "0", "0"]],
            ["scale", ["xyz", "1", "1", "1"]],
            ["rotate", ["xyz", "0", "0", "0"]],
        ]
        parent.append(o)

    def add_switch_model(self, parent: list, path: str):
        o = [
            "model",
            '"${KIPRJMOD}/' + str(path) + '/cherry-mx-switches/asm_mx_asm_PCB.stp"',
            ["offset", ["xyz", "-2.1", "-4.5", "4"]],
            ["scale", ["xyz", "1", "1", "1"]],
            ["rotate", ["xyz", "-180", "0", "90"]],
        ]
        parent.append(o)

    def add_keycap_model(self, parent: list, url: str):
        o = [
            "model",
            f'"{url}"',
            ["offset", ["xyz", "-2.2", "-4.9", "10"]],
            ["scale", ["xyz", "0.4", "0.4", "0.4"]],
            ["rotate", ["xyz", "0", "0", "0"]],
        ]
        parent.append(o)
