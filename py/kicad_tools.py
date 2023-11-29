from decimal import Decimal
from enum import Enum
import copy
import math
from typing import Dict, List, cast
from attr import dataclass
from ki_symbols import KiSymbols, PinPosition, Wire
from sexptype import SexpListType, SexpType, SexpTypeValue, makeDecimal, makeString

INF = math.inf


@dataclass
class KeyGridInfo:
    grid_spacing: Decimal = Decimal(2.54)
    switch_origin_x: Decimal = grid_spacing * 60
    switch_origin_y: Decimal = grid_spacing * 10

    led_origin_x: Decimal = Decimal(1.27 * 3) + (grid_spacing * 8)  # grid_spacing
    led_origin_y: Decimal = switch_origin_y

    spacing_x: Decimal = grid_spacing * 5
    spacing_y: Decimal = grid_spacing * 6


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
    def __init__(
        self,
        x1: Decimal = Decimal(-1),
        y1: Decimal = Decimal(-1),
        x2: Decimal = Decimal(-1),
        y2: Decimal = Decimal(-1),
    ):

        if x1 == -1:
            self.x1 = Decimal("inf")
            self.y1 = Decimal("inf")
            self.x2 = Decimal("-inf")
            self.y2 = Decimal("-inf")
        else:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

    def update_xy(self, sx: str | Decimal, sy: str | Decimal) -> None:
        x = Decimal(sx)
        y = Decimal(sy)

        self.x1 = min(self.x1, x)
        self.y1 = min(self.y1, y)
        self.x2 = max(self.x2, x)
        self.y2 = max(self.y2, y)

    def add_border(self, n: Decimal) -> None:
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

    def find_objects_by_atom(
        self, root: SexpType, atom: str, maxDepth=float("inf")
    ) -> SexpListType:
        def _find_objects_by_atom_inner(
            array, atom, maxDepth, depth, out: SexpListType
        ):
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

    def find_object_by_atom(
        self, root: SexpType, atom: str, maxDepth=float("inf")
    ) -> SexpType:
        objs = self.find_objects_by_atom(root, atom, maxDepth)
        if len(objs) > 1:
            raise Exception(f"Found too many {atom}")
        if len(objs) == 0:
            raise Exception(f"Found zero {atom}")
        return objs[0]

    def find_footprint_by_reference(self, root: SexpType, ref: str) -> SexpType:
        prints = self.find_objects_by_atom(root, "footprint", 1)

        for p in prints:
            o = self.find_objects_by_atom(p, "fp_text", INF)
            filtered = filter(
                lambda fp: (fp[1] == "reference") and (fp[2] == q_string(ref)), o
            )

            lst = list(filtered)
            if len(lst) > 0:
                return p

        return []

    def _get_text_obj_by_type(self, root: SexpType, ref: str, type: str) -> SexpType:
        p = self.find_footprint_by_reference(root, ref)

        assert p is not None

        o = self.find_objects_by_atom(p, "fp_text", INF)
        filtered = filter(lambda fp: (fp[1] == type), o)
        obj = list(filtered)[0]
        return obj

    def set_hidden_footprint_text_by_reference(
        self, root: SexpType, ref: str, type: str, hidden: bool
    ) -> None:
        obj = self._get_text_obj_by_type(root, ref, type)

        # If it is already there, remove it.
        if "hide" in obj:
            obj.remove("hide")

        if hidden:
            obj.append("hide")

    def move_text_to_layer(
        self, root: SexpType, ref: str, type: str, layer: Layer
    ) -> None:
        obj = self._get_text_obj_by_type(root, ref, type)

        o = self.find_objects_by_atom(obj, "layer", INF)

        lst = list(o)
        lst[0][1] = layer

    def copy_to_back_silkscreen(self, root: SexpType, ref: str, type: str) -> None:
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

    def get_all_symbol_value_references(self, root: SexpType) -> Dict[str, List[str]]:
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
                value: str = makeString(value_property[2]).strip('"')
                reference: str = makeString(reference_property[2]).strip('"')

                if not value in ret:
                    ret[value] = []

                v = ret[value]
                v.append(reference)
        return ret

    def find_symbol_by_reference(
        self, root: SexpType, ref: str, unit="1"
    ) -> SexpType | None:
        symbols = self.find_objects_by_atom(root, "symbol", 1)

        for symbol in symbols:
            unit_objects = self.find_objects_by_atom(symbol, "property", INF)

            property_filtered = filter(
                lambda fp: (fp[1] == q_string("Reference"))
                and (fp[2] == q_string(ref)),
                unit_objects,
            )

            unit_objects = self.find_objects_by_atom(symbol, "unit", INF)

            is_unit_right = True

            if unit_objects is None:
                is_unit_right = True
            else:
                is_unit_right = unit_objects[0][1] == unit

            lst = list(property_filtered)
            if len(lst) > 0 and is_unit_right:
                return symbol
        return None

    def get_symbol_property(
        self, root: SexpType, ref: str, prop: str, default: str
    ) -> SexpTypeValue:
        symbol = cast(list, self.find_symbol_by_reference(root, ref))

        o = self.find_objects_by_atom(symbol, "property", INF)

        filtered = filter(lambda fp: (fp[1] == q_string(prop)), o)
        lst = list(filtered)
        if len(lst) > 0:
            return lst[0][2]
        else:
            return default

    def get_symbol_property_as_decimal(
        self, root: SexpType, ref: str, prop: str, default
    ) -> Decimal:
        r = self.get_symbol_property(root, ref, prop, default)
        r = str(r)
        return Decimal(r.strip('"'))

    def find_footprint_at_by_reference(self, root: SexpType, ref: str) -> SexpType:
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
        self,
        root: SexpType,
        ref: str,
        x: Decimal,
        y: Decimal,
        rot: Decimal = Decimal(0),
    ) -> None:
        footprint = self.find_footprint_by_reference(root, ref)

        cat = self.find_footprint_at_by_reference(root, ref)

        current_rot = makeDecimal(cat[3])
        # If the object is already rotated, then un-rotate it
        if current_rot != 0:
            cat[3] = str(makeDecimal(cat[3]) - current_rot)
            self.set_object_location(root, ref, x, y, -current_rot)

        all_ats = self.find_objects_by_atom(footprint, "at", INF)
        for at1 in all_ats:
            while len(at1) < 4:
                at1.append("0")  # If there isn't a rotation, add it.

            at1_x = makeDecimal(at1[1])
            at1_y = makeDecimal(at1[2])
            at1_rot = makeDecimal(at1[3])

            while len(at1) > 0:
                at1.pop()

            at1.append("at")
            at1.append(str(at1_x))
            at1.append(str(at1_y))
            at1.append(str(at1_rot + rot))

        # Set the primary location and rotation
        at = self.find_footprint_at_by_reference(root, ref)
        if at is None:
            raise Exception("Could not find" + ref)
        else:
            at.append("0")
            old_rot = at[3]
            while len(at) > 0:
                at.pop()

            at.append("at")
            at.append(str(x))
            at.append(str(y))
            at.append(str(rot))

    def add_bounding_box(
        self, root: SexpType, box: BoundingBox, width: float, layer: Layer
    ) -> None:
        _box: SexpType = [
            "gr_rect",
            ["start", str(box.x1), str(box.y1)],
            ["end", str(box.x2), str(box.y2)],
            ["layer", layer],
            ["width", str(width)],
            ["fill", "none"],
        ]

        root.append(_box)

    def get_bounding_box_of_layer_lines(
        self, root: SexpType, layerName: Layer
    ) -> BoundingBox:
        lines = []

        g_lines = self.find_objects_by_atom(root, "fp_line", float("inf"))
        at = self.find_objects_by_atom(root, "at", 1)

        origin_x = makeDecimal(at[0][1])
        origin_y = makeDecimal(at[0][2])

        for g_line in g_lines:
            layers = self.find_objects_by_atom(g_line, "layer", float("inf"))
            for layer in layers:
                if layer[1] == layerName:
                    lines.append(g_line)

        box = BoundingBox(Decimal(-1), Decimal(-1), Decimal(-1), Decimal(-1))
        for line in lines:
            start = self.find_object_by_atom(line, "start", float("inf"))
            end = self.find_object_by_atom(line, "end", float("inf"))

            x1 = makeDecimal(start[1])
            y1 = makeDecimal(start[2])
            x2 = makeDecimal(end[1])
            y2 = makeDecimal(end[2])

            box.update_xy(x1 + origin_x, y1 + origin_y)
            box.update_xy(x2 + origin_x, y2 + origin_y)

        return box

    def draw_circle(
        self,
        root: SexpType,
        layer: Layer,
        x: Decimal,
        y: Decimal,
        r: Decimal,
        fill: str,
    ) -> None:
        o: SexpType = [
            "gr_circle",
            ["center", str(x), str(y)],
            ["end", str(x), str(y - r)],
            ["layer", layer],
            ["width", "0.2"],
            ["fill", fill],
        ]

        root.append(o)

    def move_recursive(self, root: SexpType, mx: Decimal, my: Decimal, mr: int) -> None:
        first_at = self.find_object_by_atom(root, "at", 1)
        while len(first_at) < 4:
            first_at.append("0")

        at_x = makeDecimal(first_at[1])
        at_y = makeDecimal(first_at[2])
        at_r = makeDecimal(first_at[3])

        all_at = self.find_objects_by_atom(root, "at", math.inf)
        for atm in all_at:
            while len(atm) != 4:
                atm.append("0")

            atm[1] = str(makeDecimal(atm[1]) - at_x + mx)
            atm[2] = str(makeDecimal(atm[2]) - at_y + my)
            atm[3] = str(makeDecimal(atm[3]) - at_r + mr)

    def get_relative_pin_position_for_schematic(
        self, schematic_root: SexpType, obj: SexpType, type: str, value: str
    ) -> list[Decimal]:
        item_lib_id = self.find_object_by_atom(obj, "lib_id")

        lib_symbols = self.find_object_by_atom(schematic_root, "lib_symbols")
        symbols = self.find_objects_by_atom(lib_symbols, "symbol", 1)

        for symbol in symbols:
            if item_lib_id[1] == symbol[1]:
                pins = self.find_objects_by_atom(symbol, "pin")
                symbol_at = self.find_object_by_atom(obj, "at", 1)
                symbol_rotation = makeDecimal(symbol_at[3])

                for pin in pins:
                    match = self.find_object_by_atom(pin, type)
                    pin_value = match[1]
                    if pin_value == q_string(value):
                        pin_at = self.find_object_by_atom(pin, "at", 1)

                        dx = makeDecimal(pin_at[1])
                        dy = makeDecimal(pin_at[2])

                        if symbol_rotation == 0:
                            return [dx, dy]
                        if symbol_rotation == 90:
                            return [dy, -dx]
                        if symbol_rotation == 180:
                            return [-dx, dy]
                        if symbol_rotation == 270:
                            return [dy, dx]

        return [Decimal(0), Decimal(0)]

    def _get_key_grid_info(self):
        pass

    def add_keyswitch_to_schematic(
        self,
        designator: str,
        name: str,
        key_root: SexpType,
        mx: int,
        my: int,
        size: Decimal,
    ) -> None:
        key_grid_info = KeyGridInfo()

        symbol_diode = KiSymbols.get_diode("D" + designator, name)
        # symbol_switch = KiSymbols.get_mx_with_led("SW" + designator, name)
        symbol_switch = KiSymbols.get_mxfull_switch("SW" + designator, name, size)
        symbol_switch_led = KiSymbols.get_mxfull_led("SW" + designator, name)

        cluster_x = key_grid_info.switch_origin_x + (mx * key_grid_info.spacing_x)
        cluster_y = key_grid_info.switch_origin_y + (my * key_grid_info.spacing_y)

        diode_x = cluster_x - (key_grid_info.grid_spacing * 2)
        diode_y = cluster_y + (key_grid_info.grid_spacing * 1)

        led_x = key_grid_info.led_origin_x + (mx * key_grid_info.spacing_x)
        led_y = key_grid_info.led_origin_y + (my * key_grid_info.spacing_y)

        self.move_recursive(symbol_switch, cluster_x, cluster_y, 0)
        self.move_recursive(symbol_diode, diode_x, diode_y, 90)
        self.move_recursive(symbol_switch_led, led_x, led_y, 0)

        key_root.append(symbol_switch)
        key_root.append(symbol_diode)
        key_root.append(symbol_switch_led)

    def rotate_matrix(self, m):
        # return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]

        list_of_tuples = zip(*m[::-1])
        return [list(elem) for elem in list_of_tuples]

    def process_pin_pair(
        self,
        designator_type: str,
        pin_type: str,
        pin_type_id: str,
        unit: str,
        root: SexpType,
        designator1: int,
        designator2: int,
    ) -> Wire | None:
        part1_ref = f"{designator_type}{designator1}"
        part2_ref = f"{designator_type}{designator2}"

        part1_sym = self.find_symbol_by_reference(root, part1_ref, unit)
        part2_sym = self.find_symbol_by_reference(root, part2_ref, unit)

        if part1_sym is not None and part2_sym is not None:

            at1 = self.find_object_by_atom(part1_sym, "at", 1)
            at2 = self.find_object_by_atom(part2_sym, "at", 1)

            pin_offset1 = self.get_relative_pin_position_for_schematic(
                root, part1_sym, pin_type, pin_type_id
            )
            pin_offset2 = self.get_relative_pin_position_for_schematic(
                root, part2_sym, pin_type, pin_type_id
            )

            x1 = makeDecimal(at1[1]) + pin_offset1[0]
            y1 = makeDecimal(at1[2]) + pin_offset1[1]

            x2 = makeDecimal(at2[1]) + pin_offset2[0]
            y2 = makeDecimal(at2[2]) + pin_offset2[1]

            pin1 = PinPosition(x1, y1)
            pin2 = PinPosition(x2, y2)

            w = Wire(pin1, pin2)
            return w
        return None

    def get_wire_positions_list(
        self,
        designator_type: str,
        pin_type: str,
        pin_type_id: str,
        unit: str,
        root: SexpType,
        matrix: list[list[int]],
    ) -> list[Wire]:
        """
        Get wire pair combonations -- we are matching from
        the same pin number on the same type of designator
        (for instance, "SW" and pin "2").   This will return
        a row-by-row combo of all the wires that would jump
        between matching pairs.
        """
        wires: list[Wire] = []

        for row_idx in range(len(matrix)):
            row = matrix[row_idx]
            row2 = row[::-1]

            """
            When using the rotated matrix, the edge was not getting
            picked.  So we rotate the row values and run a second
            time.  This gives us some duplicated reversed lines in
            the output but we'll detect/clean those up later.
            """
            for direction in range(2):
                for col_idx in range(len(row) - 1):

                    designator1 = row[col_idx]
                    designator2 = row[col_idx + 1]

                    if direction == 1:
                        designator1 = row2[col_idx]
                        designator2 = row2[col_idx + 1]

                    w = self.process_pin_pair(
                        designator_type,
                        pin_type,
                        pin_type_id,
                        unit,
                        root,
                        designator1,
                        designator2,
                    )
                    if w is not None:
                        wires.append(w)

        return wires

    def calculate_wire_offset(
        self, wire: Wire, led_x_offset: Decimal, led_y_offset: Decimal
    ) -> tuple[Wire, Wire]:
        new_wire = Wire(
            PinPosition(wire.start.x, wire.start.y), PinPosition(wire.end.x, wire.end.y)
        )
        connector_wire = Wire(
            PinPosition(wire.start.x, wire.start.y), PinPosition(wire.end.x, wire.end.y)
        )

        new_wire.start.x += led_x_offset
        new_wire.start.y += led_y_offset

        new_wire.end.x += led_x_offset
        new_wire.end.y += led_y_offset

        connector_wire.end = new_wire.start
        return (new_wire, connector_wire)

    def add_wires_to_schematic(self, root: SexpType, matrix: list[list[int]]) -> None:
        """
        Add all the needed wires to the schematic.  This routine also adjusts
        for when you need to run a wire close to the part and use a short
        connector to bridge the gap.
        """

        key_grid_info = KeyGridInfo()
        led_y_offset = key_grid_info.grid_spacing * 2
        led_x_offset = key_grid_info.grid_spacing * 1

        matrix_rotated = self.rotate_matrix(matrix)

        all_wires: list[Wire] = []

        UNIT_1 = "1"
        UNIT_2 = "2"

        switch_row_wires: list[Wire] = self.get_wire_positions_list(
            "D", "number", "1", UNIT_1, root, matrix
        )
        switch_col_wires: list[Wire] = self.get_wire_positions_list(
            "SW", "number", "2", UNIT_1, root, matrix_rotated
        )

        led_row_wires: list[Wire] = self.get_wire_positions_list(
            "SW", "number", "3", UNIT_2, root, matrix
        )

        led_col_wires: list[Wire] = self.get_wire_positions_list(
            "SW", "number", "4", UNIT_2, root, matrix_rotated
        )
        led_col_connect: list[Wire] = []
        led_col_fixed: list[Wire] = []

        led_row_connect: list[Wire] = []
        led_row_fixed: list[Wire] = []

        for i in led_row_wires:
            (led_row_wire, led_row_connector) = self.calculate_wire_offset(
                i, Decimal(0), led_y_offset
            )
            led_row_fixed.append(led_row_wire)
            led_row_connect.append(led_row_connector)

        for i in led_col_wires:
            (led_col_wire, led_col_connector) = self.calculate_wire_offset(
                i, led_x_offset, Decimal(0)
            )
            led_col_fixed.append(led_col_wire)
            led_col_connect.append(led_col_connector)

        all_wires = (
            []
            + switch_row_wires
            + switch_col_wires
            + led_col_fixed
            + led_col_connect
            + led_row_fixed
            + led_row_connect
        )

        for wire in all_wires:
            wirec = KiSymbols.get_wire(wire)
            root.append(wirec)

    def draw_keepout_zone(
        self, root: SexpType, nx: Decimal, ny: Decimal, r: Decimal
    ) -> None:
        self.draw_circle(root, Layer.F_Silkscreen, nx, ny, r, "none")
        self.draw_circle(root, Layer.B_Silkscreen, nx, ny, r, "none")

        def points_in_circumference(r: float, n=100):
            pi = math.pi

            return [
                (math.cos(2 * pi / n * x) * r, math.sin(2 * pi / n * x) * r)
                for x in range(0, n + 1)
            ]

        o: SexpType = [
            "zone",
            ["net", "0"],
            ["net_name", '""'],
            ["layers", "F&B.Cu"],
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

        pts = points_in_circumference(float(r), 30)
        for point in pts:
            rr: SexpType = ["xy", str(point[0] + float(nx)), str(point[1] + float(ny))]
            slot[0].append(rr)

        foo = [
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
                    ["xy", "347.9875", "274.5"],
                    ["xy", "347.8563856044028", "275.7474701449066"],
                    ["xy", "347.46877274585563", "276.9404198584548"],
                    ["xy", "346.8416019662497", "278.02671151375483"],
                    ["xy", "346.0022836381532", "278.95886895286435"],
                    ["xy", "344.9875", "279.69615242270663"],
                    ["xy", "343.8416019662497", "280.2063390977709"],
                    ["xy", "342.61467077960594", "280.4671313722096"],
                    ["xy", "341.3603292203941", "280.4671313722096"],
                    ["xy", "340.1333980337503", "280.2063390977709"],
                    ["xy", "338.9875", "279.69615242270663"],
                    ["xy", "337.9727163618469", "278.95886895286435"],
                    ["xy", "337.1333980337503", "278.02671151375483"],
                    ["xy", "336.5062272541444", "276.9404198584548"],
                    ["xy", "336.1186143955972", "275.7474701449066"],
                    ["xy", "335.9875", "274.5"],
                    ["xy", "336.1186143955972", "273.2525298550934"],
                    ["xy", "336.5062272541444", "272.0595801415452"],
                    ["xy", "337.1333980337503", "270.97328848624517"],
                    ["xy", "337.97271636184684", "270.04113104713565"],
                    ["xy", "338.9875", "269.30384757729337"],
                    ["xy", "340.1333980337503", "268.7936609022291"],
                    ["xy", "341.3603292203941", "268.5328686277904"],
                    ["xy", "342.61467077960594", "268.5328686277904"],
                    ["xy", "343.8416019662497", "268.7936609022291"],
                    ["xy", "344.9875", "269.30384757729337"],
                    ["xy", "346.00228363815313", "270.04113104713565"],
                    ["xy", "346.8416019662497", "270.97328848624517"],
                    ["xy", "347.46877274585563", "272.0595801415452"],
                    ["xy", "347.8563856044028", "273.2525298550934"],
                    ["xy", "347.9875", "274.5"],
                ],
            ],
        ]

        root.append(o)

    def remove_atoms(self, parent: SexpType, atom: str) -> None:
        while True:
            atoms = self.find_objects_by_atom(parent, atom, 1)
            if len(atoms) == 0:
                break

            parent.remove(atoms[0])

    def add_sd123_model(self, parent: SexpType, path: str) -> None:
        o: SexpType = [
            "model",
            '"${KIPRJMOD}/' + str(path) + 'SOD-diodes/SOD-123.step"',
            ["offset", ["xyz", "0", "0", "0"]],
            ["scale", ["xyz", "1", "1", "1"]],
            ["rotate", ["xyz", "0", "0", "0"]],
        ]
        parent.append(o)

    def add_switch_model(self, parent: SexpType, path: str) -> None:
        o: SexpType = [
            "model",
            '"${KIPRJMOD}/' + str(path) + '/cherry-mx-switches/asm_mx_asm_PCB.stp"',
            ["offset", ["xyz", "0", "0", "4"]],
            ["scale", ["xyz", "1", "1", "1"]],
            ["rotate", ["xyz", "-180", "0", "90"]],
        ]
        parent.append(o)

    def add_keycap_model(self, parent: SexpType, url: str) -> None:
        o: SexpType = [
            "model",
            f'"{url}"',
            ["offset", ["xyz", "0", "0", "6"]],
            ["scale", ["xyz", "0.4", "0.4", "0.4"]],
            ["rotate", ["xyz", "0", "0", "0"]],
        ]
        parent.append(o)
