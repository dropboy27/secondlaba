import os
from pathlib import Path
from src.Exceptions.Exc import (PathDoesNotExist, NotADirectoryPath)
from loguru import logger


def cd(entered_path: str = os.getcwd()):
    path = Path(entered_path)
    if entered_path == "~":
        logger.success(f"cd {entered_path}")
        os.chdir(Path.home())
        return
    if entered_path == "..":
        logger.success(f"cd {entered_path}")
        os.chdir("..")
        return
    if not path.exists():
        logger.error(f"Путь не существует {entered_path}")
        raise PathDoesNotExist(path)
    if not path.is_dir():
        logger.error(f"Путь не является директорией {entered_path}")
        raise NotADirectoryPath(path)

    else:
        logger.success(f"cd {entered_path}")
        os.chdir(entered_path)
