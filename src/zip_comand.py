import shutil
from pathlib import Path
from src.Exceptions.Exc import (PathDoesNotExist, NotADirectoryPath)
from loguru import logger


def zip_archive(entered_path, archive_name=""):
    """
    Создаёт ZIP архив из каталога

    entered_path - путь к каталогу для архивации
    archive_name - имя выходного архива (без расширения)
    """

    path = Path(entered_path)

    if not path.exists():
        logger.error(f"{entered_path} не существует")
        raise PathDoesNotExist

    if not path.is_dir():
        logger.error(f"{entered_path} не является каталогом")
        raise NotADirectoryPath

    if archive_name == "":
        archive_name = path.name

    shutil.make_archive(archive_name, 'zip', path.parent, path.name)
    logger.success(f"zip {archive_name}")
