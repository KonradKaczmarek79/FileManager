import os

# run the user's program in our generated folders
os.chdir('module/root_folder')

possible_options = {"pwd", "cd"}
relative_options = {".", ".."}

# put your code here
command = input("Input the command\n")

while command != "quit":

    option = "."

    if " " in command:
        # find a first space and split command (before space) and option (after soace)
        command, option = command[:command.index(" ")], command[command.index(" ") + 1:]

    if command not in possible_options:
        print("Invalid command")

    elif command == "pwd":
        print(os.getcwd())
    elif command == "cd":
        try:
            os.chdir(option)
            print(os.getcwd().replace("\\", "/").split("/")[-1])
        except FileNotFoundError:
            print("Invalid command")

    command = input()