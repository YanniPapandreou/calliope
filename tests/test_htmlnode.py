from ward import test, each

from calliope.htmlnode import HTMLNode, LeafNode, ParentNode


@test("test `props_to_html`")
def _(
    node=each(
        HTMLNode(props={"href": "https://www.google.com", "target": "_blank"}),
        HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
                "awesome_key": "awesome_value",
            }
        ),
        HTMLNode(),
        HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        ),
    ),
    expected=each(
        ' href="https://www.google.com" target="_blank"',
        ' href="https://www.google.com" target="_blank" awesome_key="awesome_value"',
        "",
        ' class="greeting" href="https://boot.dev"',
    ),
):
    assert isinstance(node, HTMLNode)
    assert node.props_to_html() == expected


@test("test `repr` works")
def _():
    node = HTMLNode("p", "text")
    assert "HTMLNode(p, text, children: None, None)" == repr(node)


@test("test `to_html` ({desc})")
def _(
    node=each(
        LeafNode("p", "This is a paragraph of text."),
        LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
        LeafNode(None, "Hello, world!"),
        ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ),
        ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ),
    ),
    expected=each(
        "<p>This is a paragraph of text.</p>",
        '<a href="https://www.google.com">Click me!</a>',
        "Hello, world!",
        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
    ),
    desc=each(
        "when no children",
        "with props",
        "with no tag",
        "with `LeafNode` children only",
        "with headings",
    ),
):
    assert isinstance(node, HTMLNode)
    assert node.to_html() == expected


@test("test `to_html` with children")
def _():
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    assert parent_node.to_html() == "<div><span>child</span></div>"


@test("test `to_html` with grandchilren")
def _():
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    assert parent_node.to_html() == "<div><span><b>grandchild</b></span></div>"
