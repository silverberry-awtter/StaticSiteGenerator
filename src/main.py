#print("hello world")

#from textnode import TextNode, TextType
from copystatic import sync_static_to_public
from generate_page import generate_page, generate_pages_recursive

def main():
    # Creating a new TextNode object with the requested dummy values
#    node = TextNode(
#        "This is some anchor text",
#        TextType.LINK,
#        "https://www.boot.dev"
#    )

    # Printing the object to verify the __repr__ format
#    print(node)

    sync_static_to_public()

#    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

# This ensures main() only runs if main.py is executed directly
if __name__ == "__main__":
    main()
