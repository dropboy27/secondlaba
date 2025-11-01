from pathlib import Path


class PathDoesNotExist(Exception):
    def __init__(self, path=None):
        self.path = path
        if path:
            super().__init__(f"Директории не существует: {path}")
        else:
            super().__init__("Директории не существует")


class NotADirectoryPath(Exception):
    def __init__(self):
        super().__init__("Это не директория")


class NotAFile(Exception):
    def __init__(self):
        super().__init__("Это не файл")


class NotRecursive(Exception):
    def __init__(self):
        super().__init__("Для рекурсивного удаления директории необходим -r")
