from genericpath import isdir
import os


def file_exists(filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        return True
    else:
        print(f"WARNING: {filename} does not exist.")
        return False


def create_folder(__name="data", __printError: bool = True):
    # create data folder
    try:
        if isdir(__name) is False:
            os.makedirs(__name)
    except FileExistsError as __errFile:
        if __printError:
            print("WARNING: folder exists", __errFile)


# def save_file_to_folder(__path="/path", __filename="data.csv"):
#     create_folder(__path, False)
#     output_file_path = os.path.join(__path, __filename)
