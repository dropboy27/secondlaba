from pathlib import Path
from loguru import logger


def cat(file: str):
    path = Path(file)
    if not path.is_file():
        logger.error(f"Файл не найден или является дерикторией {file}")
        raise FileNotFoundError(path)
    content = path.read_text(encoding="utf-8")
    print(content)
