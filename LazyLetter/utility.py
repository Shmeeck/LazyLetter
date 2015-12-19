import os


def filename_join(path, filename=None):
    if filename:
        return os.path.join(path, filename)
    else:
        return path


def delete_file(path, filename=None):
    filepath = filename_join(path, filename)

    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)

        return True
    else:
        return False
