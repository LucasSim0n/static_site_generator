import unittest

from text_funcs import extract_markdown_images, extract_markdown_links


class TestMdExtracction(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches[0])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://github.com)"
        )
        self.assertListEqual([("link", "https://github.com")], matches[0])


if __name__ == "__main__":
    unittest.main()
