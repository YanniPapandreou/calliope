from typing import List, Tuple
import re

from calliope.textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_code,
    text_type_bold,
    text_type_italic,
)

valid_delimiter_text_types = {
    "**": text_type_bold,
    "*": text_type_italic,
    "`": text_type_code,
}


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: str
) -> List[TextNode]:
    assert (
        text_type in valid_delimiter_text_types.values()
    ), f"`text_type` must be one of {list(valid_delimiter_text_types.values())}; got `{text_type = }`."
    assert (
        delimiter in valid_delimiter_text_types.keys()
    ), f"`delimiter` must be one of {list(valid_delimiter_text_types.keys())}; got `{delimiter = }`."
    assert (
        text_type == valid_delimiter_text_types[delimiter]
    ), f"`{text_type = }` does not match `{delimiter = }`, expected `{valid_delimiter_text_types[delimiter]}`."
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        num_parts = len(parts)
        if num_parts % 2 != 1:
            # delimiters are not in pairs when `num_parts` is not odd
            raise Exception(
                f"Invalid markdown syntax: must have matching closing delimiter {delimiter}."
            )
        for i, text in enumerate(parts):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, text_type_text))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def _part_to_singleton_nodes_list(part: str) -> List[TextNode]:
    if part == "":
        return []
    return [TextNode(part, text_type_text)]


def _split_node_image(node: TextNode) -> List[TextNode]:
    if node.text_type != text_type_text:
        return [node]
    images = extract_markdown_images(node.text)
    if len(images) == 0:
        return [node]
    image = images[0]
    parts = node.text.split(f"![{image[0]}]({image[1]})", 1)
    image_node = [TextNode(image[0], text_type_image, image[1])]
    first_node = _part_to_singleton_nodes_list(parts[0])
    if len(images) == 1:
        last_node = _part_to_singleton_nodes_list(parts[1])
        return first_node + image_node + last_node
    assert parts[1] != ""
    return (
        first_node + image_node + _split_node_image(TextNode(parts[1], text_type_text))
    )


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    if len(old_nodes) == 1:
        return _split_node_image(old_nodes[0])
    return _split_node_image(old_nodes[0]) + split_nodes_image(old_nodes[1:])


def _split_node_link(node: TextNode) -> List[TextNode]:
    if node.text_type != text_type_text:
        return [node]
    links = extract_markdown_links(node.text)
    if len(links) == 0:
        return [node]
    link = links[0]
    parts = node.text.split(f"[{link[0]}]({link[1]})", 1)
    link_node = [TextNode(link[0], text_type_link, link[1])]
    first_node = _part_to_singleton_nodes_list(parts[0])
    if len(links) == 1:
        last_node = _part_to_singleton_nodes_list(parts[1])
        return first_node + link_node + last_node
    assert parts[1] != ""
    return first_node + link_node + _split_node_link(TextNode(parts[1], text_type_text))


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    if len(old_nodes) == 1:
        return _split_node_link(old_nodes[0])
    return _split_node_link(old_nodes[0]) + split_nodes_link(old_nodes[1:])


def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, text_type_text)
    textnodes = split_nodes_delimiter([node], "`", text_type_code)
    textnodes = split_nodes_delimiter(textnodes, "**", text_type_bold)
    textnodes = split_nodes_delimiter(textnodes, "*", text_type_italic)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
