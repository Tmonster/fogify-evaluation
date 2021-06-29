import pathlib


def make_dir(results_dir):
    try:
        pathlib.Path(f"./{results_dir}").mkdir()
    except FileExistsError as e:
        # ignore that test_results already exists
        print(f"could not make directory {results_dir}. Exiting")


def file_exists(file):
    try:
        f = open(file, "r")
        f.close()
        return True
    except FileNotFoundError as e:
        return False