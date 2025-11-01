import stat
from pathlib import Path
from datetime import datetime
from src.Exceptions.Exc import (PathDoesNotExist, NotADirectoryPath)
from loguru import logger


def ls(entered_path: str, arg: str = "") -> None:
    path = Path(entered_path)

    if not path.exists():
        logger.error(f"Путь не существует {entered_path}")
        raise PathDoesNotExist(path)
    if not path.is_dir():
        logger.error(f"Путь не является директорией {entered_path}")
        raise NotADirectoryPath(path)
    if arg == '-l':
        for file in path.iterdir():
            ftime = datetime.fromtimestamp(file.stat().st_mtime)
            mtime_str = ftime.strftime('%Y-%m-%d %H:%M:%S')
            file_size = file.stat().st_size
            if file_size < 1024:
                file_size = f"{file_size} байт"
            elif file_size < 1024**2:
                file_size = f"{file_size/1024:.3f} Кб"
            elif file_size < 1024**3:
                file_size = f"{file_size/1024**2:.3f} Мб"
            else:
                file_size = f"{file_size/1024**3:.3f} Гб"
            print(
                f"{file.name} {file_size} {mtime_str} {stat.filemode(file.stat().st_mode)}")
            logger.success(f"{arg} ls {entered_path}")
    else:
        for file in path.iterdir():
            print(file.name)
    logger.success(f"{arg} ls {entered_path}")
