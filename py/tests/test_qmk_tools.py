import json
import unittest
from qmk_tools import QmkTools  # type: ignore

from tests.test_filepaths import SAMPLE_QMKINFO_FILENAME


class TestStringMethods(unittest.TestCase):
    def read_file(self) -> dict:
        with open(SAMPLE_QMKINFO_FILENAME, "r") as data_file:
            data = data_file.read()
            return json.loads(data)

    def getQmkTools(self) -> QmkTools:
        qmk = self.read_file()
        qmk_tools = QmkTools(qmk=qmk, json_path_to_qmk_layout="layouts.LAYOUT.layout")
        return qmk_tools

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_sanity(self):
        qmk_tools = self.getQmkTools()
        qmk_layout_list = qmk_tools.get_layout_from_dictionary()
        self.assertGreater(len(qmk_layout_list), 0)

    def test_get_keyname_list_from_qmk(self):
        qmk_tools = self.getQmkTools()
        key_names = qmk_tools.get_keynames_list_from_qmk()

        self.assertEqual(len(key_names), 80)

    def test_get_key_layoutdata_by_name(self):
        qmk_tools = self.getQmkTools()
        key_names = qmk_tools.get_keynames_list_from_qmk()

        for key_name in key_names:
            key = qmk_tools.get_key_from_layoutdata_by_name(key_name)
            self.assertEqual(key.label, key_name)

    def test_arrange_layout_in_yx_order(self):
        qmk_tools = self.getQmkTools()
        qmk_layout_list = qmk_tools.arrange_layout_in_yx_order()

        y_list = list(map(lambda y: y[0], qmk_layout_list.items()))

        is_y_sorted = y_list == sorted(y_list)
        self.assertTrue(is_y_sorted)

        for _y, keys in qmk_layout_list.items():
            x_list = list(map(lambda k: k.x, keys))
            is_x_sorted = x_list == sorted(x_list)
            self.assertTrue(is_x_sorted)


if __name__ == "__main__":
    unittest.main()
