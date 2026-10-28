import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Invalid Markdown: Missing an h1 (# ) heading layer.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} with basepath {basepath}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_string)

    # Dynamically inject the configurable base path for asset routes
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path):
            if item.endswith(".md"):
                html_filename = item[:-3] + ".html"
                dest_path = os.path.join(dest_dir_path, html_filename)
                # Forward the basepath to the individual file generator
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            nested_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, nested_dest_dir, basepath)
