import os


def delete_file(path, filename=None):
    if filename:
        path = os.path.join(path, filename)

    if os.path.exists(path):
        os.remove(path)

        return True
    else:
        return False
