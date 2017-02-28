import typing as T

from asagami.node import (
    Node,
    InlineNode,
    ModuleBlockNode,
)


class Module:
    name: T.ClassVar[str] = ''
    node_class: T.ClassVar[Node] = None


class InlineModule(Module):
    start_signature: T.ClassVar[T.Optional[str]] = None
    end_signature: T.ClassVar[T.Optional[str]] = None
    node_class: T.ClassVar[InlineNode]


class BlockModule(Module):
    shorten_pattern: T.Optional[T.re.Pattern[str]] = None
    node_class: ModuleBlockNode = None

    def is_target(self, line: str) -> bool:
        raise NotImplementedError


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
