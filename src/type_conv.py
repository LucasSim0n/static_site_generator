from htmlnode import LeafNode
from textnode import TextType

# NORMAL = "normal"
# BOLD = "bold"
# ITALIC = "italic"
# CODE = "code"
# LINK = "link"
# IMAGE = "image"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(text_node.text)

        case TextType.BOLD:
            return LeafNode(text_node.text, "b")

        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")

        case TextType.CODE:
            return LeafNode(text_node.text, "code")

        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode(
                text_node.text, "img", {"src": text_node.url, "alt": text_node.text}
            )

        case _:
            raise Exception("Unknown text type")
