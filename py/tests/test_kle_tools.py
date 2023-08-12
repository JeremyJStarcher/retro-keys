import json
import unittest
from kle_tools import KleTools

from tests.test_filepaths import SAMPLE_KEYBOARD_LAYOUT_FILENAME


class TestKleTools(unittest.TestCase):
    def read_file(self) -> list:
        with open(SAMPLE_KEYBOARD_LAYOUT_FILENAME, "r") as data_file:
            data = data_file.read()
            return json.loads(data)

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def getKleTools(self) -> KleTools:
        kle = self.read_file()
        kle_tools = KleTools(kle=kle)
        return kle_tools

    def test_sanity(self):
        kle_tools = self.getKleTools()
        kle_key_data = kle_tools.get_key_data()

        self.assertEqual(len(kle_key_data), 80)

    def test_get_keyname_list_from_kle(self):
        kle_tools = self.getKleTools()
        key_names = kle_tools.get_keynames_list_from_kle()

        self.assertEqual(len(key_names), 80)

    def test_get_key_layoutdata_by_name(self):
        kle_tools = self.getKleTools()
        key_names = kle_tools.get_keynames_list_from_kle()

        for key_name in key_names:
            key = kle_tools.get_key_from_layoutdata_by_name(key_name)
            self.assertEqual(key.canonical_name, key_name)


if __name__ == "__main__":
    unittest.main()
