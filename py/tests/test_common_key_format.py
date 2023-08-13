import json
import unittest
from common_key_format import CommonKeyData
from kle_tools import KleTools
from qmk_tools import QmkTools

from tests.test_filepaths import (
    SAMPLE_KEYBOARD_LAYOUT_FILENAME,
    SAMPLE_QMKINFO_FILENAME,
)


class TestCommonKeyFormat(unittest.TestCase):
    def read_qmk_file(self) -> dict:
        with open(SAMPLE_QMKINFO_FILENAME, "r") as data_file:
            data = data_file.read()
            return json.loads(data)

    def read_kle_file(self) -> list:
        with open(SAMPLE_KEYBOARD_LAYOUT_FILENAME, "r") as data_file:
            data = data_file.read()
            return json.loads(data)

    def getQmkTools(self) -> QmkTools:
        qmk = self.read_qmk_file()
        qmk_tools = QmkTools(qmk=qmk, json_path_to_qmk_layout="layouts.LAYOUT.layout")
        return qmk_tools

    def getKleTools(self) -> KleTools:
        kle = self.read_kle_file()
        kle_tools = KleTools(kle=kle)
        return kle_tools

    def test_get_key_layoutdata_by_name_for_qmk(self):
        common_key_format = CommonKeyData()

        qmk_tools = self.getQmkTools()
        key_names = qmk_tools.get_keynames_list_from_qmk()
        self.assertGreater(len(key_names), 0)

        common_key_format.update_from_qmk(qmk_tools)

        for key_name in key_names:
            qmk_key = qmk_tools.get_key_from_layoutdata_by_name(key_name)
            common = common_key_format.get_from_common_keys_or_new(key_name)

            self.assertEqual(qmk_key.x, common.qmk_location.x)
            self.assertEqual(qmk_key.y, common.qmk_location.y)

    def test_get_key_layoutdata_by_name_for_kle(self):
        common_key_format = CommonKeyData()

        kle_tools = self.getKleTools()
        key_names = kle_tools.get_keynames_list_from_kle()

        self.assertGreater(len(key_names), 0)

        common_key_format.update_from_kle(kle_tools)

        for key_name in key_names:
            kle_Key = kle_tools.get_key_from_layoutdata_by_name(key_name)
            common = common_key_format.get_from_common_keys_or_new(key_name)

            self.assertEqual(kle_Key.x, common.kle_location.x)
            self.assertEqual(kle_Key.y, common.kle_location.y)

    def test_loading_kle_and_qmk_does_not_double(self):
        common_key_format = CommonKeyData()

        kle_tools = self.getKleTools()
        kle_key_names = kle_tools.get_keynames_list_from_kle()

        qmk_tools = self.getQmkTools()
        qmk_key_names = qmk_tools.get_keynames_list_from_qmk()

        sorted1 = sorted(kle_key_names)
        sorted2 = sorted(qmk_key_names)

        self.assertEqual(sorted1, sorted2)

        common_key_format.update_from_qmk(qmk_tools)
        common_key_format.update_from_kle(kle_tools)

        self.assertEqual(len(common_key_format.common_key_dict), len(sorted1))

    def test_convert_relative_to_absolute(self):
        common_key_format_kle = CommonKeyData()
        common_key_format_qmk = CommonKeyData()

        kle_tools = self.getKleTools()
        qmk_tools = self.getQmkTools()

        common_key_format_kle.update_from_kle(kle_tools)
        common_key_format_qmk.update_from_qmk(qmk_tools)

        common_key_format_kle.convert_kle_location_to_qmk()

        # Now, compare the values.
        key_names = qmk_tools.get_keynames_list_from_qmk()

        for key_name in key_names:
            kle_key = common_key_format_kle.get_from_common_keys_or_new(key_name)
            qmk_key = common_key_format_qmk.get_from_common_keys_or_new(key_name)

            self.assertAlmostEqual(kle_key.qmk_location.x, qmk_key.qmk_location.x)
            self.assertAlmostEqual(kle_key.qmk_location.y, qmk_key.qmk_location.y)

    def test_get_key_names(self):
        common_key_format_kle = CommonKeyData()

        kle_tools = self.getKleTools()

        common_key_format_kle.update_from_kle(kle_tools)

        key_names_kle = sorted(kle_tools.get_keynames_list_from_kle())
        key_names_common = sorted(common_key_format_kle.get_key_names())

        self.assertEqual(key_names_kle, key_names_common)


if __name__ == "__main__":
    unittest.main()
