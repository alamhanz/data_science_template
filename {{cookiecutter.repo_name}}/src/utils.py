import os


def get_folder_name(current_path=None):
    if current_path:
        curr_path = current_path
    else:
        curr_path = os.getcwd()

    if os.name == "posix":
        folder_name = os.getcwd().split("/")[-1]
    else:
        folder_name = os.getcwd().split("\\")[-1]

    return folder_name
