class Writer:
    def __init__(self):
        self.data = ''

    def write(self, str):
        self.data += str

    def dump(self):
        return self.data
