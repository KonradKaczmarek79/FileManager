import os

# run the user's program in our generated folders
os.chdir('module/root_folder')

possible_options = {"pwd", "cd", "ls"}
relative_options = {".", ".."}

# put your code here
command = input("Input the command\n")

def change_dir(cd_option: str):
    try:
        os.chdir(cd_option)
        print(os.getcwd().replace("\\", "/").split("/")[-1])
    except FileNotFoundError:
        print("Invalid command")

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
        print(get_info_with_filesize(human_readable_size=None))
    elif ls_option == "-l":
        print(get_info_with_filesize())
    elif ls_option == "-lh":
        print(get_info_with_filesize(human_readable_size=True))


while command != "quit":

    option = ""

    if " " in command:
        # find a first space and split command (before space) and option (after space)
        command, option = command[:command.index(" ")], command[command.index(" ") + 1:]

    if command not in possible_options:
        print("Invalid command")

    elif command == "pwd":
        print(os.getcwd())
    elif command == "cd":
        change_dir(option)
    elif command == "ls":
        list_content(option)

    command = input()
