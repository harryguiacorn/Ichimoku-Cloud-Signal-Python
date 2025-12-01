from genericpath import isdir
import os
import logging

logger = logging.getLogger(__name__)


def split_filepath(filepath):
    filepath_without_filename, filename_with_extension = os.path.split(
        filepath
    )
    return filepath_without_filename, filename_with_extension


def file_exists(filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        return True
    else:
        logger.warning("%s does not exist.", filename)
        return False


def create_folder(__name="data", __printError: bool = True):
    # create data folder
    try:
        if isdir(__name) is False:
            os.makedirs(__name)
    except FileExistsError as __errFile:
        if __printError:
            logger.warning("Folder exists: %s", __errFile)


# def save_file_to_folder(__path="/path", __filename="data.csv"):
#     create_folder(__path, False)
#     output_file_path = os.path.join(__path, __filename)
