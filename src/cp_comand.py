
import shutil
from pathlib import Path
from loguru import logger
from src.Exceptions.Exc import (PathDoesNotExist, NotRecursive)


def cp(entered_path: str, destination: str, recursive=""):
    """
    Копирует файл или директорию из источника в назначение

    entered_path - путь к исходному файлу/папке
    destination - путь назначения
    recursive - флаг для рекурсивного копирования папок
    """
    src = Path(entered_path)
    dst = Path(destination)

    if not src.exists():
        logger.error(f"Файл или папка не существует {entered_path}")
        raise PathDoesNotExist()

    if src.is_file():
        if dst.is_dir():
            dst = dst / src.name
        shutil.copy2(src, dst)
        logger.success(f"cp {recursive} {entered_path} {destination}")

    elif src.is_dir():
        if recursive != '-r':
            logger.error(
                f"Для копирования папки надо использовать -r {entered_path}")
            raise NotRecursive()
        shutil.copytree(src, dst)
        logger.success(f"cp {recursive} {entered_path} {destination}")
