import unittest
from kicad_parser import KiCadParser
from dataclasses import dataclass
from dataclass_wizard import fromdict, asdict

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


if __name__ == "__main__":
    unittest.main()
