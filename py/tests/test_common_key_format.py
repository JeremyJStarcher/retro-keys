import json
import unittest
from common_key_format import CommonKeyData
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

    def test_get_key_layoutdata_by_name(self):
        common_key_format = CommonKeyData()

        qmk_tools = self.getQmkTools()
        key_names = qmk_tools.get_keynames_list_from_qmk()

        common_key_format.update_from_qmk(qmk_tools)

        for key_name in key_names:
            qmk_key = qmk_tools.get_key_from_layoutdata_by_name(key_name)
            common = common_key_format.get_from_common_keys_or_new(key_name)

            self.assertEqual(qmk_key.x, common.absolute.x)
            self.assertEqual(qmk_key.y, common.absolute.y)


if __name__ == "__main__":
    unittest.main()
