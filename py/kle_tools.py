from decimal import Decimal
from typing import List, cast
from attr import dataclass
from bs4 import BeautifulSoup, Tag


@dataclass
class KleData:
    # Comes in from JSON so these must be floats
    x = 0.0
    y = 0.0
    h = 1.0
    w = 1.0
    y_idx: int = 0
    x_idx: int = 0
    is_homing_key = False
    is_decal = False
    labels: str = ""
    canonical_name = ""


class KleTools:
    def __init__(self, *, kle: list) -> None:
        self.kle = kle

        """ KLE Key data"""
        self.kle_key_data: List[KleData] = []
        self.__parse_key_data()

    def __parse_key_data(self):
        def set_label(kle_data: KleData):
            soup = BeautifulSoup(kle_data.labels, "html.parser")
            kle_data.canonical_name = cast(Tag, soup.find("i", class_="qmk_id")).text

        """
        This is NOT a complete KLE file parser -- it only parses enough to handle
        the very specific use case of the Retro-Keys project.
        """

        key_list = [p for p in self.kle if isinstance(p, list)]

        for y_idx, y_row in enumerate(key_list):
            x_array_idx = 0
            x_key_idx = 0
            while x_array_idx < len(y_row):
                key_data_or_label = y_row[x_array_idx]

                if isinstance(key_data_or_label, str):
                    kle_data = KleData()
                    kle_data.labels = key_data_or_label
                    kle_data.y_idx = y_idx
                    kle_data.x_idx = x_key_idx
                    set_label(kle_data)

                    self.kle_key_data.append(kle_data)
                    x_array_idx += 1
                    x_key_idx += 1
                    continue

                kle_data = KleData()
                kle_data.labels = y_row[x_array_idx + 1]
                set_label(kle_data)
                kle_data.y_idx = y_idx
                kle_data.x_idx = x_key_idx

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

                self.kle_key_data.append(kle_data)
                x_array_idx += 2
                x_key_idx += 1

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
