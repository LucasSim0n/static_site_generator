import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Image", TextType.IMAGE, "~/Imágenes/Fondos/comet.jpg")
        node2 = TextNode("Image", TextType.IMAGE, "~/Imágenes/Fondos/a.jpg")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode(
            "Image", TextType.LINK, "https://github.com/LucasSim0n/asteroids"
        )
        node2 = TextNode(
            "Image", TextType.LINK, "https://github.com/LucasSim0n/asteroids"
        )
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
