def q_string(s: str) -> str:
    return '"' + s + '"'


class KiSymbols:
    @staticmethod
    def get_diode(designator: str, name: str):
        o = [
            "symbol",
            ["lib_id", '"atari-keyboard-rescue:D_Small_ALT-Device"'],
            ["at", "138.43", "69.85", "90"],
            ["unit", "1"],
            ["in_bom", "yes"],
            ["on_board", "yes"],
            ["dnp", "no"],
            ["uuid", "531a95e8-0a0e-490d-970d-472dfb031305"],
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
    def get_mx_with_led(designator: str, name: str):
        o = [
            "symbol",
            ["lib_id", '"keebio:MX-with-LED"'],
            ["at", "45.72", "50.8", "0"],
            ["unit", "1"],
            ["in_bom", "yes"],
            ["on_board", "yes"],
            ["dnp", "no"],
            ["fields_autoplaced"],
            ["uuid", "58cd7370-da76-4ce4-a1f8-b0bd9031ca55"],
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
                '""',
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
