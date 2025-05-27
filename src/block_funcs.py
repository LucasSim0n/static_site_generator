import re

from block_type import BlockType
from html_node import *
from text_funcs import text_node_to_html_node, text_to_textnodes
from text_node import TextNode, TextType


def block_to_block_type(block):
    if re.match(r"^#{1,6}\s", block):  # encabezados tipo #, ##, etc.
        return BlockType.HEADING
    elif re.match(r"^```", block):  # bloques de código
        return BlockType.CODE
    elif re.match(r"^>", block):  # citas
        return BlockType.QUOTE
    elif re.match(r"^-", block):  # lista no ordenada
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.", block):  # lista ordenada
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
    parts = block.split("\n")
    list_elements = list(map(lambda x: f"<li>{x}</li>", parts))
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

            return LeafNode(text, f"h{head_type}")

        case BlockType.UNORDERED_LIST:
            list_elements = get_list_html(text)
            return ParentNode("ul", list_elements)

        case BlockType.ORDERED_LIST:
            list_elements = get_list_html(text)
            return ParentNode("ol", list_elements)

        case BlockType.QUOTE:
            return LeafNode(text, "blockquote")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)
        child = text_to_children(block, block_type)

        child_blocks.append(child)

    return ParentNode("div", child_blocks)
