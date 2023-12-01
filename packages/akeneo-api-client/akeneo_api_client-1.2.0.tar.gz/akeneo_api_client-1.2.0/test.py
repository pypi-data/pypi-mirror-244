import requests
import json
import urllib.parse


query_params = {'search': '[]', 'with_count':False}

for k, v in query_params.items():
    if type(v) is bool:
        query_params[k] = 'true' if v is True else 'false'

print(query_params)

# sb = SearchBuilder()
# sb.add_filter('updated', '>', '2020-01-01 00:00:00')
# sb.add_filter('completeness', '=', 100, {"scope": "ecommerce"})
# search = sb.get_filters()
# print(search)

# search = {
#     "updated": [{"operator":">","value":"2016-07-04 10:00:00"}],
#     "completeness": [{"operator": "=", "value": 100, "scope": "ecommerce"}]
# }
#
# json_str = json.dumps(search, separators=(',', ':'))
# q = urllib.parse.quote(json_str)
#
# response = requests.request(
#     'GET',
#     'https://inviqa.demo.cloud.akeneo.com/api/rest/v1/products-uuid?search='+q,
#     headers={"Authorization": "Bearer ZjBhY2YxZTE4Yjc5ZWMwMjMwNWEwZmYxMDQxNzdkNjMwNWU3ZjIyMTM2ZGYyYmI2NWZjNzFlZWMxMmM5NzliYQ"}
# )
#
# print(response.json())