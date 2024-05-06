from ward import test, each

from calliope.inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from calliope.textnode import (
    TextNode,
    text_type_code,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_image,
    text_type_link,
)


@test("test `split_nodes_delimiter` for single code block")
def _():
    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" word", text_type_text),
    ]


@test("test `split_nodes_delimiter` for two code blocks")
def _():
    node = TextNode(
        "This is text with a `code block` and another `code word`.", text_type_text
    )
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" and another ", text_type_text),
        TextNode("code word", text_type_code),
        TextNode(".", text_type_text),
    ]


@test("test `split_nodes_delimiter` for single bold word")
def _():
    node = TextNode("This is text with a **bold** word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bold", text_type_bold),
        TextNode(" word", text_type_text),
    ]


@test("test `split_nodes_delimiter` for two bold words")
def _():
    node = TextNode(
        "This is text with a **bold** word and **another** bold word",
        text_type_text,
    )
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bold", text_type_bold),
        TextNode(" word and ", text_type_text),
        TextNode("another", text_type_bold),
        TextNode(" bold word", text_type_text),
    ]


@test("test `split_nodes_delimiter` for single italic word")
def _():
    node = TextNode("This is text with an *italic* word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    assert new_nodes == [
        TextNode("This is text with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word", text_type_text),
    ]


@test("test `split_nodes_delimiter` for two italic words")
def _():
    node = TextNode(
        "This is text with an *italic* word and an *italic ending*", text_type_text
    )
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    assert new_nodes == [
        TextNode("This is text with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word and an ", text_type_text),
        TextNode("italic ending", text_type_italic),
    ]


@test("test `split_nodes_delimiter` multi")
def _():
    node_1 = TextNode("This is text with a `code block` word", text_type_text)
    node_2 = TextNode("This is text with a **bold** word", text_type_text)
    node_3 = TextNode("This is text with an *italic* word", text_type_text)
    new_nodes = split_nodes_delimiter([node_1, node_2, node_3], "**", text_type_bold)
    assert new_nodes == [
        node_1,
        TextNode("This is text with a ", text_type_text),
        TextNode("bold", text_type_bold),
        TextNode(" word", text_type_text),
        node_3,
    ]


@test("test delim bold")
def _():
    node = TextNode("This is text with a **bolded** word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bolded", text_type_bold),
        TextNode(" word", text_type_text),
    ]


@test("test delim bold double")
def _():
    node = TextNode(
        "This is text with a **bolded** word and **another**", text_type_text
    )
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bolded", text_type_bold),
        TextNode(" word and ", text_type_text),
        TextNode("another", text_type_bold),
    ]


@test("test delim bold multiword")
def _():
    node = TextNode(
        "This is text with a **bolded word** and **another**", text_type_text
    )
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bolded word", text_type_bold),
        TextNode(" and ", text_type_text),
        TextNode("another", text_type_bold),
    ]


@test("test delim italic")
def _():
    node = TextNode("This is text with an *italic* word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    assert new_nodes == [
        TextNode("This is text with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word", text_type_text),
    ]


@test("test delim code")
def _():
    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" word", text_type_text),
    ]


@test("test `extract_markdown_images`")
def _(
    text=each(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
    ),
    expected=each(
        [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ],
        [("image", "https://i.imgur.com/zjjcJKZ.png")],
    ),
):
    assert isinstance(text, str)
    assert extract_markdown_images(text) == expected


@test("test `extract_markdown_links`")
def _(
    text=each(
        "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)",
    ),
    expected=each(
        [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ],
        [
            ("link", "https://boot.dev"),
            ("another link", "https://blog.boot.dev"),
        ],
    ),
):
    assert isinstance(text, str)
    assert extract_markdown_links(text) == expected


@test("test `split_nodes_image` {desc}")
def _(
    node=each(
        TextNode(
            "This is text with a single ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) found online.",
            text_type_text,
        ),
        TextNode(
            "This is text with a single ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text,
        ),
        TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) only.",
            text_type_text,
        ),
        TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text,
        ),
        TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        ),
        TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        ),
        TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        ),
        TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        ),
    ),
    expected=each(
        [
            TextNode("This is text with a single ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" found online.", text_type_text),
        ],
        [
            TextNode("This is text with a single ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
        ],
        [
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" only.", text_type_text),
        ],
        [
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
        ],
        [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ],
        [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        [
            TextNode("image", text_type_image, "https://www.example.com/image.png"),
        ],
        [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
    ),
    desc=each(
        "(single node - single image)",
        "(single node - single ending image)",
        "(single node - single starting image)",
        "(single node - only image text)",
        "(single node - multiple images)",
        "(split image)",
        "(split image single)",
        "(split images)",
    ),
):
    assert isinstance(node, TextNode)
    new_nodes = split_nodes_image([node])
    assert new_nodes == expected


@test("test `split_nodes_image` (multiple nodes)")
def _():
    nodes = [
        TextNode(
            "This is text with a single ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) found online.",
            text_type_text,
        ),
        TextNode(
            "This is text with a single ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text,
        ),
        TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) only.",
            text_type_text,
        ),
        TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            text_type_text,
        ),
        TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        ),
    ]
    expected_nodes = [
        TextNode("This is text with a single ", text_type_text),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
        ),
        TextNode(" found online.", text_type_text),
        TextNode("This is text with a single ", text_type_text),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
        ),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
        ),
        TextNode(" only.", text_type_text),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
        ),
        TextNode("This is text with an ", text_type_text),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
        ),
        TextNode(" and another ", text_type_text),
        TextNode(
            "second image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
        ),
    ]
    new_nodes = split_nodes_image(nodes)
    assert new_nodes == expected_nodes


@test("test `split_nodes_link` {desc}")
def _(
    node=each(
        TextNode(
            "This is text with a single [link](https://my-link.com) found online.",
            text_type_text,
        ),
        TextNode(
            "This is text with a single [link](https://my-link.com)",
            text_type_text,
        ),
        TextNode(
            "[link](https://my-link.com) only.",
            text_type_text,
        ),
        TextNode(
            "[link](https://my-link.com)",
            text_type_text,
        ),
        TextNode(
            "This is text with an [link](https://my-link.com) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        ),
        TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        ),
    ),
    expected=each(
        [
            TextNode("This is text with a single ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://my-link.com",
            ),
            TextNode(" found online.", text_type_text),
        ],
        [
            TextNode("This is text with a single ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://my-link.com",
            ),
        ],
        [
            TextNode(
                "link",
                text_type_link,
                "https://my-link.com",
            ),
            TextNode(" only.", text_type_text),
        ],
        [
            TextNode(
                "link",
                text_type_link,
                "https://my-link.com",
            ),
        ],
        [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://my-link.com",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ],
        [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("another link", text_type_link, "https://blog.boot.dev"),
            TextNode(" with text that follows", text_type_text),
        ],
    ),
    desc=each(
        "(single node - single link)",
        "(single node - single ending link)",
        "(single node - single starting link)",
        "(single node - only link text)",
        "(single node - multiple links)",
        "(split links)",
    ),
):
    assert isinstance(node, TextNode)
    new_nodes = split_nodes_link([node])
    assert new_nodes == expected


@test("test `split_nodes_link` (multiple nodes)")
def _():
    nodes = [
        TextNode(
            "This is text with a single [link](https://my-link.com) found online.",
            text_type_text,
        ),
        TextNode(
            "This is text with a single [link](https://my-link.com)",
            text_type_text,
        ),
        TextNode(
            "[link](https://my-link.com) only.",
            text_type_text,
        ),
        TextNode(
            "[link](https://my-link.com)",
            text_type_text,
        ),
        TextNode(
            "This is text with an [link](https://my-link.com) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        ),
    ]
    expected_nodes = [
        TextNode("This is text with a single ", text_type_text),
        TextNode(
            "link",
            text_type_link,
            "https://my-link.com",
        ),
        TextNode(" found online.", text_type_text),
        TextNode("This is text with a single ", text_type_text),
        TextNode(
            "link",
            text_type_link,
            "https://my-link.com",
        ),
        TextNode(
            "link",
            text_type_link,
            "https://my-link.com",
        ),
        TextNode(" only.", text_type_text),
        TextNode(
            "link",
            text_type_link,
            "https://my-link.com",
        ),
        TextNode("This is text with an ", text_type_text),
        TextNode(
            "link",
            text_type_link,
            "https://my-link.com",
        ),
        TextNode(" and another ", text_type_text),
        TextNode(
            "second link",
            text_type_link,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
        ),
    ]
    new_nodes = split_nodes_link(nodes)
    assert new_nodes == expected_nodes


@test("test `text_to_textnodes`")
def _():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    expected_textnodes = [
        TextNode("This is ", text_type_text),
        TextNode("text", text_type_bold),
        TextNode(" with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word and a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" and an ", text_type_text),
        TextNode(
            "image",
            text_type_image,
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
        ),
        TextNode(" and a ", text_type_text),
        TextNode("link", text_type_link, "https://boot.dev"),
    ]
    textnodes = text_to_textnodes(text)
    assert textnodes == expected_textnodes
