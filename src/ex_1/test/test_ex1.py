import pytest
import main

@pytest.mark.parametrize(
    "file_pattern, path, result",
    [
        (
            "*.log",
            "./test_folder",
            ["./test_folder/aaa.log", "./test_folder/a/bbb.log"],
        ),
        ("aaa", "./test_folder", []),
        ("a*", "./test_folder", ["./test_folder/aaa.log", "./test_folder/abc.txt"]),
        (
            "*b*",
            "./test_folder",
            ["./test_folder/abc.txt", "./test_folder/a/bbb", "./test_folder/a/bbb.log"],
        ),
        ("*aaa*", "./test_folder", ['./test_folder/aaa.log']),
    ],
)
def test_find_files_pattern(file_pattern: str, path: str, result: list):
    assert set(main.find_files(file_pattern, path)) == set(result)

@pytest.mark.parametrize(
    "file_pattern, path, result",
    [
        (
            "*.log",
            "./test_folder",
            ["./test_folder/aaa.log", "./test_folder/a/bbb.log"],
        ),
        ("aaa", "./test_folder", []),
        ("a*", "./test_folder", ["./test_folder/aaa.log", "./test_folder/abc.txt"]),
        (
            "*b*",
            "./test_folder",
            ["./test_folder/abc.txt", "./test_folder/a/bbb", "./test_folder/a/bbb.log"],
        ),
        ("*aaa*", "./test_folder", ['./test_folder/aaa.log']),
    ],
)
def test_find_files_pattern_recursive(file_pattern: str, path: str, result: list):
    assert set(main.find_files_recursive(file_pattern, path)) == set(result)
