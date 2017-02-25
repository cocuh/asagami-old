from asagami.node import (
    ModuleInlineNode,
    ModuleBlockNode,
)
from asagami.module import (
    InlineModule,
    BlockModule,
)


class CodeInlineNode(ModuleInlineNode):
    name = 'code'


class CodeBlockNode(ModuleBlockNode):
    name = 'code'


class CodeInlineModule(InlineModule):
    name = 'code'
    start_signature = None
    end_signature = None
    node_class = CodeInlineNode


class CodeBlockModule(BlockModule):
    name = 'code'
    node_class = CodeBlockNode
