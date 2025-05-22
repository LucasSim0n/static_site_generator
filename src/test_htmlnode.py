import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_htmlrepr(self):
        node = HTMLNode(
            tag="a",
            value="some text",
            children=None,
            props={"href": "https://poops.com", "title": "your poops site"},
        )
        xpctd_props = (
            f'a some text None  href="https://poops.com" title="your poops site"'
        )
        self.assertEqual(node.__repr__(), xpctd_props)

    def test_leaf_to_html_p(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
