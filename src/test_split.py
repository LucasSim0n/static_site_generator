import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplit(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("code block", TextType.CODE, None),
                TextNode(" word", TextType.TEXT, None),
            ]
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("code block", TextType.ITALIC, None),
                TextNode(" word", TextType.TEXT, None),
            ]
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("This is text with a *code block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("code block", TextType.BOLD, None),
                TextNode(" word", TextType.TEXT, None),
            ]
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
