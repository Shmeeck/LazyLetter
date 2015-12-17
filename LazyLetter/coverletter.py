import os

from . import utility


def get_list(config):
    """
    Retrieves a list of cover letters from the selected path located within a
    configurator.Config() object.
    """
    cover_letters = []
    path_letters = config.path_letters
    directory_list = os.listdir(path_letters)

    # remove all directories in the list
    for item in directory_list:
        if os.path.isfile(os.path.join(path_letters, item)) and \
           '.txt' in item:

            cover_letters.append(item)

    return cover_letters


def get(config, letter_name):
    """
    Returns a string object containing the contents of one cover letter txt
    file, returns "" and a debug report (if enabled in config) on fail.
    """
    filepath = os.path.join(config.path_letters, letter_name)

    try:
        with open(filepath, 'r') as f:
            result = f.read()
            f.close()
            return result
    except FileNotFoundError as message:
        if config.debug:
            print('[DEBUG] Attempted to load',
                  letter_name + ':', message,
                  )
        else:
            print(letter_name, 'does not exist.')

        return ""


def delete(config, letter_name):
    """
    Removes a cover letter file within the path_letters path specified within a
    configurator.Config() object.

    Returns True on success, otherwise False.
    """
    return utility.delete_file(config.path_letters, letter_name)
