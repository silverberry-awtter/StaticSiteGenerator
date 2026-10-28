import unittest
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_split_multiple_delimiters(self):
        node = TextNode("Start **bold 1** middle **bold 2** end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold 1", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("bold 2", TextType.BOLD),
                TextNode(" end", TextType.TEXT),
            ]
        )

    def test_missing_closing_delimiter(self):
        node = TextNode("This is **broken bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_preserves_non_text_nodes(self):
        bold_node = TextNode("Already Bold", TextType.BOLD)
        text_node = TextNode("Normal with `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold_node, text_node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Already Bold", TextType.BOLD),
                TextNode("Normal with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ]
        )



class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            matches
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            matches
        )

    def test_links_do_not_extract_images(self):
        # The lookbehind pattern (?<!!) prevents image tags from being extracted as links
        text = "Here is an ![image alt](https://example.com) and a [real link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("real link", "https://example.com")], matches)

    def test_extract_empty_alt_and_anchor(self):
        text = "Empty image ![](https://example.com) and empty link [](https://example.com)"
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)

        self.assertListEqual([("", "https://example.com")], img_matches)
        self.assertListEqual([("", "https://example.com")], link_matches)



class TestInlineMarkdownSplits(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode("[Google](https://google.com) is a search engine", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" is a search engine", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("Look at this logo ![python](https://python.org)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Look at this logo ", TextType.TEXT),
                TextNode("python", TextType.IMAGE, "https://python.org"),
            ],
            new_nodes,
        )

    def test_no_links_or_images(self):
        node = TextNode("Just plain text with no markdown shortcuts.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))
        self.assertListEqual([node], split_nodes_image([node]))



class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ],
            nodes
        )

    def test_text_to_textnodes_simple_bold(self):
        text = "Only **bold** syntax here."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Only ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" syntax here.", TextType.TEXT),
            ],
            nodes
        )

    def test_text_to_textnodes_plain(self):
        text = "This is completely raw text with zero markdown decorations."
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)


if __name__ == "__main__":
    unittest.main()
