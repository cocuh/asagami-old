import contextlib


class Writer:
    def __init__(self, space_num=4):
        self.data = ''
        self.indent_num = 0
        self.space_num = space_num

    @contextlib.contextmanager
    def indent(self):
        self.indent_num += 1
        yield
        self.indent_num -= 1

    def write(self, string: str):
        self.data += string

    def dump(self):
        return self.data
