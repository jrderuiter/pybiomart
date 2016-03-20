

class MockResponse(object):

    def __init__(self, text=''):
        self.text = text

    def raise_for_status(self):
        pass
