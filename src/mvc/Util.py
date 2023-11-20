from genericpath import isdir
import os


def file_exists(filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        return True
    else:
        print(f"WARNING: {filename} does not exist.")
        return False


def createDataFolder(__name="data"):
    # create data folder
    try:
        if isdir(__name) is False:
            os.makedirs(__name)
    except FileExistsError as __errFile:
        print("data folder exists", __errFile)
