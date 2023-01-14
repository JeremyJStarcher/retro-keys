import unittest
import pytest
from kicad_tools import KicadTool
from kicad_tools import Layer
from kicad_parser import KiCadParser
from tests.test_filepaths import SAMPLE_PCB_FILENAME


def read_file():
    data_file = open(SAMPLE_PCB_FILENAME, "r")
    data = data_file.read()
    data_file.close()
    return data


class TestStringMethods(unittest.TestCase):
    def parseFile(self):
        s = read_file()
        parser = KiCadParser(s)
        return parser.toList()

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_findObjectsByNounByRootDepth0(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findObjectsByNoun(pcb, "kicad_pcb", 0)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0][0], "kicad_pcb")

    def test_findObjectsByNounByLevel1Depth0(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findObjectsByNoun(pcb, "level1-test", 0)
        self.assertEqual(len(l), 0)

    def test_findObjectsByNounByLevel1Depth1(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findObjectsByNoun(pcb, "level1-test", 1)
        self.assertEqual(len(l), 1)

    def test_findObjectByNounByLevel1Depth1(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findObjectByNoun(pcb, "level1-test", 1)
        self.assertEqual(len(l), 1)

    def test_findFootprintByGoodReference(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findFootprintByReference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[0], "footprint")

    def test_findFootprintByBadReference(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findFootprintByReference(pcb, "THIS_DOES_NOT_EXIST")
        self.assertTrue(len(l) == 0)

    def test_findAtGoodReference(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findAtByReference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[1], "-153.1515")
        self.assertEqual(l[2], "82.409")

    def test_findSetObjectLocation(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        pcb_tool.setObjectLocation(pcb, "SW201", -100, -200)
        l = pcb_tool.findAtByReference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[1], -100)
        self.assertEqual(l[2], -200)

    def test_getBoundingBoxOfLayerLines(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        switch = pcb_tool.findFootprintByReference(pcb, "SW201")
        # box = parser.getBoundingBoxOfLayerLines(switch, "\"Dwgs.User\"")
        box = pcb_tool.getBoundingBoxOfLayerLines(switch, Layer.User_Drawings)
        # print(Layer.User_Drawings)

        assert box.x1 == pytest.approx(-165.21, 1)
        assert box.y1 == pytest.approx(77.964, 1)
        assert box.x2 == pytest.approx(-146.166, 1)
        assert box.y2 == pytest.approx(97.014, 1)

    # Test the schematic
    def test_findSymbolByGoodReference(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.findSymbolByReference(schematic, "H257")
        self.assertTrue(l != None)
        self.assertEqual(l[0], "symbol")

    def test_getSymbolPropertyPropertyFound(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.getSymbolProperty(schematic, "H257", "PCB_X", 100)
        self.assertEqual(pcb_x, '"-30"')

    def test_getSymbolPropertyPropertyAsFloatFound(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.getSymbolPropertyAsFloat(schematic, "H257", "PCB_X", 100)
        self.assertEqual(pcb_x, -30)

    def test_getSymbolPropertyPropertyAsFloatNotFound(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.getSymbolPropertyAsFloat(schematic, "H257", "XYZZY", 100)
        self.assertEqual(pcb_x, 100)

    def test_removeNouns(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        parent = pcb_tool.findFootprintByReference(pcb, "SW266")
        startNouns = pcb_tool.findObjectsByNoun(parent, "model", float("inf"))
        self.assertGreater(len(startNouns), 0)

        pcb_tool.removeNouns(parent, "model")
        afterNouns = pcb_tool.findObjectsByNoun(parent, "model", float("inf"))
        self.assertEqual(len(afterNouns), 0)


if __name__ == "__main__":
    unittest.main()
