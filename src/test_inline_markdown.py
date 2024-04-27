import unittest

from inline_markdown import split_nodes_delimiter
from textnode import (
    TextNode,
    text_type_code,
    text_type_text,
    text_type_bold,
    text_type_italic,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_delim_code_double(self):
        node = TextNode("This is text with a `code block` and another `code word`.", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and another ", text_type_text),
                TextNode("code word", text_type_code),
                TextNode(".", text_type_text),
            ],
            new_nodes,
    )

    def test_split_nodes_delim_bold(self):
        node = TextNode("This is text with a **bold** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_delim_bold_double(self):
        node = TextNode("This is text with a **bold** word and **another** bold word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
                TextNode(" bold word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_delim_italic_double(self):
        node = TextNode("This is text with an *italic* word and an *italic ending*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and an ", text_type_text),
                TextNode("italic ending", text_type_italic),
                TextNode("", text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_multi(self):
        node_1 = TextNode("This is text with a `code block` word", text_type_text)
        node_2 = TextNode("This is text with a **bold** word", text_type_text)
        node_3 = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter(
            [node_1, node_2, node_3], "**", text_type_bold
        )
        self.assertEqual(
            [
                node_1,
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
                node_3,
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
