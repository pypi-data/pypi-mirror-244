class Page:

    def __init__(self, page_factory, http_client, first_link, next_link, items):
        self.page_factory = page_factory
        self.http_client = http_client
        self.first_link = first_link
        self.next_link = next_link
        self.items = items

    def get_first_page(self):
        return self.get_page(self.first_link)

    def get_next_page(self):
        return self.get_page(self.next_link)

    def get_items(self):
        return self.items

    def has_next_page(self):
        return self.next_link != ""

    def get_next_link(self):
        return self.next_link

    def get_page(self, uri):
        response = self.http_client.send_request("GET", uri, {"Accept": "*/*"})
        return self.page_factory.create_page(response.json())
