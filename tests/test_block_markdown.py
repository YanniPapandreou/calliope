from ward import test, each, raises

from calliope.block_markdown import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)


@test("test `markdown_to_blocks`")
def _():
    md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
    expected_blocks = [
        "This is **bolded** paragraph",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "* This is a list\n* with items",
    ]
    assert markdown_to_blocks(md) == expected_blocks


@test("test `markdown_to_blocks` with extra new lines")
def _():
    md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
    expected_blocks = [
        "This is **bolded** paragraph",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "* This is a list\n* with items",
    ]
    assert markdown_to_blocks(md) == expected_blocks


@test("test `block_to_block_type` {desc}")
def _(
    block=each(
        "This is a **bolded** paragraph.",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "# Heading 1",
        "## Heading 2",
        "### Heading 3",
        "#### Heading 4",
        "##### Heading 5",
        "###### Heading 6",
        "```\ndef f(x):\n    return x\n```",
        "> This is a quote on a single line.",
        "> This is a quote on multiple lines\n> This is the second line of the quote.",
        "* This is a list with one item.",
        "* This is a list\n* with several items.",
        "1. This is a list with one item.",
        "1. This is a list\n2. with several items.",
    ),
    expected=each(
        block_type_paragraph,
        block_type_paragraph,
        block_type_heading,
        block_type_heading,
        block_type_heading,
        block_type_heading,
        block_type_heading,
        block_type_heading,
        block_type_code,
        block_type_quote,
        block_type_quote,
        block_type_unordered_list,
        block_type_unordered_list,
        block_type_ordered_list,
        block_type_ordered_list,
    ),
    desc=each(
        "(single-line paragraph)",
        "(multi-line paragraph)",
        "(heading 1)",
        "(heading 2)",
        "(heading 3)",
        "(heading 4)",
        "(heading 5)",
        "(heading 6)",
        "(code block)",
        "(single-line quote)",
        "(multi-line quote)",
        "(unordered list with single item)",
        "(unordered list with several items)",
        "(ordered list with single item)",
        "(ordered list with several items)",
    ),
):
    assert isinstance(block, str)
    assert block_to_block_type(block) == expected


@test("test `block_to_block_type` with invalid markdown blocks {desc}")
def _(
    block=each(
        "#Heading 1",
        "##Heading 2",
        "###Heading 3",
        "####### Heading with too many #'s",
        "```\ndef f(x):\n    return x\n``",
        "```\ndef f(x):\n    return x\n`",
        "```\ndef f(x):\n    return x\n",
        "> This is a quote on multiple lines\nThis is the second line of the quote.",
        "* This is a list\n with several items.",
        "1. This is a list\n3. with several items.",
        "1.This is a list\n2. with several items.",
        "1. This is a list\n2.with several items.",
        "1. This is a list\n with several items.",
        "2. This is a list.",
    ),
    intended_type=each(
        block_type_heading,
        block_type_heading,
        block_type_heading,
        block_type_heading,
        block_type_code,
        block_type_code,
        block_type_code,
        block_type_quote,
        block_type_unordered_list,
        block_type_ordered_list,
        block_type_ordered_list,
        block_type_ordered_list,
        block_type_ordered_list,
        block_type_ordered_list,
    ),
    desc=each(
        "(level 1 heading with no space after '#')",
        "(level 2 heading with no space after '##')",
        "(level 3 heading with no space after '###')",
        "(heading with to many levels)",
        "(code block with incorrect ending #1)",
        "(code block with incorrect ending #2)",
        "(code block with incorrect ending #3)",
        "(quote without a '>' on all lines)",
        "(unordered list without a '*' on all lines)",
        "(ordered list with incorrect numbering)",
        "(ordered list without space after numbering #1)",
        "(ordered list without space after numbering #2)",
        "(ordered list without numbers on each line)",
        "(ordered list which does not start from 1)",
    ),
):
    exception_dict = {
        block_type_heading: "Invalid markdown heading block",
        block_type_code: "Invalid markdown code block",
        block_type_quote: "Invalid markdown quote block",
        block_type_unordered_list: "Invalid markdown unordered list",
        block_type_ordered_list: "Invalid markdown ordered list",
    }
    assert isinstance(block, str)
    assert isinstance(intended_type, str)
    with raises(Exception) as ex:
        block_to_block_type(block)
    assert str(ex.raised).startswith(exception_dict[intended_type])


@test("test `markdown_to_html_node` {desc}")
def _(
    md=each(
        """
This is **bolded** paragraph
text in a p
tag here

""",
        """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

""",
        """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

""",
        """
# this is an h1

this is paragraph text

## this is an h2
""",
        """
> This is a
> blockquote block

this is paragraph text

""",
    ),
    expected=each(
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
    ),
    desc=each(
        "(single paragraph)",
        "(multiple paragraphs)",
        "(lists)",
        "(headings)",
        "(blockquote)",
    ),
):
    assert isinstance(md, str)
    node = markdown_to_html_node(md)
    html = node.to_html()
    assert html == expected
