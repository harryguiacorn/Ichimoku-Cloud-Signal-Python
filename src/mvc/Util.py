import os


def file_exists(self, filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        return True
    else:
        print(f"WARNING: {filename} does not exist.")
        return False
