from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


def markdown_to_blocks(markdown):
    # Split the raw document by double newlines
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in raw_blocks:
        # Strip leading/trailing whitespace from the block
        stripped = block.strip()
        # Only keep the block if it contains actual text
        if stripped != "":
            filtered_blocks.append(stripped)

    return filtered_blocks




class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # 1. Headings check
    if block.startswith("#"):
        # Max out check up to 6 characters
        for i in range(1, 7):
            if block.startswith("#" * i + " "):
                return BlockType.HEADING

    # 2. Code block check
    # In Boot.dev, code blocks start with 3 backticks and end with 3 backticks
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Split multiline blocks to run row-by-row checks
    lines = block.split("\n")

    # 3. Quote check
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # 4. Unordered list check
    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # 5. Ordered list check (Must start exactly at 1 and increment by 1 sequentially)
    is_ordered_list = True
    for idx, line in enumerate(lines):
        expected_start = f"{idx + 1}. "
        if not line.startswith(expected_start):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # 6. Fallback default
    return BlockType.PARAGRAPH



def text_to_children(text):
    """Converts a raw string of text into a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            # Join multiple consecutive lines into a single paragraph string
            lines = block.split("\n")
            paragraph_text = " ".join([line.strip() for line in lines])
            children = text_to_children(paragraph_text)
            block_nodes.append(ParentNode("p", children))

        elif block_type == BlockType.HEADING:
            # Count the number of leading hashes to determine the header level
            num_hashes = len(block) - len(block.lstrip("#"))
            text = block[num_hashes + 1:] # Skip the hashes and the space
            children = text_to_children(text)
            block_nodes.append(ParentNode(f"h{num_hashes}", children))

        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            text_node = TextNode(code_text, TextType.TEXT)
            code_node = ParentNode("code", [text_node_to_html_node(text_node)])
            block_nodes.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            # Strip the > character and clean up each line
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.lstrip("> ").strip())
            quote_text = " ".join(cleaned_lines)
            children = text_to_children(quote_text)
            block_nodes.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                # Remove the "- " prefix
                item_text = line[2:]
                children = text_to_children(item_text)
                li_nodes.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ul", li_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                # Find where the period and space end to cut off the numbering prefix
                prefix_end = line.find(". ") + 2
                item_text = line[prefix_end:]
                children = text_to_children(item_text)
                li_nodes.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ol", li_nodes))

    # Wrap all generated blocks inside a parent div block container
    return ParentNode("div", block_nodes)


