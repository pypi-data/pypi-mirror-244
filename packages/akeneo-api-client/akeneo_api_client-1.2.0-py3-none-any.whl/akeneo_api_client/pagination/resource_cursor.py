class ResourceCursor:

    def __init__(self, page_size, first_page):
        self.page_size = page_size
        self.current_page = first_page

    def __iter__(self):
        self.current_index = -1
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index == 0:
            return self.current_page.get_items()
        else:
            if self.current_page.has_next_page():
                next_page = self.current_page.get_next_page()
                self.current_page = next_page
                return next_page.get_items()
            else:
                raise StopIteration