import abc
import typing as T

from asagami.writer import Writer


class Node:
    name: T.ClassVar[str]
    renderer: T.ClassVar[T.Type['Renderer']]

    def __len__(self):
        '''
        :return: the number of children 
        '''
        return 0


N = T.TypeVar('N')


class Renderer(T.Generic[N]):
    def __init__(self, document, env, render_mode):
        self.document = document
        self.env = env

        render_method = {
            'html': self.render_html,
            'xml': self.render_xml,
        }.get(render_mode, None)
        if render_method is None:
            raise ValueError('invalid render mode')
        self.render = render_method

    def render_html(self, writer: Writer, node: N):
        raise NotImplementedError

    def render_xml(self, writer: Writer, node: N):
        raise NotImplementedError


class RootNode:
    name: T.ClassVar[str] = 'root'
    children: T.List[Node]

    def __init__(self):
        self.children = []

    def add_child(self, child: Node):
        self.children.append(child)


class RootNodeRenderer(Renderer[RootNode]):
    def render_html(self, writer: Writer, node: RootNode):
        with writer.indent:
            for child in node.children:
                child.render(writer)


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


class LineBlockNodeRenderer(Renderer['LineBlockNode']):
    def render_xml(self, writer: Writer, node: N):
        writer.write('<LineBlockNode>')
        with writer.indent:
            pass
        writer.write('</LineBlockNode>')


LineBlockNode.renderer = LineBlockNodeRenderer


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


class TextNodeRenderer(Renderer[TextNode]):
    def render_default(self, writer: Writer, node: TextNode):
        writer.write(node.text)

    def render_html(self, writer: Writer, node: TextNode):
        self.render_default(writer, node)

    def render_xml(self, writer: Writer, node: TextNode):
        self.render_default(writer, node)
