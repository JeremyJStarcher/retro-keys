from dataclasses import dataclass
from typing import List
from dataclass_wizard import fromdict, asdict  # type: ignore


@dataclass
class QmkLayout:
    label: str
    matrix: list[int]
    w: float
    h: float
    x: float
    y: float


class QmkTools:

    qmk: dict
    json_path_to_qmk_layout: str

    def __init__(
        self,
        *,
        qmk: dict,
        json_path_to_qmk_layout: str,
    ) -> None:
        self.qmk = qmk
        self.json_path_to_qmk_layout = json_path_to_qmk_layout

    def format_decimal_value(self, f: float):
        return f"{f:.4f}"

    def get_layout_from_dictionary(self) -> list[QmkLayout]:
        path_elements = self.json_path_to_qmk_layout.split(".")

        top = self.qmk
        if self.json_path_to_qmk_layout != "":
            for bit in path_elements:
                top = top[bit]

        qmk_layout_dict = top
        qmk_layout_list: list[QmkLayout] = []

        for l in qmk_layout_dict:

            # data = {
            #     #   "h": 1.25,
            #     "label": "SELECT",
            #     "matrix": [3, 8],
            #     "w": 1.25,
            #     "x": 16.5,
            #     "y": 4,
            # }

            l.setdefault("h", 1)
            l.setdefault("w", 1)

            layout = fromdict(QmkLayout, l)
            qmk_layout_list.append(layout)
        return qmk_layout_list

    def arrange_layout_in_yx_order(self) -> dict[float, list[QmkLayout]]:
        """
        Return a sorted list by keyboard layout, by each
        different 'y' and then the keys sorted by 'x' within
        that 'y'.
        """

        layout = self.get_layout_from_dictionary()

        y_set = set(map(lambda ll: ll.y, layout))
        y_list = list(y_set)
        y_list.sort()

        # Pre-prime all of the values so we have them in sorted order.
        heightDict: dict[float, list[QmkLayout]] = {}
        for y in y_list:
            heightDict[y] = []

        # Walk through the layout one after the other and drop them
        # in the right bucket.
        for l in layout:
            hs = heightDict.get(l.y, [])
            hs.append(l)
            heightDict[l.y] = hs

        for h, v in heightDict.items():
            v.sort(key=lambda x: x.x)

        return heightDict

    def absolute_to_relative(self, absolute_values: List[float]) -> List[float]:
        relative_values = [absolute_values[0]] + [
            b - a for a, b in zip(absolute_values[:-1], absolute_values[1:])
        ]
        return relative_values
