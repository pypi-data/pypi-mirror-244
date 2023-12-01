import json

from .json_serializable import JsonSerializable


class DictSerialize(JsonSerializable):

    def __init__(self, obj: dict):
        self.obj = obj

    def serialize(self) -> str:
        return json.dumps(self.obj)
