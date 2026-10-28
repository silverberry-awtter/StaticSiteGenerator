import sys
from copystatic import sync_static_to_public
from generate_page import generate_pages_recursive

def main():
    # Default base path is standard root "/"
    basepath = "/"

    # If a command-line argument is provided, capture it as the basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Building site with active base path: '{basepath}'")

    # 1. Clear out public/ and duplicate assets
    sync_static_to_public()

    # 2. Walk layout structures and bake templates with the custom base path
    generate_pages_recursive("content", "template.html", "public", basepath)

if __name__ == "__main__":
    main()
