from ward import test


from calliope.textnode import TextNode


@test("test `TextNode` equality")
def _():
    node = TextNode("This is a text node", "bold")
    node2 = TextNode("This is a text node", "bold")
    assert node == node2


@test("test `TextNode` non-equality")
def _():
    node = TextNode("This is a text node", "bold")
    node2 = TextNode("This is a text node", "italic")
    assert node != node2


@test("test `TextNode` non-equality with url")
def _():
    node = TextNode("This is a text node", "bold")
    node2 = TextNode("This is a text node", "bold", "www.google.com")
    assert node != node2


@test("test `repr` works")
def _():
    node = TextNode("This is a text node", "text", "https://www.boot.dev")
    assert "TextNode(This is a text node, text, https://www.boot.dev)" == repr(node)
