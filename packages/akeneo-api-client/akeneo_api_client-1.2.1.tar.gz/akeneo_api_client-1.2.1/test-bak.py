import requests
import json
import urllib.parse

search = {
    "updated": [{"operator":">","value":"2016-07-04 10:00:00"}],
    "completeness": [{"operator": "=", "value": 100, "scope": "ecommerce"}]
}

json_str = json.dumps(search, separators=(',', ':'))
q = urllib.parse.quote(json_str)

# print(json_str)
# print(q)

response = requests.request(
    'GET',
    'https://inviqa.demo.cloud.akeneo.com/api/rest/v1/products-uuid?search='+q,
    headers={"Authorization": "Bearer ZjBhY2YxZTE4Yjc5ZWMwMjMwNWEwZmYxMDQxNzdkNjMwNWU3ZjIyMTM2ZGYyYmI2NWZjNzFlZWMxMmM5NzliYQ"}
)

print(response.json())