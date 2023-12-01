from decimal import Decimal
from enum import Enum
from typing import Union, List


class UnitNumber(Enum):
    ONE = "1"
    TWO = "2"


class PinType(Enum):
    NUMBER = "number"


class PinNumber(Enum):
    _1 = "1"
    _2 = "2"
    _3 = "3"
    _4 = "4"


# Forward declaration for a recursive type
SexpTypeValue = Union[str, "SexpType"]
SexpType = List[SexpTypeValue]
SexpListType = List[SexpType]


def makeDecimal(v: SexpTypeValue):
    if isinstance(v, str):
        return Decimal(v)
    else:
        raise TypeError(f"(makeDecimal) Expected a string, but got {type(v).__name__}")


def makeString(v: SexpTypeValue):
    if isinstance(v, str):
        return v
    else:
        raise TypeError(f"(makeString) Expected a string, but got {type(v).__name__}")
