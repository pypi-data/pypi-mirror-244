from .page import Page


class PageFactory:

    def __init__(self, authenticated_http_client):
        self.authenticated_http_client = authenticated_http_client

    def create_page(self, json):
        try:
            next_link = json["_links"]["next"]["href"]
        except KeyError:
            next_link = ""

        try:
            first_link = json["_links"]["first"]["href"]
        except KeyError:
            first_link = ""

        return Page(
            PageFactory(self.authenticated_http_client),
            self.authenticated_http_client,
            first_link,
            next_link,
            json["_embedded"]["items"]
        )
