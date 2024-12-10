from dataclasses import dataclass
from enum import Enum


class COLOR_SCHEME(Enum):
    NORMAL = 1
    REVERSED = 2


class LEGEND_STATUS(Enum):
    LEGEND_TRUE = True
    LEGEND_FALSE = False


class StlMode(Enum):
    KEY_CAP = 1
    LEGEND = 2
    TWO_COLOR = 3


class SlicerTarget(Enum):
    CURA = 1
    BAMBU = 2


class KeyType(Enum):
    STD = 1
    SPECIAL = 2
    X2 = 3
    CURSOR = 4
    LAYOUT = 5


@dataclass
class KeyInfo:
    key_name: str
    key_type: KeyType
    legend_status: LEGEND_STATUS
    color_scheme: COLOR_SCHEME
