from decimal import Decimal
from enum import Enum, IntEnum
import copy
import math
from typing import Dict, List, Optional, cast
from attr import dataclass
from ki_symbols import KiSymbols, PinPosition, Wire
from sexptype import (
    PinNumber,
    PinType,
    SexpListType,
    SexpType,
    SexpTypeValue,
    UnitNumber,
    makeDecimal,
    makeString,
)


@dataclass
class KeyGridInfo:
    grid_spacing: Decimal = Decimal(2.54)
    switch_origin_x: Decimal = grid_spacing * 67
    switch_origin_y: Decimal = grid_spacing * 12

    led_origin_x: Decimal = Decimal(1.27 * 3) + (grid_spacing * 13)  # grid_spacing
    led_origin_y: Decimal = switch_origin_y

    spacing_x: Decimal = grid_spacing * 5
    spacing_y: Decimal = grid_spacing * 6

    led_y_offset: Decimal = grid_spacing * 2
    led_x_offset: Decimal = grid_spacing * 1


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
        x1: Optional[Decimal] = None,
        y1: Optional[Decimal] = None,
        x2: Optional[Decimal] = None,
        y2: Optional[Decimal] = None,
    ):
        if x1 is None or y1 is None or x2 is None or y2 is None:
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


class QueryRecursionLevel(IntEnum):
    HERE = 0
    DEEP = 1


class KicadTool:
    def find_objects_by_foo(
        self, root: SexpType, query: SexpTypeValue, recursionLevel: QueryRecursionLevel
    ) -> SexpListType:
        def _find_objects_by_atom_inner(
            local_root: SexpType,
            query: SexpTypeValue,
            maxDepth,
            depth,
            out: SexpListType,
        ):
            for top in local_root:
                if top is None or query is None:
                    continue

                # If it is too small, no way it can match
                if len(top) < len(query):
                    continue

                match = True

                for i in range(len(query)):
                    bit = query[i]
                    local_bit = top

                    if isinstance(bit, str) and isinstance(local_bit, str):
                        if local_bit != bit:
                            match = False

                    if isinstance(bit, str) and isinstance(local_bit, list):
                        if bit != local_bit[i]:
                            match = False

                    if isinstance(bit, list):
                        s = str(top)

                        if isinstance(top, list):
                            res = self.find_objects_by_foo(
                                top, bit, QueryRecursionLevel.HERE
                            )
                            if len(res) == 0:
                                match = False

                if (match) and isinstance(top, list):
                    out.append(top)

                if depth < maxDepth and isinstance(top, list):
                    _find_objects_by_atom_inner(top, query, maxDepth, depth + 1, out)
            return out

        out: SexpListType = []
        maxDepth = 1 if recursionLevel == QueryRecursionLevel.HERE else math.inf

        _find_objects_by_atom_inner([root], query, maxDepth, 0, out)
        return out

    def find_objects_by_atom(
        self, root: SexpType, atom: str, recursionLevel: QueryRecursionLevel
    ) -> SexpListType:
        return self.find_objects_by_foo(root, [atom], recursionLevel)

    def find_object_by_atom(
        self, root: SexpType, atom: str, recursionLevel: QueryRecursionLevel
    ) -> SexpType:
        objs = self.find_objects_by_atom(root, atom, recursionLevel)
        if len(objs) > 1:
            raise Exception(f"Found too many {atom}")
        if len(objs) == 0:
            raise Exception(f"Found zero {atom}")
        return objs[0]

    def find_footprint_by_reference(self, root: SexpType, ref: str) -> SexpType:
        l = self.find_objects_by_foo(
            root,
            ["footprint", ["fp_text", "reference", '"' + ref + '"']],
            QueryRecursionLevel.HERE,
        )
        if isinstance(l, list) and len(l) > 0:
            return l[0]
        return []

    def _get_text_obj_by_type(self, root: SexpType, ref: str, type: str) -> SexpType:
        p = self.find_footprint_by_reference(root, ref)

        assert p is not None

        o = self.find_objects_by_atom(p, "fp_text", QueryRecursionLevel.DEEP)
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

        o = self.find_objects_by_atom(obj, "layer", QueryRecursionLevel.DEEP)

        lst = list(o)
        lst[0][1] = layer

    def copy_to_back_silkscreen(self, root: SexpType, ref: str, type: str) -> None:
        p = self.find_footprint_by_reference(root, ref)
        assert p is not None

        obj = self._get_text_obj_by_type(root, ref, type)
        nn = copy.deepcopy(obj)

        layerObject = self.find_objects_by_atom(nn, "layer", QueryRecursionLevel.DEEP)

        lst = list(layerObject)
        lst[0][1] = Layer.B_Silkscreen
        nn[1] = "user"

        effectsObject = self.find_objects_by_atom(
            nn, "effects", QueryRecursionLevel.DEEP
        )

        effectsList = list(effectsObject)
        effectsList[0].append(["justify", "mirror"])

        p.append(nn)

    def get_all_symbol_value_references(self, root: SexpType) -> Dict[str, List[str]]:
        ret: Dict[str, List[str]] = dict()

        symbols = self.find_objects_by_atom(root, "symbol", QueryRecursionLevel.HERE)

        for symbol in symbols:
            properties = self.find_objects_by_atom(
                symbol, "property", QueryRecursionLevel.HERE
            )

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
        self, root: SexpType, ref: str, unit=UnitNumber.ONE
    ) -> SexpType | None:

        unitstr = "1"
        if unit == UnitNumber.TWO:
            unitstr = "2"

        z: SexpTypeValue = [
            "symbol",
            ["unit", unitstr],
            [
                "property",
                '"Reference"',
                q_string(ref),
            ],
        ]

        l1 = self.find_objects_by_foo(
            root,
            z,
            QueryRecursionLevel.HERE,
        )

        if len(l1) == 0:
            return None

        return l1[0]

    def get_symbol_property(
        self, root: SexpType, ref: str, prop: str, default: str
    ) -> SexpTypeValue:
        symbol = self.find_symbol_by_reference(root, ref)
        if symbol is None:
            raise Exception("get_symbol_property: Symbol not found " + ref)

        o = self.find_objects_by_atom(symbol, "property", QueryRecursionLevel.DEEP)

        filtered = filter(lambda fp: (fp[1] == q_string(prop)), o)
        lst = list(filtered)
        if len(lst) > 0:
            return lst[0][2]
        else:
            return default

    def find_footprint_at_by_reference(self, root: SexpType, ref: str) -> SexpType:
        footprint = self.find_footprint_by_reference(root, ref)
        assert footprint is not None

        o = self.find_object_by_atom(footprint, "at", QueryRecursionLevel.HERE)

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
        ref_rot: Decimal | None = None,
    ) -> None:
        footprint = self.find_footprint_by_reference(root, ref)

        cat = self.find_footprint_at_by_reference(root, ref)

        current_rot = makeDecimal(cat[3])
        # If the object is already rotated, then un-rotate it
        if current_rot != 0:
            cat[3] = str(makeDecimal(cat[3]) - current_rot)
            rrot2 = None
            if ref_rot is not None:
                rrot2 = -ref_rot

            self.set_object_location(root, ref, x, y, -current_rot, rrot2)

        all_ats = self.find_objects_by_atom(footprint, "at", QueryRecursionLevel.HERE)
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

        if ref_rot is not None:
            obj = self.find_footprint_by_reference(root, ref)
            if obj is None:
                raise Exception("Could not find" + ref)

            reference_scode = self.find_objects_by_atom(
                obj, "fp_text", QueryRecursionLevel.HERE
            )
            for s in reference_scode:
                if s[1] == "reference":
                    text_at = self.find_object_by_atom(
                        s, "at", QueryRecursionLevel.HERE
                    )
                    if isinstance(text_at, list):
                        while len(text_at) < 4:
                            text_at.append("0")
                        text_at[3] = str(ref_rot)

        # Set the primary location and rotation
        at = self.find_footprint_at_by_reference(root, ref)
        if at is None:
            raise Exception("Could not find" + ref)

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

        g_lines = self.find_objects_by_atom(root, "fp_line", QueryRecursionLevel.DEEP)
        at = self.find_objects_by_atom(root, "at", QueryRecursionLevel.HERE)

        origin_x = makeDecimal(at[0][1])
        origin_y = makeDecimal(at[0][2])

        for g_line in g_lines:
            layers = self.find_objects_by_atom(
                g_line, "layer", QueryRecursionLevel.DEEP
            )
            for layer in layers:
                if layer[1] == layerName:
                    lines.append(g_line)

        box = BoundingBox()
        for line in lines:
            start = self.find_object_by_atom(line, "start", QueryRecursionLevel.DEEP)
            end = self.find_object_by_atom(line, "end", QueryRecursionLevel.DEEP)

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
        first_at = self.find_object_by_atom(root, "at", QueryRecursionLevel.HERE)
        while len(first_at) < 4:
            first_at.append("0")

        at_x = makeDecimal(first_at[1])
        at_y = makeDecimal(first_at[2])
        at_r = makeDecimal(first_at[3])

        all_at = self.find_objects_by_atom(root, "at", QueryRecursionLevel.DEEP)
        for atm in all_at:
            while len(atm) != 4:
                atm.append("0")

            atm[1] = str(makeDecimal(atm[1]) - at_x + mx)
            atm[2] = str(makeDecimal(atm[2]) - at_y + my)
            atm[3] = str(makeDecimal(atm[3]) - at_r + mr)

    def get_absolute_pin_position_for_schematic(
        self,
        root: SexpType,
        ref: str,
        pin_type: PinType,
        pin_type_id: PinNumber,
        unit: UnitNumber,
    ) -> PinPosition:

        symbol = self.find_symbol_by_reference(root, ref, unit)

        if symbol is None:
            raise Exception("Could not find " + ref)

        at = self.find_object_by_atom(symbol, "at", QueryRecursionLevel.HERE)

        pin_offset1 = self.get_relative_pin_position_for_schematic(
            root, symbol, pin_type, pin_type_id
        )

        x = makeDecimal(at[1]) + pin_offset1[0]
        y = makeDecimal(at[2]) + pin_offset1[1]

        pin1 = PinPosition(x, y, ref, pin_type, pin_type_id)

        return pin1

    def get_relative_pin_position_for_schematic(
        self, schematic_root: SexpType, obj: SexpType, type: PinType, value: PinNumber
    ) -> list[Decimal]:

        pin_number = 1
        if value == PinNumber._1:
            pin_number = 1

        if value == PinNumber._2:
            pin_number = 2

        if value == PinNumber._3:
            pin_number = 3

        if value == PinNumber._4:
            pin_number = 4

        item_lib_id = self.find_object_by_atom(obj, "lib_id", QueryRecursionLevel.HERE)

        lib_symbols = self.find_object_by_atom(
            schematic_root, "lib_symbols", QueryRecursionLevel.DEEP
        )
        symbols = self.find_objects_by_atom(
            lib_symbols, "symbol", QueryRecursionLevel.HERE
        )

        for symbol in symbols:
            if item_lib_id[1] == symbol[1]:
                pins = self.find_objects_by_atom(
                    symbol, "pin", QueryRecursionLevel.DEEP
                )
                symbol_at = self.find_object_by_atom(
                    obj, "at", QueryRecursionLevel.HERE
                )
                symbol_rotation = makeDecimal(symbol_at[3])

                for pin in pins:
                    if type != PinType.NUMBER:
                        raise Exception("Can only handle number pin type right now")

                    match = self.find_object_by_atom(
                        pin, "number", QueryRecursionLevel.DEEP
                    )
                    pin_value = match[1]
                    if pin_value == q_string(str(pin_number)):
                        pin_at = self.find_object_by_atom(
                            pin, "at", QueryRecursionLevel.HERE
                        )

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

        raise Exception("Could not find pin offset")

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
        do_not_populate: bool,
    ) -> None:
        key_grid_info = KeyGridInfo()

        symbol_diode = KiSymbols.get_diode("D" + designator, name)
        # symbol_switch = KiSymbols.get_mx_with_led("SW" + designator, name)
        symbol_switch = KiSymbols.get_mxfull_switch("SW" + designator, name, size)
        symbol_switch_led = KiSymbols.get_mxfull_led("SW" + designator, name)

        if do_not_populate:
            for sym in [symbol_diode, symbol_switch, symbol_switch_led]:
                dnp = self.find_object_by_atom(sym, "dnp", QueryRecursionLevel.HERE)
                dnp[1] = "yes"
                in_bom = self.find_object_by_atom(
                    sym, "in_bom", QueryRecursionLevel.HERE
                )
                in_bom[1] = "no"
                on_board = self.find_object_by_atom(
                    sym, "on_board", QueryRecursionLevel.HERE
                )
                on_board[1] = "no"

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

    def rotate_matrix(self, m: list[list[int]]):
        return [list(row) for row in zip(*m)]

    def process_pin_pair(
        self,
        designator_type: str,
        pin_type: PinType,
        pin_type_id: PinNumber,
        unit: UnitNumber,
        root: SexpType,
        designator1: int,
        designator2: int,
    ) -> Wire | None:
        part1_ref = f"{designator_type}{designator1}"
        part2_ref = f"{designator_type}{designator2}"

        part1_sym = self.find_symbol_by_reference(root, part1_ref, unit)
        part2_sym = self.find_symbol_by_reference(root, part2_ref, unit)

        if part1_sym is None or part2_sym is None:
            return None

        pin2 = self.get_absolute_pin_position_for_schematic(
            root,
            part2_ref,
            pin_type,
            pin_type_id,
            unit,
        )

        pin1 = self.get_absolute_pin_position_for_schematic(
            root,
            part1_ref,
            pin_type,
            pin_type_id,
            unit,
        )

        w = Wire(pin1, pin2)
        return w

    def get_wire_positions_list(
        self,
        designator_type: str,
        pin_type: PinType,
        pin_type_id: PinNumber,
        unit: UnitNumber,
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

        start_pin = wire.start.copy()
        end_pin = wire.end.copy()
        connector_wire = Wire(wire.start, wire.end)

        new_wire = Wire(start_pin.copy(), end_pin.copy())
        new_wire.start.x += led_x_offset
        new_wire.start.y += led_y_offset

        new_wire.end.x += led_x_offset
        new_wire.end.y += led_y_offset

        connector_wire.end = new_wire.start
        return (new_wire, connector_wire)

    def wires_to_pin_list(self, all_wires: list[Wire]) -> list[PinPosition]:
        pin_list: list[PinPosition] = []
        for wire in all_wires:
            pin_list.append(wire.start)
            pin_list.append(wire.end)

        return pin_list

    def first_positive_in_rows(self, matrix: list[list[int]]):
        first_positives: list[int] = []
        for row in matrix:
            first_positive = next((num for num in row if num > 0), None)
            if first_positive is None:
                first_positives.append(-1)
            else:
                first_positives.append(first_positive)
        return first_positives

    def _add_schematic_global_labels(
        self,
        root: SexpType,
        matrix_normal: list[list[int]],
        matrix_rotated: list[list[int]],
        wires: list[Wire],
        key_grid_info: KeyGridInfo,
    ):
        new_wires: list[Wire] = []

        @dataclass
        class GlobalTagInfo:
            des_prefix: str
            global_label_prefix: str
            pin_number: PinNumber
            UnitNumber: UnitNumber
            x1_offset: Decimal
            y1_offset: Decimal
            x2_offset: Decimal
            y2_offset: Decimal

        row_global_label_info: List[GlobalTagInfo] = [
            GlobalTagInfo(
                "D",
                "SW_ROW",
                PinNumber._1,
                UnitNumber.ONE,
                Decimal(0),
                Decimal(0),
                -key_grid_info.grid_spacing,
                Decimal(0),
            ),
            GlobalTagInfo(
                "SW",
                "LED_ROW",
                PinNumber._3,
                UnitNumber.TWO,
                Decimal(0),
                key_grid_info.led_y_offset,
                -key_grid_info.grid_spacing,
                Decimal(0),
            ),
        ]

        column_global_label_info: List[GlobalTagInfo] = [
            GlobalTagInfo(
                "SW",
                "SW_COL",
                PinNumber._2,
                UnitNumber.ONE,
                Decimal(0),
                Decimal(0),
                Decimal(0),
                -key_grid_info.grid_spacing * 4,
            ),
            GlobalTagInfo(
                "SW",
                "LED_COL",
                PinNumber._4,
                UnitNumber.TWO,
                key_grid_info.led_x_offset,
                Decimal(0),
                Decimal(0),
                -key_grid_info.grid_spacing * 4,
            ),
        ]

        def place_global_labels(idx: int, des: int, global_labels: List[GlobalTagInfo]):
            for global_label in global_labels:
                ref = global_label.des_prefix + str(des)

                p1 = self.get_absolute_pin_position_for_schematic(
                    root,
                    ref,
                    PinType.NUMBER,
                    global_label.pin_number,
                    global_label.UnitNumber,
                )

                p1.x += global_label.x1_offset
                p1.y += global_label.y1_offset

                p2 = p1.copy()
                p1.x += global_label.x2_offset
                p1.y += global_label.y2_offset
                new_wire = Wire(p1, p2)
                new_wires.append(new_wire)

                global_label_symbol = KiSymbols.get_global_label(
                    f"{global_label.global_label_prefix}{idx+1}"
                )
                self.move_recursive(global_label_symbol, p1.x, p1.y, 180)
                root.append(global_label_symbol)

        first_in_row = self.first_positive_in_rows(matrix_normal)
        first_in_col = self.first_positive_in_rows(matrix_rotated)

        for refnum_idx in enumerate(first_in_row):
            (idx, ref_num) = refnum_idx

            place_global_labels(idx, ref_num, row_global_label_info)

        for refnum_idx in enumerate(first_in_col):
            (idx, ref_num) = refnum_idx
            place_global_labels(idx, ref_num, column_global_label_info)

        wires += new_wires

    def add_wires_to_schematic(self, root: SexpType, matrix: list[list[int]]) -> None:
        """
        Add all the needed wires to the schematic.  This routine also adjusts
        for when you need to run a wire close to the part and use a short
        connector to bridge the gap.
        """

        key_grid_info = KeyGridInfo()

        matrix_rotated = self.rotate_matrix(matrix)

        all_wires: list[Wire] = []

        switch_row_wires: list[Wire] = self.get_wire_positions_list(
            "D", PinType.NUMBER, PinNumber._1, UnitNumber.ONE, root, matrix
        )
        switch_col_wires: list[Wire] = self.get_wire_positions_list(
            "SW", PinType.NUMBER, PinNumber._2, UnitNumber.ONE, root, matrix_rotated
        )

        led_row_wires: list[Wire] = self.get_wire_positions_list(
            "SW", PinType.NUMBER, PinNumber._3, UnitNumber.TWO, root, matrix
        )

        led_col_wires: list[Wire] = self.get_wire_positions_list(
            "SW", PinType.NUMBER, PinNumber._4, UnitNumber.TWO, root, matrix_rotated
        )
        led_col_connect: list[Wire] = []
        led_col_fixed: list[Wire] = []

        led_row_connect: list[Wire] = []
        led_row_fixed: list[Wire] = []

        for i in led_row_wires:
            (led_row_wire, led_row_connector) = self.calculate_wire_offset(
                i, Decimal(0), key_grid_info.led_y_offset
            )
            led_row_fixed.append(led_row_wire)
            led_row_connect.append(led_row_connector)

        for i in led_col_wires:
            (led_col_wire, led_col_connector) = self.calculate_wire_offset(
                i, key_grid_info.led_x_offset, Decimal(0)
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

        self._add_schematic_global_labels(
            root, matrix, matrix_rotated, all_wires, key_grid_info
        )

        for wire in all_wires:
            wirec = KiSymbols.get_wire(wire)
            # if wire.type == WireType.GLOBAL:
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

        slot = self.find_objects_by_atom(o, "pts", QueryRecursionLevel.DEEP)

        pts = points_in_circumference(float(r), 30)
        for point in pts:
            rr: SexpType = ["xy", str(point[0] + float(nx)), str(point[1] + float(ny))]
            slot[0].append(rr)

        root.append(o)

    def remove_atoms(self, parent: SexpType, atom: str) -> None:
        while True:
            atoms = self.find_objects_by_atom(parent, atom, QueryRecursionLevel.HERE)
            if len(atoms) == 0:
                break

            parent.remove(atoms[0])

    def add_sd123_model(self, parent: SexpType, path: str) -> None:
        o: SexpType = [
            "model",
            '"${KIPRJMOD}/' + str(path) + '/SOD-diodes/SOD-123.step"',
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
