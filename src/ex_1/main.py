import sys
import os
from fnmatch import fnmatch
from utils.logger import Logger

logger = Logger.get_logger(logger_name="ex_1")

def find_files(file_pattern: str, path: str):
    """
    Find files recursively in a directory
    """
    found_files = []
    logger.info(f"Base path: {path}")
    # print current directory
    for root, dirs, files in os.walk(path):
        logger.info(f"Root: {root}")
        logger.info(f"Dirs: {dirs}")
        logger.info(f"Files: {files}")
        for file in files:
            if fnmatch(file, file_pattern):
                found_files.append(os.path.join(root, file))
    return found_files

def find_files_recursive(file_pattern: str, path: str, **kwargs):
    found_files = kwargs.pop("found_files", [])
    logger.info(f"Base path: {path}")

    # List current directory
    curr_dir = os.listdir(path)
    logger.info(f"Current directory: {curr_dir}")
    for elem in curr_dir:
        # check if directory
        if os.path.isdir(os.path.join(path, elem)):
            logger.info(f"Found directory: {elem}")
            # recursively call function
            find_files_recursive(file_pattern, os.path.join(path, elem), found_files=found_files)
        elif fnmatch(elem, file_pattern):
            logger.info(f"Found file: {elem}")
            found_files.append(os.path.join(path, elem))
    return found_files


if __name__ == "__main__":
    # Read the path and file suffix from the command line
    file_suffix = sys.argv[1]
    path = sys.argv[2]
    # Call the function and print the result
    files = find_files_recursive(file_suffix, path)
    logger.info(f"Found files: {files}")
