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
        return parser.to_list()

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_find_objects_by_atomByRootDepth0(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "kicad_pcb", 0)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0][0], "kicad_pcb")

    def test_find_objects_by_atomByLevel1Depth0(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "level1-test", 0)
        self.assertEqual(len(l), 0)

    def test_find_objects_by_atomByLevel1Depth1(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "level1-test", 1)
        self.assertEqual(len(l), 1)

    def test_find_object_by_atomByLevel1Depth1(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_object_by_atom(pcb, "level1-test", 1)
        self.assertEqual(len(l), 1)

    def test_findFootprintByGoodReference(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_footprint_by_reference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[0], "footprint")

    def test_findFootprintByBadReference(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_footprint_by_reference(pcb, "THIS_DOES_NOT_EXIST")
        self.assertTrue(len(l) == 0)

    def test_findAtGoodReference(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_at_by_reference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[1], "-153.1515")
        self.assertEqual(l[2], "82.409")

    def test_findset_object_location(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        pcb_tool.set_object_location(pcb, "SW201", -100, -200)
        l = pcb_tool.find_at_by_reference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[1], -100)
        self.assertEqual(l[2], -200)

    def test_get_bounding_box_of_layer_lines(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        switch = pcb_tool.find_footprint_by_reference(pcb, "SW201")
        # box = parser.get_bounding_box_of_layer_lines(switch, "\"Dwgs.User\"")
        box = pcb_tool.get_bounding_box_of_layer_lines(switch, Layer.User_Drawings)
        # print(Layer.User_Drawings)

        assert box.x1 == pytest.approx(-165.21, 1)
        assert box.y1 == pytest.approx(77.964, 1)
        assert box.x2 == pytest.approx(-146.166, 1)
        assert box.y2 == pytest.approx(97.014, 1)

    # Test the schematic
    def test_findSymbolByGoodReference(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        l = pcb_tool.find_symbol_by_reference(schematic, "H257")
        self.assertTrue(l != None)
        self.assertEqual(l[0], "symbol")

    def test_get_symbol_propertyPropertyFound(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.get_symbol_property(schematic, "H257", "PCB_X", 100)
        self.assertEqual(pcb_x, '"-30"')

    def test_get_symbol_propertyPropertyAsFloatFound(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.get_symbol_property_as_float(schematic, "H257", "PCB_X", 100)
        self.assertEqual(pcb_x, -30)

    def test_get_symbol_propertyPropertyAsFloatNotFound(self):
        schematic = self.parseFile()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.get_symbol_property_as_float(schematic, "H257", "XYZZY", 100)
        self.assertEqual(pcb_x, 100)

    def test_remove_atoms(self):
        pcb = self.parseFile()
        pcb_tool = KicadTool()

        parent = pcb_tool.find_footprint_by_reference(pcb, "SW266")
        startatoms = pcb_tool.find_objects_by_atom(parent, "model", float("inf"))
        self.assertGreater(len(startatoms), 0)

        pcb_tool.remove_atoms(parent, "model")
        afteratoms = pcb_tool.find_objects_by_atom(parent, "model", float("inf"))
        self.assertEqual(len(afteratoms), 0)


if __name__ == "__main__":
    unittest.main()
