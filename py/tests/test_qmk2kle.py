import json
import unittest
from kicad_parser import KiCadParser
from dataclasses import dataclass
from qmk2kle import QmkLayout, QmkTools
from dataclass_wizard import fromdict, asdict  # type: ignore

from tests.test_filepaths import SAMPLE_QMKINFO_FILENAME


class TestStringMethods(unittest.TestCase):
    def read_file(self) -> dict:
        with open(SAMPLE_QMKINFO_FILENAME, "r") as data_file:
            data = data_file.read()
            return json.loads(data)

    def getQmkTools(self) -> QmkTools:
        qmk = self.read_file()
        qmkTools = QmkTools(qmk=qmk, pathToLayout="layouts.LAYOUT.layout")
        return qmkTools

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_sanity(self):
        qmkTools = self.getQmkTools()
        qmkLayoutList = qmkTools.getLayoutFromDictionary()
        self.assertGreater(len(qmkLayoutList), 0)

    def test_getLayoutArrangedByKeyboardLayout(self):
        qmkTools = self.getQmkTools()
        qmkLayoutList = qmkTools.getLayoutArrangedByKeyboardLayout()

        y_list = list(map(lambda y: y[0], qmkLayoutList.items()))

        isYSorted = y_list == sorted(y_list)
        self.assertTrue(isYSorted)

        for _y, keys in qmkLayoutList.items():
            x_list = list(map(lambda k: k.x, keys))
            isXSorted = x_list == sorted(x_list)
            self.assertTrue(isXSorted)


if __name__ == "__main__":
    unittest.main()
