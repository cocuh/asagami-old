import typing as T

from asagami.node import (
    ModuleInlineNode,
    ModuleBlockNode,
)
from asagami.module import (
    InlineModule,
    BlockModule,
)
from asagami.writer import Writer


class CodeInlineNode(ModuleInlineNode):
    name = 'code'

    def set_options(
            self,
            lang: str = '',
    ):
        self.lang = lang

    def render_html(self, writer: Writer):
        writer.write(f'<code>{self.value}</code>')


class CodeBlockNode(ModuleBlockNode):
    name = 'code'

    def set_options(
            self,
            lang: T.Optional[str] = None,
            schema: T.Optional[str] = None,
    ):
        self.lang = lang
        self.schema = schema


class CodeInlineModule(InlineModule):
    name = 'code'
    start_signature = None
    end_signature = None
    node_class = CodeInlineNode


class CodeBlockModule(BlockModule):
    name = 'code'
    node_class = CodeBlockNode
