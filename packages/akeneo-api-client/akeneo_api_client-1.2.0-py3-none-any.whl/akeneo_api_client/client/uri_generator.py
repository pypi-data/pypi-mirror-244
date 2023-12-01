import urllib.parse
from urllib.parse import urlencode


def bool_to_string(query_params={}) -> dict:
    for k, v in query_params.items():
        if type(v) is bool:
            query_params[k] = 'true' if v is True else 'false'

    return query_params


class UriGenerator:

    def __init__(self, base_uri):
        self.base_uri = base_uri.rstrip('/')

    def generate(self, path, uri_params=[], query_params={}):
        uri_params = tuple(map(lambda x: urllib.parse.quote(str(x)), uri_params))
        uri = self.base_uri + "/" + (path.lstrip('/') % uri_params)

        if len(query_params) > 0:
            query_params = bool_to_string(query_params)

            url_parts = list(urllib.parse.urlparse(uri))
            url_parts[4] = urlencode(query_params)
            uri = urllib.parse.urlunparse(url_parts)

        return uri
