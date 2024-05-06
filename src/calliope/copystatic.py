import logging
from rich.logging import RichHandler
import os
import shutil

FORMAT = "%(message)s"
logging.basicConfig(
    # level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()],
)  # set level=20 or logging.INFO to turn off debug
LOG = logging.getLogger("rich")


def copy_files_recursive(src: str, dst: str) -> None:
    mk_dir(dst)
    if not os.path.exists(src):
        raise Exception(f"`{src}` does not exist")
    paths = os.listdir(src)
    for path in paths:
        src_path = os.path.join(src, path)
        dst_path = os.path.join(dst, path)
        if os.path.isfile(src_path):
            LOG.info(f"Copying `{src_path}` to `{dst_path}`")
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)


def mk_dir(dir: str) -> None:
    if os.path.exists(dir):
        LOG.warning(f"`{dir}` already exists; doing nothing")
    else:
        LOG.info(f"Creating directory `{dir}`")
        os.mkdir(dir)
