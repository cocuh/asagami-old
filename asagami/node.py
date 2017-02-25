import typing as T


class Node:
    name: str = None

    def __len__(self):
        return 0


class TextNode(Node):
    text: str

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return self.text


class InlineNode(Node):
    pass


InlineChildrenType = T.Union[InlineNode, TextNode]


class BlockNode(Node):
    pass


class LineBlockNode(BlockNode):
    children: T.List[InlineChildrenType]

    def __init__(self, children: T.List[InlineChildrenType] = []):
        self.children = children

    def append_child(self, child: InlineChildrenType):
        self.children.append(child)

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return '<LineNode children=[{!r}]>'.format(
            ', '.join(
                map(repr, self.children)
            )
        )


class ModuleBlockNode(BlockNode):
    def __init__(self, value, kwargs, body):
        pass


class ModuleInlineNode(InlineNode):
    def __init__(self, value, kwargs):
        pass
