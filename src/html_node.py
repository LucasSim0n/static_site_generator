class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            raise ValueError("'props' not defined for this node")

        f_props = " ".join(list(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items())))
        return f" {f_props}"

    def __repr__(self) -> str:
        return f"{self.tag} {self.value} {self.children} {self.props_to_html()}"


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        match self.tag:
            case None:
                return self.value
            case "a":
                return f"<a {self.props_to_html()}>{self.value}</a>"
            case "img":
                return f"<img {self.props_to_html()}/>"
            case _:
                return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError(f"Parent nodes must have a tag")

        if self.children == None:
            raise ValueError("Parent nodes must have children nodes")

        result = "".join(list(map(lambda x: x.to_html(), self.children)))

        return f"<{self.tag}>{result}</{self.tag}>"
