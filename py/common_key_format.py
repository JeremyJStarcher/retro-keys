from attr import dataclass

from qmk_tools import QmkTools


@dataclass
class CommonKeyFormatLocation:
    x: float = -1
    y: float = -1


@dataclass
class CommonKeyFormat:
    relative = CommonKeyFormatLocation()
    absolute = CommonKeyFormatLocation()
    w = 1.0
    h = 1.0
    name: str = ""


CommonFormatKeys = dict[str, CommonKeyFormat]


@dataclass
class CommonKeyData:
    common_key_dict: CommonFormatKeys = dict()

    def get_from_common_keys_or_new(self, canonical_name: str) -> CommonKeyFormat:
        if canonical_name not in self.common_key_dict:
            item = CommonKeyFormat()
            item.absolute = CommonKeyFormatLocation()
            item.relative = CommonKeyFormatLocation()

            self.common_key_dict[canonical_name] = item
            return item
        else:
            return self.common_key_dict[canonical_name]

    def update_from_qmk(self, qmk_tools: QmkTools) -> None:
        keyname_list = qmk_tools.get_keynames_list_from_qmk()

        for keyname in keyname_list:
            qmk_key = qmk_tools.get_key_from_layoutdata_by_name(keyname)

            ll = qmk_tools.get_layout_from_dictionary()

            common_format = self.get_from_common_keys_or_new(keyname)

            common_format.name = keyname
            common_format.absolute.x = qmk_key.x
            common_format.absolute.y = qmk_key.y
