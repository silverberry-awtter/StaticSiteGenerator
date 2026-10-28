from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        # If it's not a raw text node, we skip splitting it completely
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Split the text string by the delimiter string
        sections = old_node.text.split(delimiter)

        # A pair of delimiters always splits a string into an ODD number of sections.
        # e.g., "text `code` text" -> ['text ', 'code', 'text'] (Length 3)
        # If the length is even, it means a closing delimiter is missing!
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: matching closing delimiter '{delimiter}' not found in text: '{old_node.text}'")

        split_nodes = []
        for i in range(len(sections)):
            # Skip empty sections (handles empty strings if delimiter is at the very beginning/end)
            if sections[i] == "":
                continue

            # Even indices (0, 2, 4...) are outside the delimiters -> TextType.TEXT
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            # Odd indices (1, 3, 5...) are inside the delimiters -> Target text_type
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)



def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            image_alt = image[0]
            image_url = image[1]
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes



def text_to_textnodes(text):
    # Start with the entire raw markdown string wrapped as a single text node
    nodes = [TextNode(text, TextType.TEXT)]

    # 1. Split markdown images first
    nodes = split_nodes_image(nodes)

    # 2. Split markdown links next
    nodes = split_nodes_link(nodes)

    # 3. Split bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # 4. Split italic text (handles both common flavors * and _)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # 5. Split code block inline text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

