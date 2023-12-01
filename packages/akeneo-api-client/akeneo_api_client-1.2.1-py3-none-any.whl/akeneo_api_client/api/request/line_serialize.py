import json

from .json_serializable import JsonSerializable


class LineSerialize(JsonSerializable):

    def __init__(self):
        self.items = []

    def add_item(self, item: dict) -> None:
        self.items.append(json.dumps(item))

    def add_items(self, items: list[dict]) -> None:
        for item in items:
            self.add_item(item)

    def serialize(self) -> str:
        return "\n".join(self.items)
