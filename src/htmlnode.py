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

        f_props = " ".join(list(map(lambda x: f"{x[0]}: {x[1]}", self.props.items())))
        return f" {f_props}"

    def __repr__(self) -> str:
        return f"{self.tag} {self.value} {self.children} {self.props_to_html()}"
