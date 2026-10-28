import sys
from copystatic import sync_static_to_public
from generate_page import generate_pages_recursive

def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Building site with active base path: '{basepath}'")

    # 1. Clear out docs/ and duplicate assets (We change this from sync_static_to_public)
    sync_static_to_public("static", "docs")

    # 2. Compile templates directly into the docs/ folder
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
