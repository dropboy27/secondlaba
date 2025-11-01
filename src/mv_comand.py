import shutil
from pathlib import Path
from loguru import logger
from src.Exceptions.Exc import (PathDoesNotExist)


def mv(source, destination):
    src = Path(source)
    dst = Path(destination)

    if not src.exists():
        logger.error(f"Файл или папка '{source}' не найдена")
        raise PathDoesNotExist()

    if dst.is_dir():
        dst = dst / src.name

    shutil.move(str(src), str(dst))
    logger.success(f"mv {source} {destination}")
