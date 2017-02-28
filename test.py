from asagami.parser import AsagamiParser
from asagami.writer import Writer


def main():
    parser = AsagamiParser()
    document = parser.parse(open('test.ag').read())
    print(document)
    print(document.children)

    writer = Writer()
    writer = document.render(writer, 'html')
    print(writer.dump())


if __name__ == '__main__':
    main()
