from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            raise Exception(f"{node.text_type} is not valid.")

        subnodes = []
        parts = node.text.split(delimiter)
        print(parts)
        for i, val in enumerate(parts):
            if i % 2 == 1:
                subnodes.append(TextNode(val, text_type))
            else:
                subnodes.append(TextNode(val, TextType.TEXT))

        new_nodes.append(subnodes)

    return new_nodes
