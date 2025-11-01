import os
import re
from pathlib import Path
import shutil
from loguru import logger


def grep(pattern, entered_path='.', recursive="", ignore_case=""):

    ignore_case_flag = 0
    if ignore_case == "-i":
        ignore_case_flag = re.IGNORECASE

    try:
        reg = re.compile(pattern, ignore_case_flag)
    except re.error as e:
        logger.error(f"Ошибка в регулярном выражении: {e}")
        print(f"Ошибка в регулярном выражении: {e}")
        return 0

    path = Path(entered_path)

    files = []

    if path.is_file():
        files = [path]
    elif path.is_dir():
        if recursive:
            files = [f for f in path.rglob('*') if f.is_file()]
        else:
            files = [f for f in path.iterdir() if f.is_file()]
    else:
        logger.error(f"Путь не существует: {path}")
        print(f"Путь не существует: {path}")
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                line_num = 1
                for line in file:
                    matches = reg.finditer(line)

                    for match in matches:
                        found_fragment = match.group()

                        print(f"{entered_path}:{line_num}:{found_fragment}")
                    line_num += 1
        except Exception as e:
            logger.error(e)
            return 0
