import shutil
import os
import time
from pathlib import Path
from src.Exceptions.Exc import (PathDoesNotExist, NotRecursive)
from loguru import logger


def rm(file, recursive=""):
    """
    Удаляет файл или каталог, перемещая в .trash

    file - путь к файлу/папке для удаления
    recursive - флаг для рекурсивного удаления каталогов
    """
    path = Path(file)

    if not path.exists():
        logger.error(f"Файла не существует {file}")
        raise PathDoesNotExist()

    if file == "/" or file == ".." or file == "~":
        logger.error(f"Запрещено удалять: {file}")
        print(f"Ошибка: запрещено удалять {file}")
        return

    if path.is_file():
        move_to_trash(path)
        logger.success(f"Файл {file} перемещён в корзину")
        print(f"Файл {file} перемещён в корзину")

    elif path.is_dir():
        if recursive != "-r":
            logger.error("Не введен  -r для рекурсивного удаления")
            raise NotRecursive()

        confirmation = input(
            f"Вы уверены, что хотите удалить директорию '{file}'? (y/n): ").strip().lower()
        if confirmation != 'y':
            print("Удаление отменено")
            logger.info(f"Удаление директории {file} отменено пользователем")
        else:
            move_to_trash(path)
            logger.success(f"Директория {file} перемещена в корзину")
            print(f"Директория {file} перемещена в корзину")


def move_to_trash(path):
    """
    Перемещает файл или директорию в корзину
    path - объект для перемещения
    """
    delete_time = int(time.time())
    name_parts = path.name.rsplit('.', 1)

    if len(name_parts) == 2:
        new_name = f"{name_parts[0]}_{delete_time}.{name_parts[1]}"
    else:
        new_name = f"{path.name}_{delete_time}"

    project_dir = Path(__file__).parent.parent
    trash_dir = project_dir / ".trash"

    if not trash_dir.exists():
        trash_dir.mkdir()

    trash_path = trash_dir / new_name
    shutil.move(str(path), str(trash_path))
