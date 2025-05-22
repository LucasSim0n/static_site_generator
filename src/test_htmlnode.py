import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_htmlrepr(self):
        node = HTMLNode(
            tag="a",
            value="some text",
            children=None,
            props={"href": "https://poops.com", "title": "your poops site"},
        )
        xpctd_props = (
            f"a some text None  href: https://poops.com title: your poops site"
        )
        self.assertEqual(node.__repr__(), xpctd_props)


if __name__ == "__main__":
    unittest.main()
