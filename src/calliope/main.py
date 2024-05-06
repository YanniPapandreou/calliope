import os
import shutil

from calliope.copystatic import copy_files_recursive
from calliope.generator import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if os.path.exists(dir_path_public):
        print(f"Deleting public directory: `{dir_path_public}`...")
        shutil.rmtree(dir_path_public)

    print(
        f"Copying static files from `{dir_path_static}` to public directory `{dir_path_public}`..."
    )
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
