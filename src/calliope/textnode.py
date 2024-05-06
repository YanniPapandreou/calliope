from typing import Optional

from calliope.htmlnode import HTMLNode, LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

valid_text_types = [
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
]


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, TextNode)
        return (
            (self.text == __value.text)
            and (self.text_type == __value.text_type)
            and (self.url == __value.url)
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        assert text_node.url is not None
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        assert text_node.url is not None
        assert text_node.text is not None
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception(
        f"Invalid text node: `text_type` must be one of `{valid_text_types}`; got {text_node.text_type = }"
    )
