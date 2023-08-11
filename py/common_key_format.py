from attr import dataclass


@dataclass
class CommonKeyFormatLocation:
    def __init__(self):
        self.x: float = -1
        self.y: float = -1


@dataclass
class CommonKeyFormat:
    def __init__(self):
        relative = CommonKeyFormatLocation()
        absolute = CommonKeyFormatLocation()
        h: float = 1.0
        w: float = 1.0


CommonFormatKeys = dict[str, CommonKeyFormat]


@dataclass
class CommonKeyData:
    def __init__(self):
        list: CommonFormatKeys = dict()

    def get_from_common_keys_or_new(
        self, list: CommonFormatKeys, canonical_name: str
    ) -> CommonKeyFormat:
        item = list.get(canonical_name)
        if item == None:
            item = CommonKeyFormat()
            list[canonical_name] = item
        return item
