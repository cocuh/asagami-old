from asagami.node import Renderer
from asagami.parser import AsagamiParser
from asagami.writer import Writer


def main():
    parser = AsagamiParser()
    document = parser.parse(open('test.ag').read())
    print(document)

    writer = Writer()
    renderer = Renderer(document)
    renderer.render(document.root, writer)
    print(writer.dump())


if __name__ == '__main__':
    main()
