import shutil
import os
import sys
from pathlib import Path
from loguru import logger
from src.Exceptions.Exc import (
    PathDoesNotExist, NotADirectoryPath, NotRecursive, NotAFile)

from src.ls_comand import ls
from src.cd_comand import cd
from src.cat_comand import cat
from src.cp_comand import cp
from src.mv_comand import mv
from src.rm_comand import rm
from src.grep_comand import grep
from src.zip_comand import zip_archive
from src.unzip_comand import unzip_archive
from src.tar_comand import tar_archive
from src.untar_comand import untar_archive
from src.history import add_to_history, history, undo

logger.remove()

logger.add("shell.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")


def main() -> None:
    """Главная функция эмулятора shell"""
    while True:
        try:
            # получаем текущую директорияю, чтобы она отображалась как в линухе
            current_dir = os.getcwd()
            user_input = input(f"{current_dir}$ ").strip()

            # пропускаем enter
            if not user_input:
                continue

            # Разбиваем команду на части
            parts = user_input.split()
            command = parts[0]

            if command == "exit":
                print("Выход")
                break

            if command == "help":
                print("Доступные команды:")
                print("  ls [путь] [-l]       - список файлов")
                print("  cd [путь]            - смена директории")
                print("  cat [файл]           - вывод содержимого файла")
                print("  cp [-r] [источник] [назначение] - копирование")
                print("  mv [источник] [назначение]      - перемещение")
                print("  rm [-r] [путь]       - удаление")
                print("  grep [шаблон] [путь] [-r] [-i]  - поиск по шаблону")
                print("  zip [путь] [имя]     - создать zip архив")
                print("  unzip [архив]        - распаковать zip")
                print("  tar [путь] [имя]     - создать tar архив")
                print("  untar [архив]        - распаковать tar")
                print("  history [число]      - показать историю команд")
                print("  undo                 - отменить последнюю команду")
                print("  exit                 - выход")
                continue

            add_to_history(user_input)

            if command == "ls":
                # Если пользователь ввел ls, значит выдаем ему окманду ls от текущей директории
                if len(parts) == 1:
                    ls(".")
                elif len(parts) == 2:
                    # если пользователь ввел команду и -l, то ls -l от текущей директории
                    if parts[1] == "-l":
                        ls(".", "-l")
                    # Если пользователь ввел команду и директорию, то ls от директории
                    else:
                        ls(parts[1])
                # если пользователь ввел все три аргумента, то выводим ls -l
                elif len(parts) == 3:
                    if parts[2] == "-l":
                        ls(parts[1], parts[2])
                    else:
                        print("Команда введена неверно")
                        logger.error(user_input)

            elif command == "cd":
                if len(parts) == 1:
                    cd(str(Path.home()))
                else:
                    cd(parts[1])

            elif command == "cat":
                if len(parts) < 2:
                    print("Комманда введена неверно: cat <файл>")
                else:
                    cat(parts[1])

            elif command == "cp":
                if len(parts) == 4 and parts[1] == "-r":
                    cp(parts[2], parts[3], parts[1])
                elif len(parts) == 3:
                    cp(parts[1], parts[2])
                else:
                    print("Комманда введена неверно: cp -r <источник> <назначение>")

            elif command == "mv":
                if len(parts) < 3:
                    print("Комманда введена неверно: mv <источник> <назначение>")
                else:
                    mv(parts[1], parts[2])

            elif command == "rm":
                if len(parts) == 3 and parts[1] == "-r":
                    rm(parts[2], "-r")
                elif len(parts) == 2:
                    rm(parts[1])
                else:
                    print("Комманда введена неверно: rm -r <путь>")

            elif command == "grep":
                if len(parts) < 2:
                    print(
                        "Комманда введена неверно: grep <шаблон> [путь] [-r] [-i]")
                    continue
                for i in range(2, len(parts)):
                    if parts[i] == "-r":
                        recursive = "-r"
                    elif parts[i] == "-i":
                        ignore_case = "-i"
                    else:
                        path = parts[i]
                grep(parts[1], path, recursive, ignore_case)

            elif command == "zip":
                if len(parts) == 3:
                    zip_archive(parts[2], parts[1])
                elif len(parts) == 2:
                    zip_archive(parts(1))
                else:
                    print("Комманда введена неверно: unzip <aрхив>")

            elif command == "unzip":
                if len(parts) < 2:
                    print("Комманда введена неверно: unzip <архив>")
                else:
                    unzip_archive(parts[1])

            elif command == "tar":
                if len(parts) == 3:
                    tar_archive(parts[1], parts[2])
                elif len(parts) == 2:
                    tar_archive(parts[1])
                else:
                    print("Комманда введена неверно: tar <путь> [имя архива]")

            elif command == "untar":
                if len(parts) < 2:
                    print("Комманда введена неверно: untar <архив>")
                else:
                    untar_archive(parts[1])

            elif command == "history":
                if len(parts) == 2:
                    history(parts[1])
                else:
                    history()

            elif command == "undo":
                undo()

            else:
                print(f"Неизвестная команда: {command}")
                print("Введите 'help' для списка доступных команд")

        except Exception as e:
            logger.error(f"Ошибка выполнения команды: {e}")
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
