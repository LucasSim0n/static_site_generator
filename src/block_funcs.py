import re

from block_type import BlockType
from html_node import *
from text_funcs import text_node_to_html_node, text_to_textnodes


def block_to_block_type(block):
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    elif re.match(r"^```", block):
        return BlockType.CODE
    elif re.match(r"^>", block):
        return BlockType.QUOTE
    elif re.match(r"^-", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    trtd_blocks = []
    for block in raw_blocks:
        if block.isspace():
            continue
        trtd_blocks.append(block.strip())

    return trtd_blocks


def get_list_html(block):

    list_elements = []

    parts = block.split("\n")
    stripped = list(map(lambda x: x.strip("0123456789.- "), parts))
    treated = list(map(text_to_textnodes, stripped))

    for element in treated:
        list_elements.append(
            ParentNode("li", [text_node_to_html_node(x) for x in element])
        )

    return list_elements


def text_to_children(text, b_type):
    match b_type:
        case BlockType.PARAGRAPH:
            fixed = " ".join(text.split())
            nodes = text_to_textnodes(fixed)
            html_nodes = list(map(text_node_to_html_node, nodes))
            return ParentNode("p", html_nodes)

        case BlockType.CODE:
            fixed = text.strip("`\n ") + "\n"
            return ParentNode("pre", [LeafNode(fixed, "code")])

        case BlockType.HEADING:
            head_type = 0
            for char in text:
                if char != "#":
                    break
                head_type += 1

            return LeafNode(text[head_type + 1 :], f"h{head_type}")

        case BlockType.UNORDERED_LIST:
            list_elements = get_list_html(text)
            return ParentNode("ul", list_elements)

        case BlockType.ORDERED_LIST:
            list_elements = get_list_html(text)
            return ParentNode("ol", list_elements)

        case BlockType.QUOTE:
            return LeafNode(text[2:], "blockquote")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)
        child = text_to_children(block, block_type)

        child_blocks.append(child)

    return ParentNode("div", child_blocks)


def extract_title(markdown):
    header = re.findall(r"^#\s(.*)", markdown)
    if not header:
        raise Exception("No h1 found")

    return header[0]
