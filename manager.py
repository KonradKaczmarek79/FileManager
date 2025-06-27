import os
import shutil
from typing import Callable
import re

# run the user's program in our generated folders
os.chdir('module/root_folder')

possible_commands = {"pwd", "cd", "ls", "mkdir", "rm", "mv", "cp"}
relative_options = {".", ".."}

# put your code here
command = input("Input the command\n")

def change_dir(cd_option: str):
    try:
        os.chdir(cd_option)
        return os.getcwd().replace("\\", "/").split("/")[-1]
    except FileNotFoundError:
        return "Invalid command"


def convert_human_readable(value: int) -> str:
    if value < 1024:
        return f"{value}B"
    elif value < 1024**2:
        return f"{value // 1024}KB"
    elif value < 1024**3:
        return f"{value // 1024}MB"
    else:
        return f"{value // 1024}GB"


def get_info_with_filesize(human_readable_size: bool | None = False):
    subdirectories = ""
    files = ""

    for element in os.listdir():
        if os.path.isdir(element):
            subdirectories += f"{element}\n"
        elif os.path.isfile(element) and human_readable_size is not None:
            # it can be handled using os.path.getsize
            # files += f"{element} {convert_human_readable(os.path.getsize(element)) if human_readable_size else os.path.getsize(element)}\n"
            # or using os.stat(element).st_size
            files += f"{element} {convert_human_readable(os.stat(element).st_size) if human_readable_size else os.stat(element).st_size}\n"
        else:
            files += f"{element}\n"

    return f"{subdirectories}{files}".strip()


def list_content(ls_option: str):
    if ls_option == "":
        return get_info_with_filesize(human_readable_size=None)
    elif ls_option == "-l":
        return get_info_with_filesize()
    elif ls_option == "-lh":
        return get_info_with_filesize(human_readable_size=True)
    else:
        return "Invalid command"


def make_directory(directory_path: str) -> None | str:
    """
    Creates a mew directory in a specified folder

    :param directory_path: a path to a new directory absolute or relative
    :return: Error message (if directory_path not specified or if directory exists) or None (in the case of success)
    """
    if not directory_path:
        return "Specify the name of the directory to be made"

    try:
        os.mkdir(directory_path)
    except FileExistsError:
        return "The directory already exists"


def remove_directory(directory_path: str) -> None | str:
    """
    Removes a specified directory

    :param directory_path: a path to a directory you want to remove
    :return: Error message (if directory_path not specified or if directory not exists) or None
    """

    try:
        shutil.rmtree(directory_path)
    except FileNotFoundError:
        return "No such file or directory"


def remove_file(file_path: str) -> None | str:
    """
    Removes a specified file

    :param file_path: a path to a file you want to remove
    :return: Error message (if file_path not specified or if file not exists) or None
    """

    try:
        os.remove(file_path)
    except FileNotFoundError:
        return "No such file or directory"


def remove_files_per_extension(extension: str) -> None | str:
    """
    Removes files with the specified extension

    :param extension: (str) extension in format .abc
    :return: None or error message (if extension not found in current directory)
    """
    # filter returns an iterator so it is
    files_to_delete = list(filter(lambda filename: filename.endswith(extension), os.listdir()))

    if not files_to_delete:
        return f"File extension {extension} not found in this directory"
    else:
        for file in files_to_delete:
            remove_file(file)
        return None


def remove_item(item_path: str) -> None | str:
    if not item_path:
        return "Specify the file or directory"

    result = "No such file or directory"
    if re.match(r"^[.][a-zA-Z]+$", item_path):
        result = remove_files_per_extension(extension=item_path)
    elif os.path.isfile(item_path):
        result = remove_file(item_path)
    elif os.path.isdir(item_path):
        result = remove_directory(item_path)
    return result


def move_content(path_source: str, path_target: str) -> None | str:
    """
    Moves the file content or directory content to specified path (second word in passed string)

    :param path_source:
    :param path_target:
    :param paths: (str) it should contain two words 1. source data path and target path
    :return: string in the case of error of if a target item already exists None otherwise
    """
    # paths = paths.split(" ")
    # if len(paths) != 2:
    #     return "Specify the current name of the file or directory and the new location and/or name"

    if os.path.exists(path_target):
        # if os.path.isdir(old_name) and os.path.isdir(new_name): -> print("The file or directory already exists")
        # otherwise try to create move and create file with name from paths[1]
        if os.path.isfile(path_source) and os.path.isdir(path_target):
            shutil.move(path_source, path_target)
            return None
        return "The file or directory already exists"

    try:
        shutil.move(path_source, path_target)
    except FileNotFoundError:
        return "No such file or directory"

def move_with_overwrite_confirmation(source, target):
    file_path = os.path.join(target, source)

    if os.path.exists(file_path):
        answer = input(f"{source} already exists in this directory. Replace? (y/n)\n")
        while answer not in {"y", "n"}:
            answer = input(f"{source} already exists in this directory. Replace? (y/n)\n")
        if answer.lower() == "n":
            return None
        elif answer.lower() == "y":
            os.remove(file_path)
    if os.path.isdir(target):
        shutil.move(source, target)
    return None

def move_one_or_many(paths: str) -> None | str:
    paths = paths.split(" ")
    if len(paths) != 2:
        return "Specify the current name of the file or directory and the new location and/or name"

    if re.match(r"^[.][a-zA-Z]+$", paths[0]):
        files_to_move = list(filter(lambda filename: filename.endswith(paths[0]), os.listdir()))
        if not files_to_move:
            return f"File extension {paths[0]} not found in this directory"
        for file in files_to_move:
            move_with_overwrite_confirmation(file, paths[1])
    else:
        return move_content(paths[0], paths[1])


def run_fn_and_check_result(fn: Callable, fn_option: str) -> None:
    """
    Runs a function and checks its result. Helper function
    :param fn: a function to run
    :param fn_option: a parameter to pass into the function
    :return: None. In the case when function returns string it is printed
    """
    result = fn(fn_option)
    if result is not None:
        print(result)


def copy_file(paths: str) -> None | str:
    """
    Copies a specified file to the specified directory

    :param paths: (str) it should contain two words 1. source (file) path and target (directory) path
    :return: None or string in the case of error (no file specified, no directory specified,
    more than 2 elements in paths string, or if the file already exists in target directory).
    """
    paths = paths.split(" ")

    if len(paths) < 2:
        return "Specify the file"
    elif len(paths) > 2:
        return "Specify the current name of the file or directory and the new location and/or name"

    if os.path.isfile(paths[0]) and os.path.isdir(paths[1]):

        if os.path.exists(os.path.join(paths[1], paths[0])):
            return f"{paths[0]} already exists in this directory"
        shutil.copy(paths[0], paths[1])
        return None
    else:
        return "No such file or directory"

def copy_file_v2(source_path: str, target_path: str) -> None | str:
    """
    Copies a specified file to the specified directory

    :param target_path: (str) source file to copy
    :param source_path: (str) target folder to copy
    :return: None or string in the case when the file already exists in target directory or when file or dir not exists.
    """

    if os.path.isfile(source_path) and os.path.isdir(target_path):

        if os.path.exists(os.path.join(target_path, source_path)):
            return f"{source_path} already exists in this directory"
        shutil.copy(source_path, target_path)
        return None
    else:
        return "No such file or directory"

def copy_with_overwrite_confirmation(source, target):
    file_path = os.path.join(target, source)

    if os.path.exists(file_path):
        answer = input(f"{source} already exists in this directory. Replace? (y/n)\n")
        while answer not in {"y", "n"}:
            answer = input(f"{source} already exists in this directory. Replace? (y/n)\n")
        if answer.lower() == "n":
            return None
    shutil.copy(source, target)
    return None


def copy_files(paths: str) -> None | str:
    paths = paths.split(" ")

    if len(paths) < 2:
        return "Specify the file"
    elif len(paths) > 2:
        return "Specify the current name of the file or directory and the new location and/or name"

    if re.match(r"^[.][a-zA-Z]+$", paths[0]):
        files_to_copy = list(filter(lambda filename: filename.endswith(paths[0]), os.listdir()))
        if len(files_to_copy) == 0:
            return f"File extension {paths[0]} not found in this directory"
        else:
            for file in files_to_copy:
                # shutil.copy(file, paths[1])
                copy_with_overwrite_confirmation(file, paths[1])
        return None
    else:
        return copy_file_v2(paths[0], paths[1])


while command != "quit":

    option = ""

    if " " in command:
        # find a first space and split command (before space) and option (after space)
        command, option = command[:command.index(" ")], command[command.index(" ") + 1:]

    if command not in possible_commands:
        print("Invalid command")

    elif command == "pwd":
        print(os.getcwd())
    elif command == "cd":
        print(change_dir(option))
    elif command == "ls":
        print(list_content(option))
    elif command == "mkdir":
        run_fn_and_check_result(make_directory, option)
    elif command == "rm":
        run_fn_and_check_result(remove_item, option)
    elif command == "mv":
        run_fn_and_check_result(move_one_or_many, option)
    elif command == "cp":
        run_fn_and_check_result(copy_files, option)

    command = input()
