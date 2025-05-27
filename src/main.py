from text_node import TextNode, TextType


def main():
    poc = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(poc)


if __name__ == "__main__":
    main()
