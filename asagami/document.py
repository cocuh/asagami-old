import typing as T

from asagami.module import (
    Module,
    ModuleList,
)
from asagami.node import (
    ModuleInlineNode,
    ModuleBlockNode,
    RootNode,
)
from asagami.writer import Writer


class DocumentClass:
    modules: T.List[Module]


class Document:
    documentclass: DocumentClass
    modules: ModuleList
    root: RootNode

    def __init__(self):
        self.documentclass = None
        self.modules = ModuleList()

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
