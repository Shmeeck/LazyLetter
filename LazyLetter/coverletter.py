import os

from . import utility
from .configurator import get_config


def get_list():
    """
    Retrieves a list of cover letters from the selected path located within a
    configurator.Config() object. Cover letter file extensions must match the
    extension specified within the get_config().file_type_letters attribute.
    """
    cover_letters = []
    path_letters = get_config().path_letters
    directory_list = os.listdir(path_letters)
    file_type = get_config().file_type_letters

    # remove all directories in the list
    for item in directory_list:
        if os.path.isfile(os.path.join(path_letters, item)):
            if file_type in item[len(item)-len(file_type):]:
                cover_letters.append(item)

    return cover_letters


def get(letter_name):
    """
    Returns a string object containing the contents of one cover letter txt
    file, returns "" and a debug report (if enabled in get_config()) on fail.
    """
    filepath = os.path.join(get_config().path_letters, letter_name)

    try:
        with open(filepath, 'r') as f:
            result = f.read()
            f.close()
            return result
    except FileNotFoundError as message:
        get_config().write_debug(get.__name__, "Attempted to load " +
                                 letter_name+': '+str(message))
        return ""


def delete(letter_name):
    """
    Removes a cover letter file within the path_letters path specified within a
    configurator.Config object.

    Returns True on success, otherwise False.
    """
    return utility.delete_file(get_config().path_letters, letter_name)
