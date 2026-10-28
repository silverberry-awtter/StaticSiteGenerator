import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_formatting(self):
        # Tests standard formatting with multiple properties and leading spaces
        node = HTMLNode(
            tag="a",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty_or_none(self):
        # Tests that an empty or missing props dictionary returns an empty string
        node_none = HTMLNode(tag="p", props=None)
        node_empty = HTMLNode(tag="p", props={})

        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_repr_output(self):
        # Tests that the debugging string representation works correctly
        node = HTMLNode(
            tag="p",
            value="Hello world",
            props={"class": "text-paragraph"}
        )
        expected_repr = "HTMLNode(tag='p', value='Hello world', children=None, props={'class': 'text-paragraph'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_raises_error(self):
        # Verifies that calling to_html on the base class throws the correct error
        node = HTMLNode(tag="div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        # Tests standard tag wrapping without properties
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        # Tests standard tag wrapping with attributes included
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        # Tests that no tag renders purely the text string
        node = LeafNode(None, "This is raw text without a tag.")
        self.assertEqual(node.to_html(), "This is raw text without a tag.")

    def test_leaf_to_html_missing_value(self):
        # Verifies that omitting a value explicitly triggers a ValueError
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        # Verifies the string representation formats without showing children
        node = LeafNode("b", "Bold text", {"class": "important"})
        expected_repr = "LeafNode(tag='b', value='Bold text', props={'class': 'important'})"
        self.assertEqual(repr(node), expected_repr)



class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "hello")],
            {"class": "wrapper", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="wrapper" id="main"><span>hello</span></div>'
        )

    def test_missing_tag(self):
        node = ParentNode(None, [LeafNode("span", "hello")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: ParentNode must have a tag")

    def test_missing_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: ParentNode must have children")


if __name__ == "__main__":
    unittest.main()

