from decimal import Decimal
from attr import dataclass

from sexptype import PinNumber, PinType, SexpType


@dataclass
class PinPosition:
    x: Decimal
    y: Decimal
    reference: str
    pin_type: PinType
    pin_id: PinNumber

    def copy(self) -> "PinPosition":
        """Create a copy of this PinPosition instance."""
        return PinPosition(self.x, self.y, self.reference, self.pin_type, self.pin_id)


@dataclass
class Wire:
    start: PinPosition
    end: PinPosition


def q_string(s: str) -> str:
    return '"' + s + '"'


class KiSymbols:
    @staticmethod
    def get_lib_symbols() -> SexpType:

        o: SexpType = [
            "lib_symbols",
            [
                "symbol",
                '"Switch:SW_SPST"',
                ["pin_names", ["offset", "0"], "hide"],
                ["in_bom", "yes"],
                ["on_board", "yes"],
                [
                    "property",
                    '"Reference"',
                    '"SW"',
                    ["at", "0", "3.175", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]]],
                ],
                [
                    "property",
                    '"Value"',
                    '"SW_SPST"',
                    ["at", "0", "-2.54", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]]],
                ],
                [
                    "property",
                    '"Footprint"',
                    '""',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"Datasheet"',
                    '"~"',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"ki_keywords"',
                    '"switch lever"',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"ki_description"',
                    '"Single Pole Single Throw (SPST) switch"',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "symbol",
                    '"SW_SPST_0_0"',
                    [
                        "circle",
                        ["center", "-2.032", "0"],
                        ["radius", "0.508"],
                        ["stroke", ["width", "0"], ["type", "default"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "-1.524", "0.254"], ["xy", "1.524", "1.778"]],
                        ["stroke", ["width", "0"], ["type", "default"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "circle",
                        ["center", "2.032", "0"],
                        ["radius", "0.508"],
                        ["stroke", ["width", "0"], ["type", "default"]],
                        ["fill", ["type", "none"]],
                    ],
                ],
                [
                    "symbol",
                    '"SW_SPST_1_1"',
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "-5.08", "0", "0"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"A"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"1"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "5.08", "0", "180"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"B"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"2"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                ],
            ],
            [
                "symbol",
                '"atari-keyboard-rescue:D_Small_ALT-Device"',
                ["pin_numbers", "hide"],
                ["pin_names", ["offset", "0.254"], "hide"],
                ["in_bom", "yes"],
                ["on_board", "yes"],
                [
                    "property",
                    '"Reference"',
                    '"D"',
                    ["at", "-1.27", "2.032", "0"],
                    [
                        "effects",
                        ["font", ["size", "1.27", "1.27"]],
                        ["justify", "left"],
                    ],
                ],
                [
                    "property",
                    '"Value"',
                    '"D_Small_ALT-Device"',
                    ["at", "-3.81", "-2.032", "0"],
                    [
                        "effects",
                        ["font", ["size", "1.27", "1.27"]],
                        ["justify", "left"],
                    ],
                ],
                [
                    "property",
                    '"Footprint"',
                    '""',
                    ["at", "0", "0", "90"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"Datasheet"',
                    '""',
                    ["at", "0", "0", "90"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"ki_fp_filters"',
                    '"TO-???* *_Diode_* *SingleDiode* D_*"',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "symbol",
                    '"D_Small_ALT-Device_0_1"',
                    [
                        "polyline",
                        ["pts", ["xy", "-0.762", "-1.016"], ["xy", "-0.762", "1.016"]],
                        ["stroke", ["width", "0"], ["type", "default"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "-0.762", "0"], ["xy", "0.762", "0"]],
                        ["stroke", ["width", "0"], ["type", "default"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "0.762", "-1.016"],
                            ["xy", "-0.762", "0"],
                            ["xy", "0.762", "1.016"],
                            ["xy", "0.762", "-1.016"],
                        ],
                        ["stroke", ["width", "0"], ["type", "default"]],
                        ["fill", ["type", "outline"]],
                    ],
                ],
                [
                    "symbol",
                    '"D_Small_ALT-Device_1_1"',
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "-2.54", "0", "0"],
                        ["length", "1.778"],
                        [
                            "name",
                            '"K"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"1"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "2.54", "0", "180"],
                        ["length", "1.778"],
                        [
                            "name",
                            '"A"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"2"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                ],
            ],
            [
                "symbol",
                '"keebio:MX-with-LED"',
                ["pin_names", ["offset", "1.016"]],
                ["in_bom", "yes"],
                ["on_board", "yes"],
                [
                    "property",
                    '"Reference"',
                    '"SW"',
                    ["at", "0", "-8.89", "0"],
                    ["effects", ["font", ["size", "1.524", "1.524"]]],
                ],
                [
                    "property",
                    '"Value"',
                    '"MX-with-LED"',
                    ["at", "0", "8.89", "0"],
                    ["effects", ["font", ["size", "1.524", "1.524"]]],
                ],
                [
                    "property",
                    '"Footprint"',
                    '""',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.524", "1.524"]], "hide"],
                ],
                [
                    "property",
                    '"Datasheet"',
                    '""',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.524", "1.524"]], "hide"],
                ],
                [
                    "symbol",
                    '"MX-with-LED_0_1"',
                    [
                        "polyline",
                        ["pts", ["xy", "-1.27", "-3.81"], ["xy", "-2.54", "-3.81"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "1.27", "-2.54"], ["xy", "1.27", "-5.08"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "2.54", "-3.81"], ["xy", "1.27", "-3.81"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "2.54", "-2.54"], ["xy", "3.81", "-1.27"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "3.81", "-2.54"],
                            ["xy", "3.81", "-1.27"],
                            ["xy", "2.54", "-1.27"],
                        ],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "-2.54", "2.54"],
                            ["xy", "-1.27", "3.81"],
                            ["xy", "1.27", "3.81"],
                            ["xy", "2.54", "2.54"],
                        ],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "-1.27", "-2.54"],
                            ["xy", "-1.27", "-5.08"],
                            ["xy", "1.27", "-3.81"],
                            ["xy", "-1.27", "-2.54"],
                        ],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "-3.81", "1.27"],
                            ["xy", "3.81", "1.27"],
                            ["xy", "3.81", "2.54"],
                            ["xy", "-3.81", "2.54"],
                            ["xy", "-3.81", "1.27"],
                        ],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                ],
                [
                    "symbol",
                    '"MX-with-LED_1_1"',
                    [
                        "pin",
                        "input",
                        "line",
                        ["at", "-5.08", "0", "0"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"~"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"1"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "input",
                        "line",
                        ["at", "5.08", "0", "180"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"~"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"2"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "input",
                        "line",
                        ["at", "-5.08", "-3.81", "0"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"~"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"3"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "input",
                        "line",
                        ["at", "5.08", "-3.81", "180"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"~"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"4"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                ],
            ],
            [
                "symbol",
                '"keebio:MX_LED"',
                ["pin_names", ["offset", "1.016"], "hide"],
                ["in_bom", "yes"],
                ["on_board", "yes"],
                [
                    "property",
                    '"Reference"',
                    '"SW"',
                    ["at", "1.651", "2.413", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]]],
                ],
                [
                    "property",
                    '"Value"',
                    '"MX_LED"',
                    ["at", "0", "-3.81", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]]],
                ],
                [
                    "property",
                    '"Footprint"',
                    '""',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"Datasheet"',
                    '""',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
                ],
                [
                    "property",
                    '"ki_locked"',
                    '""',
                    ["at", "0", "0", "0"],
                    ["effects", ["font", ["size", "1.27", "1.27"]]],
                ],
                [
                    "symbol",
                    '"MX_LED_1_1"',
                    [
                        "circle",
                        ["center", "-2.032", "0"],
                        ["radius", "0.508"],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "-2.54", "1.27"], ["xy", "2.54", "1.27"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "0", "1.27"], ["xy", "0", "3.429"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "circle",
                        ["center", "2.032", "0"],
                        ["radius", "0.508"],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "-5.08", "0", "0"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"1"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"1"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "5.08", "0", "180"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"2"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"2"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                ],
                [
                    "symbol",
                    '"MX_LED_2_1"',
                    [
                        "polyline",
                        ["pts", ["xy", "1.27", "-1.27"], ["xy", "1.27", "1.27"]],
                        ["stroke", ["width", "0.2032"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        ["pts", ["xy", "1.27", "0"], ["xy", "-1.27", "0"]],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "-1.27", "-1.27"],
                            ["xy", "-1.27", "1.27"],
                            ["xy", "1.27", "0"],
                            ["xy", "-1.27", "-1.27"],
                        ],
                        ["stroke", ["width", "0.2032"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "1.778", "-0.762"],
                            ["xy", "3.302", "-2.286"],
                            ["xy", "2.54", "-2.286"],
                            ["xy", "3.302", "-2.286"],
                            ["xy", "3.302", "-1.524"],
                        ],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "polyline",
                        [
                            "pts",
                            ["xy", "3.048", "-0.762"],
                            ["xy", "4.572", "-2.286"],
                            ["xy", "3.81", "-2.286"],
                            ["xy", "4.572", "-2.286"],
                            ["xy", "4.572", "-1.524"],
                        ],
                        ["stroke", ["width", "0"], ["type", "solid"]],
                        ["fill", ["type", "none"]],
                    ],
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "-3.81", "0", "0"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"3"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"3"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                    [
                        "pin",
                        "passive",
                        "line",
                        ["at", "3.81", "0", "180"],
                        ["length", "2.54"],
                        [
                            "name",
                            '"4"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                        [
                            "number",
                            '"4"',
                            ["effects", ["font", ["size", "1.27", "1.27"]]],
                        ],
                    ],
                ],
            ],
        ]

        return o

    @staticmethod
    def get_diode(designator: str, name: str) -> SexpType:
        o: SexpType = [
            "symbol",
            ["lib_id", '"atari-keyboard-rescue:D_Small_ALT-Device"'],
            ["at", "138.43", "69.85", "90"],
            ["unit", "1"],
            ["in_bom", "yes"],
            ["on_board", "yes"],
            ["dnp", "no"],
            # ["uuid", "531a95e8-0a0e-490d-970d-472dfb031305"],
            [
                "property",
                '"Reference"',
                q_string(designator),
                ["at", "140.1572", "68.6816", "90"],
                [
                    "effects",
                    ["font", ["size", "1.27", "1.27"]],
                    ["justify", "right"],
                ],
            ],
            [
                "property",
                '"Value"',
                q_string(name),
                ["at", "140.1572", "70.993", "90"],
                [
                    "effects",
                    ["font", ["size", "1.27", "1.27"]],
                    ["justify", "right"],
                ],
            ],
            [
                "property",
                '"Footprint"',
                '"retro-kbd:Diode-dual"',
                ["at", "138.43", "69.85", "90"],
                ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
            ],
            [
                "property",
                '"Datasheet"',
                '"~"',
                ["at", "138.43", "69.85", "90"],
                ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
            ],
            ["pin", '"1"', ["uuid", "ae415bb0-8625-44d9-a315-c14d3561d720"]],
            ["pin", '"2"', ["uuid", "a06e82c3-6bd9-476a-a04a-e74e3bdf0a71"]],
            [
                "instances",
                [
                    "project",
                    '"atari-keyboard"',
                    [
                        "path",
                        '"/f6a334f3-ee33-4c56-a7bb-b961693d3d0e/7ce608c9-579d-47fb-84c9-158fdf17ec91"',
                        ["reference", q_string(designator)],
                        ["unit", "1"],
                    ],
                ],
            ],
        ]
        return o

    @staticmethod
    def get_mx_with_led(designator: str, name: str, size: Decimal) -> SexpType:
        o: SexpType = [
            "symbol",
            ["lib_id", '"keebio:MX-with-LED"'],
            ["at", "45.72", "50.8", "0"],
            ["unit", "1"],
            ["in_bom", "yes"],
            ["on_board", "yes"],
            ["dnp", "no"],
            ["fields_autoplaced"],
            ["uuid", "58cd7370-da76-4ce4-a1f8-b0bd9031cb55"],
            [
                "property",
                '"Reference"',
                q_string(designator),
                ["at", "45.72", "41.91", "0"],
                ["effects", ["font", ["size", "1.524", "1.524"]]],
            ],
            [
                "property",
                '"Value"',
                q_string(name),
                ["at", "45.72", "44.45", "0"],
                ["effects", ["font", ["size", "1.524", "1.524"]]],
            ],
            [
                "property",
                '"Footprint"',
                f'"mx_alps:MX-{size}U"',
                ["at", "45.72", "50.8", "0"],
                ["effects", ["font", ["size", "1.524", "1.524"]], "hide"],
            ],
            [
                "property",
                '"Datasheet"',
                '""',
                ["at", "45.72", "50.8", "0"],
                ["effects", ["font", ["size", "1.524", "1.524"]], "hide"],
            ],
            ["pin", '"3"', ["uuid", "50c71f6c-3940-4029-bd52-9c330e627525"]],
            ["pin", '"4"', ["uuid", "d4ade8df-0030-4389-80d0-9e49cc63cea7"]],
            ["pin", '"2"', ["uuid", "dddf8399-153f-48c9-a9d8-05927f1e9ba4"]],
            ["pin", '"1"', ["uuid", "c4b4904f-7e9f-401c-9b02-d29567d52975"]],
            [
                "instances",
                [
                    "project",
                    '"atari-keyboard"',
                    [
                        "path",
                        '"/f6a334f3-ee33-4c56-a7bb-b961693d3d0e/7ce608c9-579d-47fb-84c9-158fdf17ec91"',
                        ["reference", q_string(designator)],
                        ["unit", "1"],
                    ],
                ],
            ],
        ]

        return o

    @staticmethod
    def get_mxfull_switch(designator: str, name: str, size: Decimal) -> SexpType:

        o: SexpType = [
            "symbol",
            ["lib_id", '"keebio:MX_LED"'],
            ["at", "68.58", "68.58", "0"],
            ["unit", "1"],
            ["in_bom", "yes"],
            ["on_board", "yes"],
            ["dnp", "no"],
            ["fields_autoplaced"],
            ["uuid", "9097d53d-223b-4938-ba61-19c94644d016"],
            [
                "property",
                '"Reference"',
                q_string(designator),
                ["at", "68.58", "60.96", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]]],
            ],
            [
                "property",
                '"Value"',
                q_string(name),
                ["at", "68.58", "63.5", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]]],
            ],
            [
                "property",
                '"Footprint"',
                f'"mx_alps:MX-{size}U"',
                ["at", "68.58", "68.58", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
            ],
            [
                "property",
                '"Datasheet"',
                '""',
                ["at", "68.58", "68.58", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
            ],
            ["pin", '"3"', ["uuid", "173fe574-dc9a-4914-89d0-c128234183da"]],
            ["pin", '"2"', ["uuid", "57b804e4-630b-4a05-96bd-7c78c5ca6f99"]],
            ["pin", '"4"', ["uuid", "1fe3ac2d-5d22-472c-a74a-87df28e4277d"]],
            ["pin", '"1"', ["uuid", "da8bb528-2f3c-44e1-ae10-65ab95de5d57"]],
            [
                "instances",
                [
                    "project",
                    '"atari-keyboard"',
                    [
                        "path",
                        '"/f6a334f3-ee33-4c56-a7bb-b961693d3d0e/7ce608c9-579d-47fb-84c9-158fdf17ec91"',
                        ["reference", q_string(designator)],
                        ["unit", "1"],
                    ],
                ],
            ],
        ]

        return o

    @staticmethod
    def get_mxfull_led(designator: str, name: str) -> SexpType:
        o: SexpType = [
            "symbol",
            ["lib_id", '"keebio:MX_LED"'],
            ["at", "60.96", "101.6", "0"],
            ["unit", "2"],
            ["in_bom", "yes"],
            ["on_board", "yes"],
            ["dnp", "no"],
            ["fields_autoplaced"],
            ["uuid", "6d57d89b-5b95-4119-8bef-11b8e121ebc9"],
            [
                "property",
                '"Reference"',
                q_string(designator),
                ["at", "62.5602", "95.25", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]]],
            ],
            [
                "property",
                '"Value"',
                q_string(name),
                ["at", "62.5602", "97.79", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]]],
            ],
            [
                "property",
                '"Footprint"',
                '""',
                ["at", "60.96", "101.6", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
            ],
            [
                "property",
                '"Datasheet"',
                '""',
                ["at", "60.96", "101.6", "0"],
                ["effects", ["font", ["size", "1.27", "1.27"]], "hide"],
            ],
            ["pin", '"3"', ["uuid", "173fe574-dc9a-4914-89d0-c128234183da"]],
            ["pin", '"2"', ["uuid", "57b804e4-630b-4a05-96bd-7c78c5ca6f99"]],
            ["pin", '"4"', ["uuid", "1fe3ac2d-5d22-472c-a74a-87df28e4277d"]],
            ["pin", '"1"', ["uuid", "da8bb528-2f3c-44e1-ae10-65ab95de5d57"]],
            [
                "instances",
                [
                    "project",
                    '"atari-keyboard"',
                    [
                        "path",
                        '"/f6a334f3-ee33-4c56-a7bb-b961693d3d0e/7ce608c9-579d-47fb-84c9-158fdf17ec91"',
                        ["reference", q_string(designator)],
                        ["unit", "2"],
                    ],
                ],
            ],
        ]

        return o

    @staticmethod
    def get_junction(x: str | Decimal, y: str | Decimal) -> SexpType:
        o: SexpType = [
            "junction",
            ["at", str(x), str(y)],
            ["diameter", "0"],
            ["color", "0", "0", "0", "0"],
        ]
        return o

    @staticmethod
    def get_wire(wire: Wire) -> SexpType:
        x1 = str(wire.start.x)
        y1 = str(wire.start.y)

        x2 = str(wire.end.x)
        y2 = str(wire.end.y)

        o: SexpType = [
            "wire",
            ["pts", ["xy", x1, y1], ["xy", x2, y2]],
            ["stroke", ["width", "0"], ["type", "default"]],
        ]
        return o

    @staticmethod
    def get_interconnect_global_label(label: str) -> SexpType:
        o: SexpType = [
            "global_label",
            q_string(label),
            ["shape", "input"],
            ["at", "185.42", "101.6", "90"],
            ["fields_autoplaced"],
            ["effects", ["font", ["size", "0.5", "0.5"]], ["justify", "left"]],
            ["uuid", "03f8d392-d47d-4f7e-b278-f382910bcc87"],
            [
                "property",
                '"Intersheetrefs"',
                '"${INTERSHEET_REFS}"',
                ["at", "185.42", "98.063", "90"],
                [
                    "effects",
                    ["font", ["size", "1.27", "1.27"]],
                    ["justify", "left"],
                    "hide",
                ],
            ],
        ]

        return o

    @staticmethod
    def get_global_label(label: str) -> SexpType:
        o: SexpType = [
            "global_label",
            q_string(label),
            ["shape", "input"],
            ["at", "30.48", "15.24", "180"],
            ["fields_autoplaced"],
            ["effects", ["font", ["size", "1.27", "1.27"]], ["justify", "right"]],
            ["uuid", "eb2988e9-2949-4f98-a3f1-6f7b5804363f"],
            [
                "property",
                '"Intersheetrefs"',
                '"${INTERSHEET_REFS}"',
                ["at", "24.1575", "15.24", "0"],
                [
                    "effects",
                    ["font", ["size", "1.27", "1.27"]],
                    ["justify", "right"],
                    "hide",
                ],
            ],
        ]

        return o
