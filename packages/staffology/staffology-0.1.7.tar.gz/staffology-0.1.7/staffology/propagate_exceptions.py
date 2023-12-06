import httpx



class StaffologyApiException(Exception):
    def __init__(self, *a, **kw):
        self.response = kw.pop("response")
        super().__init__(*a)


def raise_staffology_exception(response: httpx.Response):
    raise StaffologyApiException(response=response)
