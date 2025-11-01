import os
import shutil
from pathlib import Path
from src.Exceptions.Exc import (PathDoesNotExist, NotADirectoryPath, NotAFile)
from loguru import logger


def unzip_archive(entered_path):
    """
    Распаковывет Zip архив в текущюю директорию

    entered_path - путь к каталогу для распковки
    """

    path = Path(entered_path)

    if not path.exists():
        logger.error(f"{entered_path} не существует")
        raise PathDoesNotExist

    if not path.is_file():
        logger.error(f"{entered_path} не является файлом")
        raise NotAFile

    shutil.unpack_archive(path, os.getcwd(), 'zip')
    logger.success(f"unzip {entered_path}")
