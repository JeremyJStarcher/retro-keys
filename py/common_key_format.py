import math
from typing import List
from kle_tools import KleTools
from qmk_tools import QmkTools
from dataclasses import dataclass, field


@dataclass
class CommonKeyFormatQmk:
    x: float = -1
    y: float = -1


class CommonKeyFormatKle:
    x: float = -1
    y: float = -1
    y_idx: int
    x_idx: int


@dataclass
class CommonKeyFormat:
    kle_location = CommonKeyFormatKle()
    qmk_location = CommonKeyFormatQmk()
    w = 1.0
    h = 1.0
    name: str = ""


CommonFormatKeys = dict[str, CommonKeyFormat]


@dataclass
class CommonKeyData:
    common_key_dict: CommonFormatKeys = field(default_factory=dict)

    def get_from_common_keys_or_new(self, canonical_name: str) -> CommonKeyFormat:
        if canonical_name not in self.common_key_dict:
            item = CommonKeyFormat()
            item.qmk_location = CommonKeyFormatQmk()
            item.kle_location = CommonKeyFormatKle()
            item.name = canonical_name
            self.common_key_dict[canonical_name] = item
            return item
        else:
            return self.common_key_dict[canonical_name]

    def update_from_qmk(self, qmk_tools: QmkTools) -> None:
        keyname_list = qmk_tools.get_keynames_list_from_qmk()

        for keyname in keyname_list:
            qmk_key = qmk_tools.get_key_from_layoutdata_by_name(keyname)
            common_format = self.get_from_common_keys_or_new(keyname)

            common_format.qmk_location.x = qmk_key.x
            common_format.qmk_location.y = qmk_key.y

    def update_from_kle(self, kle_tools: KleTools) -> None:
        keyname_list = kle_tools.get_keynames_list_from_kle()

        for keyname in keyname_list:
            kle_key = kle_tools.get_key_from_layoutdata_by_name(keyname)

            common_format = self.get_from_common_keys_or_new(keyname)

            common_format.kle_location.x = kle_key.x
            common_format.kle_location.y = kle_key.y
            common_format.kle_location.y_idx = kle_key.y_idx
            common_format.kle_location.x_idx = kle_key.x_idx

            common_format.w = kle_key.w
            common_format.h = kle_key.h

    def convert_kle_location_to_qmk(self):
        """
        Converts the key location format from KLE to QMK.

        It is important to note that in the for the 'X' position, the
        width of the previous key must be taken into account.

        However, in the 'Y' position, the height of the previous row is ignored.

        Lets not talk about how long that took to figure out.

        The method updates the QMK locations based on the KLE locations within
        the common_key_dict. It sorts the keys by their y and x indexes and
        converts the relative positions to absolute coordinates.
        """

        y_indexes = sorted(
            {i2.kle_location.y_idx for _, i2 in self.common_key_dict.items()}
        )

        # The absolute Y position
        abs_y = 0.0
        for y_idx in y_indexes:
            x_vals = [
                i2
                for i1, i2 in self.common_key_dict.items()
                if i2.kle_location.y_idx == y_idx
            ]
            x_keys_sorted = sorted(x_vals, key=lambda item: item.kle_location.x_idx)

            # Get any Y_OFFSET for this row. They will all be the same.
            # (And should be part of the first field key but oh well)
            y_offset = [x.kle_location.y for x in x_vals][0]

            # Update by any offset for that 'Y' row.
            # Reverse the y direction.
            abs_y += y_offset

            # The absolute 'X' position
            abs_x = 0
            for x_key in x_keys_sorted:

                # Update by the 'X' offset on the key record itself
                abs_x += x_key.kle_location.x

                x_key.qmk_location.x = abs_x
                x_key.qmk_location.y = abs_y

                # Then update by the width
                abs_x += x_key.w

            abs_y += 1
            # Get the max height for any key in the row
            # y_h = [x.h for x in x_vals ][0]
