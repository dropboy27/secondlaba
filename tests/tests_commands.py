import pytest
import os
import shutil
from pathlib import Path
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
from src.Exceptions.Exc import PathDoesNotExist, NotADirectoryPath, NotRecursive


def test_cd_to_home():
    """Проверяем, что cd ~ переходит в домашнюю директорию"""
    cd("~")
    assert os.getcwd() == str(Path.home())


def test_cd_nonexistent_path(tmp_path):
    """Проверяем, что cd выбрасывает ошибку для несуществующего пути"""
    nonexistent = tmp_path / "nonexistent_dir_12345"
    with pytest.raises(PathDoesNotExist):
        cd(str(nonexistent))


def test_cat_existing_file(tmp_path, capsys):
    """Проверяем, что cat читает содержимое файла"""
    test_file = tmp_path / "test.txt"
    test_content = "Hello, World!"
    test_file.write_text(test_content, encoding="utf-8")

    cat(str(test_file))

    output = capsys.readouterr()

    assert output.out == test_content + "\n"


def test_cat_notexisting_file():
    """Проверяем, что cat выбрасывает ошибку для несуществующего файла"""
    with pytest.raises(FileNotFoundError):
        cat("/notexisting_file.txt")


def test_cp_file(tmp_path):
    """Проверяем, что cp копирует файл"""
    source = tmp_path / "source.txt"
    source.write_text("Test content", encoding="utf-8")

    destination = tmp_path / "destination.txt"
    cp(str(source), str(destination))
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Test content"


def test_cp_notexisting_file():
    """Проверяем, что cp выбрасывает ошибку при копировании несуществующего файла"""
    with pytest.raises(PathDoesNotExist):
        cp("/nonexistent_source.txt", "/destination.txt")


def test_mv_file(tmp_path):
    """Проверяем, что mv перемещает файл"""
    source = tmp_path / "source.txt"
    source.write_text("Moving file", encoding="utf-8")

    destination = tmp_path / "destination.txt"
    mv(str(source), str(destination))

    assert not source.exists()
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Moving file"


def test_mv_notexisting_file():
    """Проверяем, что mv выбрасывает ошибку для несуществующего файла"""
    with pytest.raises(PathDoesNotExist):
        mv("/notexisting.txt", "/destination.txt")


def test_rm_file(tmp_path):

    test_file = tmp_path / "to_delete.txt"
    test_file.write_text("Delete", encoding="utf-8")

    rm(str(test_file))

    assert not test_file.exists()

    trash_dir = tmp_path / ".trash"
    assert trash_dir.exists()
    trash_files = list(trash_dir.iterdir())
    assert len(trash_files) > 0
    assert len(trash_files) == 1


def test_rm_directory_without_recursive(tmp_path):
    """Проверяем, что rm выбрасывает ошибку при попытке удалить папку без -r"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    with pytest.raises(NotRecursive):
        rm(str(test_dir))


def test_ls_existing_directory(tmp_path, capsys):
    """Проверяем, что ls показывает файлы в директории"""
    (tmp_path / "file1.txt").write_text("content1", encoding="utf-8")
    (tmp_path / "file2.txt").write_text("content2", encoding="utf-8")

    ls(str(tmp_path))

    output = capsys.readouterr()

    assert "file1.txt" in output.out
    assert "file2.txt" in output.out


def test_ls_notexisting_path():
    """Проверяем, что ls выбрасывает ошибку для несуществующего пути"""
    with pytest.raises(PathDoesNotExist):
        ls("/nonexistent/path/12345")


def test_grep_find_pattern(tmp_path, capsys):
    """Проверяем, что grep находит текст в файле"""
    test_file = tmp_path / "test.txt"
    test_file.write_text(
        "Hello World\nPython\nHello again", encoding="utf-8")

    grep("Hello", str(test_file))

    captured = capsys.readouterr()
    assert "Hello" in captured.out


def test_grep_no_matches(tmp_path, capsys):
    """Проверяем grep, когда совпадений нет"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Python", encoding="utf-8")

    grep("Java", str(test_file))

    captured = capsys.readouterr()

    assert "Python is awesome" not in captured.out

    assert captured.out.strip() == ""


def test_zip_create_archive(tmp_path):
    """Проверяем, что zip создает архив из директории"""
    test_dir = tmp_path / "my_folder"
    test_dir.mkdir()

    (test_dir / "file.txt").write_text("Text", encoding="utf-8")

    original_dir = os.getcwd()
    os.chdir(tmp_path)

    zip_archive(str(test_dir), "my_archive")

    os.chdir(original_dir)

    archive_path = tmp_path / "my_archive.zip"
    assert archive_path.exists()


def test_zip_notexisting_directory(tmp_path):
    """Проверяем, что zip выбрасывает ошибку для несуществующей папки"""
    with pytest.raises(PathDoesNotExist):
        zip_archive("notexisting_folder")


def test_unzip_extract_archive(tmp_path):
    """Проверяем, что unzip распаковывает архив"""
    test_dir = tmp_path / "folder_to_zip"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("Test content", encoding="utf-8")
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    zip_archive(str(test_dir), "test_archive")
    shutil.rmtree(test_dir)
    unzip_archive("test_archive.zip")

    os.chdir(original_dir)

    extracted_file = tmp_path / "folder_to_zip" / "file.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text(encoding="utf-8") == "Test content"


def test_unzip_notexisting_archive():
    """Проверяем, что unzip выбрасывает ошибку для несуществующего архива"""
    with pytest.raises(PathDoesNotExist):
        unzip_archive("notexisting.zip")


# ========== Тесты для tar (создание tar архива) ==========

def test_tar_create_archive(tmp_path):
    """Проверяем, что tar создает архив"""
    test_dir = tmp_path / "my_folder"
    test_dir.mkdir()
    (test_dir / "data.txt").write_text("Some data", encoding="utf-8")

    original_dir = os.getcwd()
    os.chdir(tmp_path)

    tar_archive(str(test_dir), "my_tar")

    os.chdir(original_dir)

    tar_file = tmp_path / "my_tar.tar"
    assert tar_file.exists()


def test_tar_notexisting_directory():
    """Проверяем, что tar выбрасывает ошибку для несуществующей папки"""

    with pytest.raises(PathDoesNotExist):
        tar_archive("notexisting_folder")


# ========== Тесты для untar (распаковка tar архива) ==========

def test_untar_extract_archive(tmp_path):
    """Проверяем, что untar распаковывает tar архив"""
    test_dir = tmp_path / "folder_to_tar"
    test_dir.mkdir()
    (test_dir / "info.txt").write_text("Important info", encoding="utf-8")
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    tar_archive(str(test_dir), "test_tar")
    import shutil
    shutil.rmtree(test_dir)
    untar_archive("test_tar.tar")
    os.chdir(original_dir)
    extracted_file = tmp_path / "folder_to_tar" / "info.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text(encoding="utf-8") == "Important info"


def test_untar_notexisting_archive():
    """Проверяем, что untar выбрасывает ошибку для несуществующего архива"""
    with pytest.raises(PathDoesNotExist):
        untar_archive("notexisting.tar")
