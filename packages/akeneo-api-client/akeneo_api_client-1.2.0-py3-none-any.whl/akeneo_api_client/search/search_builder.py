import json


class SearchBuilder:
    def __init__(self):
        self.filters = {}

    def add_filter(self, property: str, operator: str, value = None, options = {}) -> None:
        filter = {"operator": operator}

        if value is not None:
            filter["value"] = value

        self.filters[property] = [filter|options]

    def get_filters(self) -> str:
        return json.dumps(self.filters, separators=(',', ':'))
