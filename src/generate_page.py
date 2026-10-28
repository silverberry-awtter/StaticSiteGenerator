import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    """
    Extracts the first h1 level header text from a markdown document.
    Raises an exception if an h1 header is missing.
    """
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Invalid Markdown: Missing an h1 (# ) heading layer.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read input files
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Process text into HTML components
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)

    # Inject elements into template placeholders
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_string)

    # Ensure destination directories exist prior to writing file
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively crawls the content directory, finds all markdown files,
    and generates corresponding HTML files in the destination directory.
    """
    # Loop over every entry inside the current content directory layer
    for item in os.listdir(dir_path_content):
        # Build the absolute system paths
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path):
            # Only process markdown files
            if item.endswith(".md"):
                # Change the extension from .md to .html for the destination filename
                html_filename = item[:-3] + ".html"
                dest_path = os.path.join(dest_dir_path, html_filename)

                # Use our existing function to convert the file
                generate_page(src_path, template_path, dest_path)
        else:
            # If it's a directory, map out the matching target subdirectory
            nested_dest_dir = os.path.join(dest_dir_path, item)

            # Recurse down into the nested folder structure
            generate_pages_recursive(src_path, template_path, nested_dest_dir)
