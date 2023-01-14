from dataclasses import dataclass
from dataclass_wizard import fromdict, asdict


@dataclass
class QmkLayout:
    label: str
    matrix: list[int, int]
    w: float
    h: float
    x: float
    y: float
