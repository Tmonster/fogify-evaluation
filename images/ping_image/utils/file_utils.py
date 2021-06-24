

def file_exists(file):
    try:
        f = open(file, "r")
        f.close()
        return True
    except FileNotFoundError as e:
        return False