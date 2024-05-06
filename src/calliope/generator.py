import os
import pathlib

from calliope.block_markdown import markdown_to_html_node


def extract_title(md: str) -> str:
    lines = md.split("\n")
    match = list(filter(lambda line: line.startswith("# "), lines))
    if len(match) == 0:
        raise Exception("Invalid markdown page: all pages need a single h1 header.")
    return match[0].lstrip("# ")


def generate_page(
    from_path: os.PathLike, template_path: os.PathLike, dest_path: os.PathLike
) -> None:
    print(
        f"Generating page from `{from_path}` to `{dest_path}` using `{template_path}`"
    )
    with open(from_path, "r") as f_md:
        md = f_md.read()
    with open(template_path, "r") as f_template:
        template = f_template.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title, 1).replace(
        "{{ Content }}", content, 1
    )
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f_out:
        f_out.write(page)


def generate_pages_recursive(
    dir_path_content: os.PathLike,
    template_path: os.PathLike,
    dest_dir_path: os.PathLike,
) -> None:
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    paths = os.listdir(dir_path_content)
    for path in paths:
        path_from_src = pathlib.Path(os.path.join(dir_path_content, path))
        if os.path.isfile(path_from_src):
            generate_page(
                path_from_src,
                template_path,
                os.path.join(
                    dest_dir_path,
                    path_from_src.name.replace(path_from_src.suffix, ".html"),
                ),
            )
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, path_from_src.name),
                template_path,
                os.path.join(dest_dir_path, path_from_src.name),
            )
