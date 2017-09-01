import typing as T

from asagami.node import (
    ModuleInlineNode,
    ModuleBlockNode,
    RenderStrategy,
    Renderer,
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


class CodeInlineRenderStrategy(RenderStrategy):
    def render_html(self, renderer: Renderer, writer: Writer, node: CodeInlineNode):
        writer.write(f'<code>{node.value}</code>')


CodeInlineNode.render_strategy = CodeInlineRenderStrategy


class CodeBlockNode(ModuleBlockNode):
    name = 'code'

    def set_options(
            self,
            lang: T.Optional[str] = None,
            schema: T.Optional[str] = None,
    ):
        self.lang = lang
        self.schema = schema


class CodeBlockRenderStrategy(RenderStrategy):
    def render_html(self, renderer: Renderer, writer: Writer, node: CodeBlockNode):
        writer.write('<code>')
        with writer.indent():
            for line in node.body.splitlines():
                writer.write(f'{line}')
        writer.write('</code>')


CodeBlockNode.render_strategy = CodeBlockRenderStrategy


class CodeInlineModule(InlineModule):
    name = 'code'
    start_signature = None
    end_signature = None
    node_class = CodeInlineNode


class CodeBlockModule(BlockModule):
    name = 'code'
    node_class = CodeBlockNode
