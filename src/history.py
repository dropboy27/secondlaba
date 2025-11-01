import os
import shutil
from pathlib import Path
from loguru import logger

PROJECT_DIR = Path(__file__).parent.parent
HISTORY_FILE = PROJECT_DIR / ".history"
TRASH_DIR = PROJECT_DIR / ".trash"


def add_to_history(command):
    """Добавляет команду в историю"""
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(command + '\n')


def history(number: int = 10):
    """Выводит последние N команд из истории с номерами"""
    if number <= 0:
        print("Число должно быть положительным")
        return None
    if not os.path.exists(HISTORY_FILE):
        print("История пуста")
        return None

    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) == 0:
        print("История пуста")
        return None

    last_comands = lines[-number:]

    start_number = len(lines) - len(last_comands) + 1
    for i in range(len(last_comands)):
        comand = last_comands[i].strip()
        print(f"{start_number + i}. {comand}")

    return lines[-1].strip()


def remove_last_from_history():
    """Удаляет последнюю команду из истории"""
    if not os.path.exists(HISTORY_FILE):
        return

    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) == 0:
        return

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        for i in range(len(lines) - 1):
            f.write(lines[i])


def undo():
    """Отменяет последнюю команду cp, mv или rm"""

    if not os.path.exists(HISTORY_FILE):
        print("История команд пуста")
        logger.error("История команд пуста")
        return 0

    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) == 0:
        print("История команд пуста")
        logger.error("История команд пуста")
        return 0

    last_comand = lines[-1].strip()

    parts = last_comand.split()

    if last_comand[0] != 'cp' and last_comand[0] != 'mv' and last_comand[0] != 'rm':
        print("Невозможно отменить команду")
        logger.error("Невозможно отменить команду")
        return 0

    command = parts[0]
    source = parts[1]
    destination = parts[2]

    if command == "cp":
        undo_cp(destination)
    elif command == "mv":
        undo_mv(source, destination)
    elif command == "rm":
        undo_rm(source)
    else:
        print(f"Команда {command} не поддерживает отмену")
        logger.error(f"Команда {command} не поддерживает отмену")
        return

    remove_last_from_history()


def undo_cp(destination):
    """Отмена команды cp - удаление скопированного файла"""
    try:
        if os.path.isfile(destination):
            os.remove(destination)
            print(f"Удален скопированный файл: {destination}")
            logger.success(f"undo cp {destination}")
        elif os.path.isdir(destination):
            shutil.rmtree(destination)
            print(f"Удален скопированный каталог: {destination}")
            logger.success(f"undo cp {destination}")
        else:
            print(f"Файл или каталог не найден: {destination}")
            logger.error(f"Файл или каталог не найден: {destination}")
    except Exception as e:
        print(f"Ошибка при отмене cp: {e}")
        logger.error(f"Ошибка при отмене cp: {e}")


def undo_mv(source, destination):
    """Отмена команды mv - возврат объекта в исходное место"""
    try:
        if os.path.exists(destination):
            shutil.move(destination, source)
            print(f"Перемещено обратно: {destination} -> {source}")
            logger.success(f"undo mv {source} {destination}")
        else:
            print(f"Файл или каталог не найден: {destination}")
            logger.error(f"Файл или каталог не найден: {destination}")
    except Exception as e:
        print(f"Ошибка при отмене mv: {e}")
        logger.error(f"Ошибка при отмене mv: {e}")


def undo_rm(source):
    """Отмена команды rm - восстановление из .trash"""
    try:
        filename = os.path.basename(source)
        trash_path = os.path.join(TRASH_DIR, filename)

        if os.path.exists(trash_path):
            shutil.move(trash_path, source)
            print(f"Восстановлено из корзины: {source}")
            logger.success(f"undo rm {source}")
        else:
            print(f"Файл не найден в корзине: {filename}")
            logger.error(f"Файл не найден в корзине: {filename}")
    except Exception as e:
        print(f"Ошибка при отмене rm: {e}")
        logger.error(f"Ошибка при отмене rm: {e}")
