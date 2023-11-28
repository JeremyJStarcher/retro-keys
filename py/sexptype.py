from decimal import Decimal
from typing import Union, List

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
