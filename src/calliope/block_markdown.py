from typing import List

from calliope.htmlnode import HTMLNode, LeafNode, ParentNode
from calliope.textnode import text_node_to_html_node
from calliope.inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(md: str) -> List[str]:
    blocks = md.split("\n\n")
    stripped_blocks = map(lambda block: block.strip(), blocks)
    filtered_blocks = filter(lambda block: block != "", stripped_blocks)
    return list(filtered_blocks)


def block_to_block_type(block: str) -> str:
    match block[0]:
        case "#":
            heading_text = block.split()[0]
            heading_chars = set(heading_text)
            if heading_chars != {"#"}:
                raise Exception(f"Invalid markdown heading block: {block = }.")
            heading_level = len(heading_text)
            if heading_level > 6:
                raise Exception(
                    f"Invalid markdown heading block: heading level must be between 1-6; got {heading_level = }."
                )
            return block_type_heading
        case "`":
            if block[0:3] != "```":
                raise Exception(
                    "Invalid markdown code block; code blocks must start with three backticks."
                )
            if block[-3:] != "```":
                raise Exception(
                    "Invalid markdown code block; code blocks must end with three backticks."
                )
            return block_type_code
        case ">":
            lines = block.split("\n")
            for line in lines:
                if line[0] != ">":
                    raise Exception(
                        "Invalid markdown quote block; all lines of a quote block must start with '>'"
                    )
            return block_type_quote
        case "*":
            lines = block.split("\n")
            for line in lines:
                if line[:2] != "* ":
                    raise Exception(
                        "Invalid markdown unordered list; all lines of an unordered list must start with '*' or '-' followed by space"
                    )
            return block_type_unordered_list
        case "-":
            lines = block.split("\n")
            for line in lines:
                if line[:2] != "- ":
                    raise Exception(
                        "Invalid markdown unordered list; all lines of an unordered list must start with '*' or '-' followed by space"
                    )
            return block_type_unordered_list

    match block[:2]:
        case "1.":
            lines = block.split("\n")
            for i, line in enumerate(lines):
                line_start = line[:3]
                if line_start != f"{i+1}. ":
                    raise Exception(
                        "Invalid markdown ordered list; all lines of an ordered list must start with a number followed by a '.' character and a space. The number must start at 1 and increment by 1 for each line."
                    )
            return block_type_ordered_list
        case _:
            if block[1] == ".":
                try:
                    starting_int = int(block[0])
                except ValueError:
                    return block_type_paragraph
                assert starting_int > 1
                raise Exception(
                    f"Invalid markdown ordered list; ordered lists must start numbering from 1; got {starting_int}."
                )

            return block_type_paragraph


def text_to_children(text: str) -> List[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = list(map(lambda node: text_node_to_html_node(node), text_nodes))
    return children


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    assert block_to_block_type(block) == block_type_paragraph
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_block_to_html_node(block: str) -> HTMLNode:
    assert block_to_block_type(block) == block_type_heading
    heading_chars, heading_text = block.split(maxsplit=1)
    heading_level = len(heading_chars)
    children = text_to_children(heading_text)
    return ParentNode(f"h{heading_level}", children)


def code_block_to_html_node(block: str) -> HTMLNode:
    assert block_to_block_type(block) == block_type_code
    code_text = block.strip("```").lstrip("\n")
    inner_node = LeafNode("code", code_text)
    outer_node = ParentNode("pre", [inner_node])
    return outer_node


def quote_block_to_html_node(block: str) -> HTMLNode:
    assert block_to_block_type(block) == block_type_quote
    quote_content = " ".join(
        map(lambda line: line.lstrip(">").strip(), block.split("\n"))
    )
    children = text_to_children(quote_content)
    return ParentNode("blockquote", children)


def unordered_list_block_to_html_node(block: str) -> HTMLNode:
    assert block_to_block_type(block) == block_type_unordered_list
    list_symbol = block[:2]
    nodes = map(
        lambda line: ParentNode("li", text_to_children(line.lstrip(list_symbol))),
        block.split("\n"),
    )
    return ParentNode("ul", list(nodes))


def ordered_list_block_to_html_node(block: str) -> HTMLNode:
    assert block_to_block_type(block) == block_type_ordered_list
    nodes = map(
        lambda line: ParentNode("li", text_to_children(line[3:])), block.split("\n")
    )
    return ParentNode("ol", list(nodes))


block_functions_map = {
    block_type_ordered_list: ordered_list_block_to_html_node,
    block_type_unordered_list: unordered_list_block_to_html_node,
    block_type_code: code_block_to_html_node,
    block_type_quote: quote_block_to_html_node,
    block_type_heading: heading_block_to_html_node,
    block_type_paragraph: paragraph_block_to_html_node,
}


def markdown_to_html_node(md: str) -> HTMLNode:
    blocks = markdown_to_blocks(md)
    children = list(
        map(
            lambda block: block_functions_map[block_to_block_type(block)](block), blocks
        )
    )
    return ParentNode("div", children)
