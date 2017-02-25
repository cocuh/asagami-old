from asagami.parser import AsagamiParser


def main():
    parser = AsagamiParser()
    document = parser.parse(open('test.ag').read())
    print(document)
    print(document.children)


if __name__ == '__main__':
    main()
