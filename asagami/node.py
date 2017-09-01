import abc
import typing as T

from asagami.writer import Writer


class Node:
    name: T.ClassVar[str]
    render_strategy: T.ClassVar[T.Type['RenderStrategy']]

    def __len__(self):
        '''
        :return: the number of children 
        '''
        return 0


N = T.TypeVar('N')


class Renderer:
    def __init__(self, document):
        self.render_strategy_cache = {}
        self.env = {}
        self.document = document

    def render(self, node: Node, writer: Writer):
        node_class = type(node)
        if node_class not in self.render_strategy_cache:
            render_strategy = node.render_strategy(self.document, self.env)
            self.render_strategy_cache[node_class] = render_strategy
        else:
            render_strategy = self.render_strategy_cache[node_class]
        render_strategy.render_html(self, writer, node)


class RenderStrategy(T.Generic[N]):
    def __init__(self, document, env):
        self.document = document
        self.env = env

    def render_html(self, renderer: Renderer, writer: Writer, node: N):
        raise NotImplementedError

    def render_xml(self, renderer: Renderer, writer: Writer, node: N):
        raise NotImplementedError


class RootNode(Node):
    name: T.ClassVar[str] = 'root'
    children: T.List[Node]

    def __init__(self, children: T.List[Node] = []):
        self.children = children

    def add_child(self, child: Node):
        self.children.append(child)


class RootNodeRenderStrategy(RenderStrategy[RootNode]):
    def render_html(self, renderer: Renderer, writer: Writer, node: RootNode):
        with writer.indent():
            for child in node.children:
                renderer.render(child, writer)


RootNode.render_strategy = RootNodeRenderStrategy


class InlineNode(Node):
    pass


InlineChildrenType = T.Union[InlineNode, 'TextNode']


class BlockNode(Node):
    pass


class LineBlockNode(BlockNode):
    name: T.ClassVar[str] = 'line_block'
    children: T.List[InlineChildrenType]

    def __init__(self, children: T.List[InlineChildrenType] = []):
        self.children = children

    def append_child(self, child: InlineChildrenType):
        self.children.append(child)

    def __len__(self):
        return len(self.children)


class LineBlockNodeRenderStrategy(RenderStrategy[LineBlockNode]):
    def render_html(self, renderer: Renderer, writer: Writer, node: LineBlockNode):
        writer.write('<p>')
        with writer.indent():
            for child in node.children:
                renderer.render(child, writer)
        writer.write('</p>')


LineBlockNode.render_strategy = LineBlockNodeRenderStrategy


class ModuleBlockNode(BlockNode, metaclass=abc.ABCMeta):
    def __init__(self, value, kwargs, body):
        self.value = value
        self.body = body
        self.set_options(**kwargs)

    @abc.abstractmethod
    def set_options(self, **kwargs):
        raise NotImplementedError()


class ModuleInlineNode(InlineNode, metaclass=abc.ABCMeta):
    def __init__(self, value, kwargs):
        self.value = value
        self.set_options(**kwargs)

    @abc.abstractmethod
    def set_options(self, **kwargs):
        raise NotImplementedError()


class TextNode(Node):
    name: T.ClassVar[str] = 'text'
    text: str

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return self.text


class TextNodeRenderStrategy(RenderStrategy[TextNode]):
    def render_html(self, renderer: Renderer, writer: Writer, node: N):
        writer.write(node.text)


TextNode.render_strategy = TextNodeRenderStrategy
