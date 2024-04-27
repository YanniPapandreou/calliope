from typing import List

from textnode import TextNode, text_type_text

def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: str
) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        parts = node.text.split(delimiter)
        num_parts = len(parts)
        if num_parts % 2 != 1:
            # delimiters are not in pairs when `num_parts` is not odd
            raise Exception(
                f"Invalid markdown syntax: must have matching closing delimiter {delimiter}."
            )
        for i, text in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(text, text_type_text))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes
