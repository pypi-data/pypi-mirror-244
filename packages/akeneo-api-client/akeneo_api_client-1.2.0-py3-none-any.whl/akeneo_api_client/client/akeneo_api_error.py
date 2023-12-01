import json
from requests.models import Response


class AkeneoApiError(Exception):

    def __init__(self, response: Response):
        self.message = "unknown error"
        self.response = response
        self.response_body = None

        content = response.content
        if len(content) > 0:
            body = json.loads(content.decode('utf-8'))

            self.response_body = body

            if isinstance(body, dict) and "message" in body:
                self.message = body["message"]

        super().__init__(self.message)