from decimal import Decimal
import math
import unittest
from kicad_tools import KicadTool, QueryRecursionLevel
from kicad_tools import Layer
from kicad_parser import KiCadParser
from sexptype import SexpType, SexpTypeValue, makeDecimal
from tests.test_filepaths import SAMPLE_KEYBOARD_SCH_FILENAME, SAMPLE_PCB_FILENAME


class TestKiCadTools(unittest.TestCase):
    def assert_float_str(self, f: float) -> None:
        try:
            float_value = float(f)  # Try to convert to float
        except ValueError:
            self.fail(f"{f} is not a valid floating-point number")

    def read_pcb_file(self) -> SexpType:
        with open(SAMPLE_PCB_FILENAME, "r") as data_file:
            data = data_file.read()
            parser = KiCadParser(data)
            return parser.to_list()

    def read_keyboard_sch_file(self) -> SexpType:
        with open(SAMPLE_KEYBOARD_SCH_FILENAME, "r") as data_file:
            data = data_file.read()
            parser = KiCadParser(data)
            return parser.to_list()

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_find_object_by_fooDepth0(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_foo(pcb, ["kicad_pcb"], QueryRecursionLevel.HERE)
        self.assertEqual(len(l), 1)
        self.assertIsInstance(l, list)

    def test_find_object_by_fooFootprintByGoodReference(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        ref = "SW201"

        l = pcb_tool.find_objects_by_foo(
            pcb,
            ["footprint", ["fp_text", "reference", '"' + ref + '"']],
            QueryRecursionLevel.HERE,
        )
        self.assertTrue(l != None)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0][0], "footprint")
        self.assertTrue(ref in str(l))

    def test_find_object_by_fooFootprintByGoodReferenceWithAt(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        ref = "SW201"

        l = pcb_tool.find_objects_by_foo(
            pcb,
            ["footprint", ["fp_text", "reference", '"' + ref + '"', ["at"]]],
            QueryRecursionLevel.HERE,
        )
        self.assertTrue(l != None)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0][0], "footprint")
        self.assertTrue(ref in str(l))

    def test_find_object_by_fooFootprintByGoodReferenceWithAtPosition(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        ref = "SW201"

        l = pcb_tool.find_objects_by_foo(
            pcb,
            ["footprint", ["fp_text", "reference", '"' + ref + '"', ["at", "-2.54"]]],
            QueryRecursionLevel.HERE,
        )
        self.assertTrue(l != None)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0][0], "footprint")
        self.assertTrue(ref in str(l))

    def test_find_object_by_fooFootprintByBadDeepReference(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        ref = "SW201"

        l = pcb_tool.find_objects_by_foo(
            pcb,
            ["footprint", ["fp_text", "reference", '"' + ref + '"', ["at", "INVALID"]]],
            QueryRecursionLevel.HERE,
        )
        self.assertTrue(l != None)
        self.assertEqual(len(l), 0)

    def test_find_objects_by_fooDepth1(self) -> None:
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        query: SexpTypeValue = ["version", "20211014"]

        l = pcb_tool.find_objects_by_foo(pcb, query, QueryRecursionLevel.DEEP)
        self.assertIsInstance(l, list)
        self.assertEqual(len(l), 1)
        self.assertIsInstance(l[0], list)
        self.assertEqual(len(l[0]), 2)

        self.assertEqual(l[0][0], query[0])
        self.assertEqual(l[0][1], query[1])

    def test_find_object_by_fooByLevel1Depth0(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "level1-test", QueryRecursionLevel.HERE)
        self.assertEqual(len(l), 0)

    def test_find_objects_by_atomByRootDepth0(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "kicad_pcb", QueryRecursionLevel.HERE)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0][0], "kicad_pcb")

    def test_find_objects_by_atomByLevel1Depth0(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "level1-test", QueryRecursionLevel.HERE)
        self.assertEqual(len(l), 0)

    def test_find_objects_by_atomByLevel1Depth1(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_objects_by_atom(pcb, "kicad_pcb", QueryRecursionLevel.HERE)
        self.assertEqual(len(l), 1)

    def test_find_object_by_atomByLevel1Depth1(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_object_by_atom(pcb, "kicad_pcb", QueryRecursionLevel.HERE)
        self.assertGreater(len(l), 1)

    def test_findFootprintByGoodReference(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_footprint_by_reference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(l[0], "footprint")

    def test_findFootprintByBadReference(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_footprint_by_reference(pcb, "THIS_DOES_NOT_EXIST")
        self.assertTrue(len(l) == 0)

    def test_findAtGoodReference(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_footprint_at_by_reference(pcb, "SW201")
        self.assertTrue(l != None)

        self.assertIsInstance(l[1], str)
        self.assertIsInstance(l[2], str)

    def test_findset_object_location(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        pcb_tool.set_object_location(pcb, "SW201", Decimal(-100), Decimal(-200))
        l = pcb_tool.find_footprint_at_by_reference(pcb, "SW201")
        self.assertTrue(l != None)
        self.assertEqual(makeDecimal(l[1]), Decimal(-100))
        self.assertEqual(makeDecimal(l[2]), Decimal(-200))

    def test_get_bounding_box_of_layer_lines(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        switch = pcb_tool.find_footprint_by_reference(pcb, "SW201")
        box = pcb_tool.get_bounding_box_of_layer_lines(switch, Layer.User_Drawings)

        self.assertLess(box.x1, box.x2)
        self.assertLess(box.y1, box.y2)

    # Test the schematic
    def test_findSymbolByGoodReference(self):
        schematic = self.read_keyboard_sch_file()
        pcb_tool = KicadTool()

        l = pcb_tool.find_symbol_by_reference(schematic, "D202")
        self.assertTrue(l != None)
        if l != None:
            self.assertEqual(l[0], "symbol")

    def test_get_symbol_propertyPropertyFound(self):
        schematic = self.read_keyboard_sch_file()
        pcb_tool = KicadTool()

        dummy = "FOOBAR"

        pcb_x = pcb_tool.get_symbol_property(schematic, "SW232", "PCB_X", dummy)
        self.assertNotEqual(pcb_x, dummy)

    def test_get_symbol_propertyPropertyAsFloatFound(self):
        schematic = self.read_keyboard_sch_file()
        pcb_tool = KicadTool()

        dummy_val = 99999.99

        pcb_x = pcb_tool.get_symbol_property_as_decimal(
            schematic, "SW232", "PCB_X", dummy_val
        )
        self.assertNotEqual(pcb_x, dummy_val)

    def test_get_symbol_propertyPropertyAsFloatNotFound(self):
        schematic = self.read_pcb_file()
        pcb_tool = KicadTool()

        pcb_x = pcb_tool.get_symbol_property_as_decimal(
            schematic, "SW232", "XYZZY", 100
        )
        self.assertEqual(pcb_x, 100)

    def test_remove_atoms(self):
        pcb = self.read_pcb_file()
        pcb_tool = KicadTool()

        parent = pcb_tool.find_footprint_by_reference(pcb, "SW266")
        startatoms = pcb_tool.find_objects_by_atom(
            parent, "model", QueryRecursionLevel.DEEP
        )
        self.assertGreater(len(startatoms), 0)

        pcb_tool.remove_atoms(parent, "model")
        afteratoms = pcb_tool.find_objects_by_atom(
            parent, "model", QueryRecursionLevel.DEEP
        )
        self.assertEqual(len(afteratoms), 0)

    def test_get_get_all_symbol_value_references(self):
        schematic = self.read_keyboard_sch_file()
        sch_tool = KicadTool()
        res = sch_tool.get_all_symbol_value_references(schematic)

        self.assertGreater(len(res), 1)

        for _, l2 in res.items():
            self.assertEqual(len(l2), 2)

    def test_move_recursive(self):
        schematic = self.read_keyboard_sch_file()
        sch_tool = KicadTool()

        parent = sch_tool.find_symbol_by_reference(schematic, "D266")
        if parent != None:
            offset_x = Decimal(-1000)
            offset_y = Decimal(-1000)
            fudge = Decimal(100)
            sch_tool.move_recursive(parent, offset_x, offset_y, 0)

            all_at = sch_tool.find_objects_by_atom(
                parent, "at", QueryRecursionLevel.DEEP
            )

            for at in all_at:
                x1 = makeDecimal(at[1])
                y1 = makeDecimal(at[2])

                self.assertLess(Decimal(abs(offset_x - x1)), fudge)
                self.assertLess(Decimal(abs(offset_y - y1)), fudge)


if __name__ == "__main__":
    unittest.main()
