import pathlib

def file_exists(file):
    try:
        f = open(file, "r")
        f.close()
        return True
    except FileNotFoundError as e:
        return False


def make_dir(dir_name):
    try:
        pathlib.Path(f"./{dir_name}").mkdir()
    except FileExistsError as e:
        # ignore that test_results already exists
        print(f"could not make directory {dir_name}. Might already exist")
