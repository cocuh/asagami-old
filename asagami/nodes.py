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


class InlineNode(Node):
    pass


class ModuleInlineNode(InlineNode):
    def __init__(self, value, kwargs):
        pass


class Module:
    name: str = ''
    node_class: Node = None


class InlineModule(Module):
    start_signature: T.Optional[str] = None
    end_signature: T.Optional[str] = None
    node_class: InlineNode = None

    def __init__(self, value, kwargs):
        pass


class BlockModule(Module):
    shorten_pattern: T.Optional[T.re.Pattern[str]] = None
    node_class: ModuleBlockNode = None

    def is_target(self, line: str) -> bool:
        raise NotImplementedError


class BoldInlineNode(InlineNode):
    children: T.List[InlineChildrenType]


class DocumentClass:
    modules: T.List[Module]


class ModuleList:
    modules: T.List[Module]
    inline_modules: T.List[InlineModule]
    block_modules: T.List[Module]

    def __init__(self):
        self.modules = []
        self.inline_modules = {}
        self.block_modules = {}

    def append(self, module: T.Type[Module]):
        self.modules.append(module)
        if issubclass(module, InlineModule):
            assert module.name not in self.inline_modules
            self.inline_modules[module.name] = module
        if issubclass(module, BlockModule):
            assert module.name not in self.block_modules
            self.block_modules[module.name] = module

    def search_inline_module(self, name: str):
        return self.inline_modules[name]

    def search_block_module(self, name: str):
        return self.block_modules[name]


class Document:
    documentclass: DocumentClass
    modules: ModuleList
    children: T.List[Node]

    def __init__(self):
        self.documentclass = None
        self.modules = ModuleList()
        self.children = []

    def append_child(self, child):
        self.children.append(child)

    def create_module_block_node(self, module_name, value, kwargs, body) -> ModuleBlockNode:
        module_class = self.modules.search_block_module(module_name)
        node_class = module_class.node_class
        node = node_class(value=value, kwargs=kwargs, body=body)
        return node

    def create_module_inline_node(self, module_name, value, kwargs) -> ModuleInlineNode:
        module_class = self.modules.search_inline_module(module_name)
        node_class = module_class.node_class
        node = node_class(value=value, kwargs=kwargs)
        return node
