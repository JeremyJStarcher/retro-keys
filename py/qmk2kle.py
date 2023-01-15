from dataclasses import dataclass
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
    pathToLayout: str

    def __init__(
        self,
        *,
        qmk: dict,
        pathToLayout: str,
    ) -> None:
        self.qmk = qmk
        self.pathToLayout = pathToLayout

    def formatValue(self, f: float):
        return f"{f:.4f}"

    def getLayoutFromDictionary(self) -> list[QmkLayout]:
        pathBits = self.pathToLayout.split(".")

        top = self.qmk
        for bit in pathBits:
            top = top[bit]

        qmkLayoutDict = top
        qmkLayoutList: list[QmkLayout] = []

        for l in qmkLayoutDict:

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
            qmkLayoutList.append(layout)
        return qmkLayoutList

    def getLayoutArrangedByKeyboardLayout(self) -> dict[float, list[QmkLayout]]:
        """
        Return a sorted list by keyboard layout, by each
        different 'y' and then the keys sorted by 'x' within
        that 'y'.
        """

        layout = self.getLayoutFromDictionary()

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
