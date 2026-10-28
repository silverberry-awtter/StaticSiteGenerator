import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from generate_page import extract_title

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

### Heading 3 with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3 with <b>bold</b> text</h3></div>"
        )

    def test_lists(self):
        md = """
- Item 1 with **bold**
- Item 2

1. First item
2. Second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1 with <b>bold</b></li><li>Item 2</li></ul><ol><li>First item</li><li>Second item</li></ol></div>"
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Invalid heading examples:
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> and a second line of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        broken_block = "> Valid line\nInvalid line without chevron"
        self.assertEqual(block_to_block_type(broken_block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        broken_block = "- Item 1\n* Broken item format mismatch"
        self.assertEqual(block_to_block_type(broken_block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # Test broken tracking sequence sequence index
        broken_seq = "1. First\n3. Wrong sequence count"
        self.assertEqual(block_to_block_type(broken_seq), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "Just a typical sentence that does not use markdown blocks."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)



class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Spaced Title   "), "Spaced Title")

    def test_extract_title_multiline(self):
        md = "Some random text\n# Actual Title\n- list item"
        self.assertEqual(extract_title(md), "Actual Title")

    def test_extract_title_missing(self):
        with self.assertRaises(ValueError):
            extract_title("## Only an h2 tag here")


if __name__ == "__main__":
    unittest.main()
