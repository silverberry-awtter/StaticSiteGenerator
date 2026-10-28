

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else None
        self.props = props if props is not None else None

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""

        attributes = []
        for key, value in self.props.items():
            attributes.append(f' {key}="{value}"')
        return "".join(attributes)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # A leaf node cannot have children, so we explicitly pass None to super()
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value.")

        # If there is no tag, render the value as raw text
        if self.tag is None:
            return self.value

        # Otherwise, wrap the value in the opening and closing HTML tags
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # ParentNode does not take a value argument
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if self.children is None:
            raise ValueError("Invalid HTML: ParentNode must have children")

        # Recursively call to_html on all children and join them together
        children_html = "".join([child.to_html() for child in self.children])

        # Wrap the children's HTML inside the parent's tags (including props)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
