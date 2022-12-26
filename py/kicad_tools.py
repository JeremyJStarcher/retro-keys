from enum import Enum
import copy
import math

INF = float("inf")


class Layer(str, Enum):
    F_CU = '"F.Cu"'
    B_CU = '"B.Cu"'
    B_Adhesive = '"B.Adhes"'
    F_Adhesive = '"F.Adhes"'
    B_Paste = '"B.Paste"'
    F_Paste = '"F.Paste"'
    B_Silkscreen = '"B.SilkS"'
    F_Silkscreen = '"F.SilkS"'
    B_Mask = '"B.Mask"'
    F_Mask = '"F.Mask"'
    User_Drawings = '"Dwgs.User"'
    User_Comments = '"Cmts.User"'
    User_Eco1 = '"Eco1.User"'
    User_Eco2 = '"Eco2.User"'
    Edge_Cuts = '"Edge.Cuts"'
    Margin = '"Margin"'
    B_Courtyard = '"B.CrtYd"'
    F_Courtyard = '"F.CrtYd"'
    B_Fab = '"B.Fab"'
    F_Fab = '"F.Fab"'


class BoundingBox:
    def __init__(self, x1: float = -1, y1: float = -1, x2: float = -1, y2: float = -1):

        if x1 == -1:
            self.x1 = float("inf")
            self.y1 = float("inf")
            self.x2 = float("-inf")
            self.y2 = float("-inf")
        else:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

    def update_xy(self, sx: str | float, sy: str | float) -> None:
        x = float(sx)
        y = float(sy)

        self.x1 = min(self.x1, x)
        self.y1 = min(self.y1, y)
        self.x2 = max(self.x2, x)
        self.y2 = max(self.y2, y)

    def addBorder(self, n: float) -> None:
        self.x1 -= n
        self.y1 -= n
        self.x2 += n
        self.y2 += n

    def __repr__(self):
        l = []

        l.append("x1: " + str(self.x1))
        l.append("y1: " + str(self.y1))
        l.append("x2: " + str(self.x2))
        l.append("y2: " + str(self.y2))

        return "{ " + ", ".join(l) + " }"


def qString(s: str) -> str:
    return '"' + s + '"'


class KicadTool:

    # def __init__():
    #     pass

    def findObjectsByNoun(self, root: list, noun: str, maxDepth=float("inf")):
        def _findObjectsByNounInner(array, noun, maxDepth, depth, out):
            for e in array:
                if isinstance(e, list):
                    if (len(e) > 0) and (e[0] == noun):
                        out.append(e)

                    if depth < maxDepth:
                        _findObjectsByNounInner(e, noun, maxDepth, depth + 1, out)
                else:
                    pass
            return out

        return _findObjectsByNounInner([root], noun, maxDepth, 0, [])

    def findObjectByNoun(self, root: list, noun: str, maxDepth=float("inf")):
        objs = self.findObjectsByNoun(root, noun, maxDepth)
        if len(objs) > 1:
            raise Exception(f"Found too many {noun}")
        if len(objs) == 0:
            raise Exception(f"Found zero {noun}" + noun)
        return objs[0]

    def findFootprintByReference(self, root: list, ref: str) -> list:
        prints = self.findObjectsByNoun(root, "footprint", 1)

        for p in prints:
            # print(p)

            o = self.findObjectsByNoun(p, "fp_text", INF)
            filtered = filter(
                lambda fp: (fp[1] == "reference") and (fp[2] == qString(ref)), o
            )

            lst = list(filtered)
            if len(lst) > 0:
                return p

        return []

    def _getTextObjByType(self, root: list, ref: str, type: str) -> list:
        p = self.findFootprintByReference(root, ref)

        assert p is not None

        o = self.findObjectsByNoun(p, "fp_text", INF)
        filtered = filter(lambda fp: (fp[1] == type), o)
        obj = list(filtered)[0]
        return obj

    def setHiddenFootprintTextByReference(
        self, root: list, ref: str, type: str, hidden: bool
    ):
        obj = self._getTextObjByType(root, ref, type)

        # If it is already there, remove it.
        if "hide" in obj:
            obj.remove("hide")

        if hidden:
            obj.append("hide")

    def moveTextToLayer(self, root: list, ref: str, type: str, layer: Layer):
        obj = self._getTextObjByType(root, ref, type)

        o = self.findObjectsByNoun(obj, "layer", INF)

        lst = list(o)
        lst[0][1] = layer

    def copyToBackSilkscreen(self, root: list, ref: str, type: str):
        p = self.findFootprintByReference(root, ref)
        assert p is not None

        obj = self._getTextObjByType(root, ref, type)
        nn = copy.deepcopy(obj)

        layerObject = self.findObjectsByNoun(nn, "layer", INF)

        lst = list(layerObject)
        lst[0][1] = Layer.B_Silkscreen
        nn[1] = "user"

        effectsObject = self.findObjectsByNoun(nn, "effects", INF)

        effectsList = list(effectsObject)
        effectsList[0].append(["justify", "mirror"])

        p.append(nn)

    def findSymbolByReference(self, root: list, ref: str):
        prints = self.findObjectsByNoun(root, "symbol", 1)

        for p in prints:
            o = self.findObjectsByNoun(p, "property", INF)

            filtered = filter(
                lambda fp: (fp[1] == qString("Reference")) and (fp[2] == qString(ref)),
                o,
            )

            lst = list(filtered)
            if len(lst) > 0:
                return p

    def getSymbolProperty(self, root: list, ref: str, prop: str, default: str):
        symbol = self.findSymbolByReference(root, ref)

        o = self.findObjectsByNoun(symbol, "property", INF)

        filtered = filter(lambda fp: (fp[1] == qString(prop)), o)
        lst = list(filtered)
        if len(lst) > 0:
            return lst[0][2]
        else:
            return default

    def getSymbolPropertyAsFloat(self, root: list, ref: str, prop: str, default):
        r = self.getSymbolProperty(root, ref, prop, default)
        r = str(r)
        return float(r.strip('"'))

    def findAtByReference(self, root: list, ref: str) -> list:
        footprint = self.findFootprintByReference(root, ref)
        assert footprint is not None

        o = self.findObjectByNoun(footprint, "at", 1)

        # There are optional parameters.
        # Its harmless to fill them in and makes other code
        # a lot simplier.
        while len(o) != 4:
            o.append("0")

        return o

    def setObjectLocation(
        self, root: list, ref: str, x: float, y: float, rot: float = 0
    ):
        footprint = self.findFootprintByReference(root, ref)

        cat = self.findAtByReference(root, ref)

        current_rot = float(cat[3])
        # If the object is already rotated, then un-rotate it
        if current_rot != 0:
            cat[3] = float(cat[3]) - current_rot
            self.setObjectLocation(root, ref, x, y, -current_rot)

        all_ats = self.findObjectsByNoun(footprint, "at", INF)
        for at1 in all_ats:
            at1.append(0)  # If there isn't a rotation, add it.

            at1_x = at1[1]
            at1_y = at1[2]
            at1_rot = at1[3]

            while len(at1) > 0:
                at1.pop()

            at1.append("at")
            at1.append(at1_x)
            at1.append(at1_y)
            at1.append(int(at1_rot) + rot)

        # Set the primary location and rotation
        at = self.findAtByReference(root, ref)
        if at != None:
            at.append(0)
            old_rot = at[3]
            while len(at) > 0:
                at.pop()

            at.append("at")
            at.append(x)
            at.append(y)
            at.append(rot)

    def addBoundingBox(self, root: list, box: BoundingBox, width: float, layer: Layer):
        _box = [
            "gr_rect",
            ["start", box.x1, box.y1],
            ["end", box.x2, box.y2],
            ["layer", layer],
            ["width", width],
            ["fill", "none"],
        ]

        root.append(_box)

    def getBoundingBoxOfLayerLines(self, root: list, layerName: Layer):
        lines = []

        g_lines = self.findObjectsByNoun(root, "fp_line", float("inf"))
        at = self.findObjectsByNoun(root, "at", 1)

        origin_x = float(at[0][1])
        origin_y = float(at[0][2])

        for g_line in g_lines:
            layers = self.findObjectsByNoun(g_line, "layer", float("inf"))
            for layer in layers:
                if layer[1] == layerName:
                    lines.append(g_line)

        box = BoundingBox(-1, -1, -1, -1)
        for line in lines:
            start = self.findObjectByNoun(line, "start", float("inf"))
            end = self.findObjectByNoun(line, "end", float("inf"))

            x1 = float(start[1])
            y1 = float(start[2])
            x2 = float(end[1])
            y2 = float(end[2])

            box.update_xy(x1 + origin_x, y1 + origin_y)
            box.update_xy(x2 + origin_x, y2 + origin_y)

        return box

    def drawCircle(self, root: list, layer: Layer, x: float, y: float, r: float):
        o = [
            "gr_circle",
            ["center", x, y],
            ["end", x, y - r],
            ["layer", layer],
            ["width", "0.2"],
            ["fill", "none"],
        ]

        root.append(o)

    def drawKeepoutZone(self, root: list, nx: float, ny: float, r: float):
        def pointsInCircum(r, n=100):
            pi = math.pi

            return [
                (math.cos(2 * pi / n * x) * r, math.sin(2 * pi / n * x) * r)
                for x in range(0, n + 1)
            ]

        o = [
            "zone",
            ["net", "0"],
            ["net_name", '""'],
            ["layers", "F&B.Cu"],
            ["tstamp", "4b23aa4c-b704-4f99-b8ee-66b834c9f1a2"],
            ["name", '"FOOBAR"'],
            ["hatch", "full", "0.508"],
            ["connect_pads", ["clearance", "0"]],
            ["min_thickness", "0.254"],
            [
                "keepout",
                ["tracks", "not_allowed"],
                ["vias", "not_allowed"],
                ["pads", "not_allowed"],
                ["copperpour", "allowed"],
                ["footprints", "allowed"],
            ],
            ["fill", ["thermal_gap", "0.508"], ["thermal_bridge_width", "0.508"]],
            [
                "polygon",
                [
                    "pts",
                    # ["xy", "367.386", "203.216"],
                ],
            ],
        ]

        slot = self.findObjectsByNoun(o, "pts", INF)

        pts = pointsInCircum(r, 30)
        for point in pts:
            rr = ["xy", point[0] + nx, point[1] + ny]
            slot[0].append(rr)

        root.append(o)

    def removeNouns(self, parent, noun):
        while True:
            nouns = self.findObjectsByNoun(parent, noun, INF)
            if len(nouns) == 0:
                break

            parent.remove(nouns[0])

    def addSD123Model(self, parent: list, path: str):
        o = [
            "model",
            '"${KIPRJMOD}/' + path + 'SOD-diodes/SOD-123.step"',
            ["offset", ["xyz", "0", "0", "0"]],
            ["scale", ["xyz", "1", "1", "1"]],
            ["rotate", ["xyz", "0", "0", "0"]],
        ]
        parent.append(o)

    def addSwitchModel(self, parent: list, path: str):
        o = [
            "model",
            '"${KIPRJMOD}/' + path + 'cherry-mx-switches/asm_mx_asm_PCB.stp"',
            ["offset", ["xyz", "-2.1", "-4.5", "4"]],
            ["scale", ["xyz", "1", "1", "1"]],
            ["rotate", ["xyz", "-180", "0", "90"]],
        ]
        parent.append(o)

    def addKeycapModel(self, parent: list, url: str):
        o = [
            "model",
            f'"{url}"',
            ["offset", ["xyz", "-2.2", "-4.9", "10"]],
            ["scale", ["xyz", "0.4", "0.4", "0.4"]],
            ["rotate", ["xyz", "0", "0", "0"]],
        ]
        parent.append(o)
