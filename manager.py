import os
import shutil
from typing import Callable

# run the user's program in our generated folders
os.chdir('module/root_folder')

possible_commands = {"pwd", "cd", "ls", "mkdir", "rm", "mv"}
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


def remove_item(item_path: str) -> None | str:
    if not item_path:
        return "Specify the file or directory"

    result = "No such file or directory"

    if os.path.isfile(item_path):
        result = remove_file(item_path)
    elif os.path.isdir(item_path):
        result = remove_directory(item_path)
    return result


def move_content(paths: str) -> None | str:
    """
    Moves the file content or directory content to specified path (second word in passed string)

    :param paths: (str) it should contain two words 1. source data path and target path
    :return: string in the case of error of if a target item already exists None otherwise
    """
    paths = paths.split(" ")
    if len(paths) != 2:
        return "Specify the current name of the file or directory and the new name"

    if os.path.exists(paths[1]):
        return "The file or directory already exists"

    try:
        shutil.move(paths[0], paths[1])
    except FileNotFoundError:
        return "No such file or directory"


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
        run_fn_and_check_result(move_content, option)

    command = input()
