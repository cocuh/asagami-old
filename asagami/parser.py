import re
import typing as T

from . import modules
from asagami.node import (
    BlockNode,
    TextNode,
    LineBlockNode,
    ModuleBlockNode,
)
from asagami.document import (
    Document,
)


class AsagamiParser:
    metadata_exp = re.compile(
        r'^::(?P<name>[a-zA-Z0-9_]+):\s*(?P<value>[a-zA-Z0-9_]\w+)',
        re.MULTILINE,
    )  # TODO: list support
    inline_module_exp = re.compile(
        r':(?P<module_name>[a-zA-Z0-9_]+)(?P<kwargs>\{[^\}]+\})?:`(?P<value>(\\`|[^\`])+)`'
    )
    module_block_exp = re.compile(
        r'^\.\. (?P<module_name>[a-zA-Z0-9_]+)(\s*::\s*(?P<value>\w+))?\s*\n(?P<body>(    [^\n]*\n|\n)*)',
        re.MULTILINE,
    )
    module_kwargs_exp = re.compile(
        r'^\.\. (?P<name>[a-zA-Z0-9_]+)\s*:\s*(?P<value>.+?)\s*$'
    )
    line_block_exp = re.compile(
        r'^(?P<body>([^\n]+\n)*[^\n]+)',
        re.MULTILINE,
    )
    rest_exp = re.compile(
        r'(?P<body>[^\n]+(.*[^\n])*)',
        re.MULTILINE,
    )

    def parse(self, text: str) -> Document:
        document = Document()

        # metadata parse
        for k, v in re.findall(self.metadata_exp, text):
            if k == 'documentclass':
                if document.documentclass is None:
                    document.documentclass = v
            elif k == 'usemodule':
                module = getattr(modules, v, None)  # TODO: move to module loader
                if module is None:
                    raise ValueError('module not found: {}'.format(v))
                document.modules.append(module)

        # body parse
        block_list = ['\n'.join(l for l in text.splitlines() if not l.startswith('::'))]
        block_exp_list = [
            (self.module_block_exp, self.parser_factory_module_block(document)),
            (self.line_block_exp, self.parser_factory_line_block(document)),
        ]  # todo: implement ModuleBlock parsing

        for node_exp, node_factory in block_exp_list:
            def parse_block_if_possible(line: T.Union[BlockNode, str]):
                if isinstance(line, str):
                    return self.parse_block(node_exp, node_factory, line)
                return [line]

            block_list = sum(map(parse_block_if_possible, block_list), [])
        block_list = list(filter(lambda block: isinstance(block, BlockNode), block_list))
        document.children = block_list

        return document

    def parse_block(self, exp: T.Pattern, node_factory, body) -> T.List[T.Union[BlockNode, str]]:
        body_length = len(body)
        block_list = []
        pos = 0
        while pos < body_length:
            result: T.Match = exp.search(body, pos=pos)
            if result is None:
                rest_result = self.rest_exp.search(body, pos=pos)
                if rest_result is not None:
                    block_list.append(rest_result['body'])
                break
            else:
                if pos != result.start():
                    rest_result = self.rest_exp.search(body, pos=pos, endpos=result.start())
                    if rest_result is not None:
                        block_list.append(rest_result['body'])
                block_list.append(node_factory(**result.groupdict()))
                pos = result.end()
        return block_list

    def parser_factory_line_block(self, document: Document):
        def parse_line_block(body: str) -> LineBlockNode:
            body_length = len(body)
            pos = 0
            children = []
            while pos < body_length:
                result = self.inline_module_exp.search(body, pos=pos)
                if result is None:
                    rest_result = self.rest_exp.search(body, pos=pos)
                    if rest_result is not None:
                        children.append(TextNode(rest_result['body']))
                    break
                else:
                    if pos != result.start():
                        rest_result = self.rest_exp.search(body, pos=pos, endpos=result.start())
                        if rest_result is not None:
                            children.append(TextNode(rest_result['body']))  # TODO: list kwargs support
                    module_data = {
                        'module_name': result['module_name'],
                        'value': result['value'],
                        'kwargs': self.parse_module_inline_kwargs(result['kwargs']),
                    }
                    inline_module_node = document.create_module_inline_node(**module_data)
                    children.append(inline_module_node)
                    pos = result.end()
            node = LineBlockNode(children)
            return node

        return parse_line_block

    def parser_factory_module_block(self, document: Document):
        def parse_module_block(module_name: str, value: str, body: str) -> ModuleBlockNode:
            body_lines = [
                line[4:]  # indent removal
                for line in body.splitlines()
                ]
            kwargs = {}
            for idx, line in enumerate(body_lines):
                result = self.module_kwargs_exp.search(line)
                if result is None:
                    break
                else:
                    assert result['name'] not in kwargs  # TODO: impl error message
                    kwargs[result['name']] = result['value']
            return document.create_module_block_node(
                module_name=module_name, value=value, body=body, kwargs=kwargs,
            )

        return parse_module_block

    def parse_module_inline_kwargs(self, kwargs: T.Optional[str]):
        if kwargs is None:
            return {}
        result = {}
        for line in kwargs.strip('{}').split(','):
            record = line.split(':')
            assert len(record) == 2
            key, value = list(map(lambda l:l.strip(), record))
            result[key] = value
        return result
