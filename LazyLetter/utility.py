import os
import sys


def filename_join(path, filename=None):
    if filename:
        return os.path.join(path, filename)
    else:
        return path


def delete_file(path, filename=None):
    if type(filename) == list:
        result = False

        for single_name in filename:
            filepath = filename_join(path, single_name)

            if os.path.exists(filepath) and os.path.isfile(filepath):
                os.remove(filepath)

                result = True

        return result
    else:
        filepath = filename_join(path, filename)

        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)

            return True
        else:
            return False


def clear_screen():
    try:
        clear = os.system('cls')
    except clear == 1:
        clear = os.system('clear')


def timedelta_string(delta):
    minutes, remainder = divmod(abs(delta.seconds), 60)
    seconds = remainder
    milliseconds = abs(delta.microseconds) // 10**3

    return str(minutes), str(seconds), str(milliseconds)
