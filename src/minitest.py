from htmlnode import LeafNode, ParentNode

if __name__ == "__main__":
    child_node = LeafNode("child", "span")
    parent_node = ParentNode("div", children=[child_node])

    print(parent_node.children == None)
