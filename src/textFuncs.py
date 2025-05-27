import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
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


def get_alt_and_url(text):
    alt = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    return (alt[0], url[0])


def extract_markdown_images(text):
    matches = re.findall(r"(!\[.*?\]\(.*?\))", text)
    slices = re.split(r"(!\[.*?\]\(.*?\))", text)
    return list(map(get_alt_and_url, matches)), slices


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)(\[.*?\]\(.*?\))", text)
    slices = re.split(r"(?<!!)(\[.*?\]\(.*?\))", text)
    return list(map(get_alt_and_url, matches)), slices


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        subnodes = []
        parts = node.text.split(delimiter)

        for i, val in enumerate(parts):
            if i % 2 == 1:
                subnodes.append(TextNode(val, text_type))
            else:
                subnodes.append(TextNode(val, TextType.TEXT))

        new_nodes.extend(subnodes.copy())

    return new_nodes


def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # raise Exception(f"{node.text_type} is not valid.")
            new_nodes.append(node)
            continue

        images, slices = extract_markdown_images(node.text)
        subnodes = []
        img_index = 0

        if len(images) == 0:
            new_nodes.extend([TextNode(node.text, TextType.TEXT)])
            continue

        for i, slice in enumerate(slices):
            if i % 2 == 1:
                subnodes.append(
                    TextNode(images[img_index][0], TextType.IMAGE, images[img_index][1])
                )
                img_index += 1
            else:
                if len(slice) == 0:
                    continue
                subnodes.append(TextNode(slice, TextType.TEXT))
        new_nodes.extend(subnodes.copy())

    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links, slices = extract_markdown_links(node.text)
        subnodes = []
        link_index = 0

        if len(links) == 0:
            new_nodes.extend([TextNode(node.text, TextType.TEXT)])
            continue

        for i, slice in enumerate(slices):
            if len(slice) == 0:
                continue

            if i % 2 == 1:
                subnodes.append(
                    TextNode(links[link_index][0], TextType.LINK, links[link_index][1])
                )
                link_index += 1

            else:
                if len(slice) == 0:
                    continue

                subnodes.append(TextNode(slice, TextType.TEXT))

        new_nodes.extend((subnodes.copy()))

    return new_nodes


def text_to_textnodes(text):
    result = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
                    ),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
    return result


if __name__ == "__main__":
    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    real = text_to_textnodes(
        "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    )
