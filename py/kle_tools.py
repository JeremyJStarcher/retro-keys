from typing import List, cast
from attr import dataclass
from bs4 import BeautifulSoup, Tag


@dataclass
class KleData:
    x = 0.0
    y = 0.0
    h = 1.0
    w = 1.0
    is_homing_key = False
    is_decal = False
    labels: List[str] = []
    canonical_name = ""


class KleTools:
    def __init__(self, *, kle: list) -> None:
        self.kle = kle

        """ KLE Key data"""
        self.kle_key_data: List[KleData] = []
        self.__parse_key_data()

    def __parse_key_data(self):
        """
        This is NOT a complete KLE file parser -- it only parses enough to handle
        the very specific use case of the Retro-Keys project.
        """
        key_list = [p for p in self.kle if isinstance(p, list)]
        flattened = [
            item
            for sublist in key_list
            for item in (sublist if isinstance(sublist, list) else [sublist])
        ]

        idx = 0
        while idx < len(flattened):
            key_data_or_label = flattened[idx]

            if isinstance(key_data_or_label, str):
                kle_data = KleData()
                kle_data.labels = [key_data_or_label]

                self.kle_key_data.append(kle_data)
                idx += 1
                continue

            kle_data = KleData()
            kle_data.labels = flattened[idx + 1]

            if key_data_or_label.get("n"):
                kle_data.is_homing_key = True

            if key_data_or_label.get("d"):
                kle_data.is_decal = True

            tmp = key_data_or_label.get("x")
            if tmp:
                kle_data.x = tmp

            tmp = key_data_or_label.get("y")
            if tmp:
                kle_data.y = tmp

            tmp = key_data_or_label.get("h")
            if tmp:
                kle_data.h = tmp

            tmp = key_data_or_label.get("w")
            if tmp:
                kle_data.w = tmp

            soup = BeautifulSoup(kle_data.labels, "html.parser")
            kle_data.canonical_name = cast(Tag, soup.find("i", class_="qmk_id")).text

            self.kle_key_data.append(kle_data)
            idx += 2

    def get_key_data(self) -> List[KleData]:
        return self.kle_key_data

    def get_keynames_list_from_kle(self) -> List[str]:
        canonical_names = [item.canonical_name for item in self.kle_key_data]
        return canonical_names

    def get_key_from_layoutdata_by_name(self, canonical_name: str):
        for k in self.kle_key_data:
            if k.canonical_name == canonical_name:
                return k
        raise ValueError(f"{canonical_name} was not found")

    # def format_decimal_value(self, f: float):
    #     return f"{f:.4f}"

    # def get_keynames_list_from_qmk(self) -> List[str]:
    #     layout = self.get_layout_from_dictionary()
    #     return [key.label for key in layout]

    # def get_layout_from_dictionary(self) -> list[QmkLayout]:
    #     if len(self.__qmk_layout_structure) > 0:
    #         return self.__qmk_layout_structure

    #     path_elements = self.json_path_to_qmk_layout.split(".")

    #     top = self.qmk
    #     if self.json_path_to_qmk_layout != "":
    #         for bit in path_elements:
    #             top = top[bit]

    #     qmk_layout_dict = top
    #     qmk_layout_list: list[QmkLayout] = []

    #     for l in qmk_layout_dict:

    #         # data = {
    #         #     #   "h": 1.25,
    #         #     "label": "SELECT",
    #         #     "matrix": [3, 8],
    #         #     "w": 1.25,
    #         #     "x": 16.5,
    #         #     "y": 4,
    #         # }

    #         l.setdefault("h", 1)
    #         l.setdefault("w", 1)

    #         layout = fromdict(QmkLayout, l)
    #         qmk_layout_list.append(layout)

    #     self.__qmk_layout_structure = qmk_layout_list
    #     return qmk_layout_list

    # def get_key_from_layoutdata_by_name(self, name: str) -> QmkLayout:
    #     layout = next(
    #         (key for key in self.__qmk_layout_structure if key.label == name), None
    #     )
    #     if layout is None:
    #         raise Exception("QmkLayout with the specified name not found.")
    #     return layout

    # def arrange_layout_in_yx_order(self) -> dict[float, list[QmkLayout]]:
    #     """
    #     Return a sorted list by keyboard layout, by each
    #     different 'y' and then the keys sorted by 'x' within
    #     that 'y'.
    #     """

    #     layout = self.get_layout_from_dictionary()

    #     y_set = set(map(lambda ll: ll.y, layout))
    #     y_list = list(y_set)
    #     y_list.sort()

    #     # Pre-prime all of the values so we have them in sorted order.
    #     heightDict: dict[float, list[QmkLayout]] = {}
    #     for y in y_list:
    #         heightDict[y] = []

    #     # Walk through the layout one after the other and drop them
    #     # in the right bucket.
    #     for l in layout:
    #         hs = heightDict.get(l.y, [])
    #         hs.append(l)
    #         heightDict[l.y] = hs

    #     for h, v in heightDict.items():
    #         v.sort(key=lambda x: x.x)

    #     return heightDict

    # def absolute_to_relative(self, absolute_values: List[float]) -> List[float]:
    #     relative_values = [absolute_values[0]] + [
    #         b - a for a, b in zip(absolute_values[:-1], absolute_values[1:])
    #     ]
    #     return relative_values
