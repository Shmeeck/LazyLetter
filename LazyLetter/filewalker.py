import os


def join(path, filename=None):
    if filename:
        return os.path.join(path, filename)
    else:
        return path


def delete(path, filename):
    if type(filename) == list:
        result = False

        for single_name in filename:
            filepath = join(path, single_name)

            if os.path.exists(filepath) and os.path.isfile(filepath):
                os.remove(filepath)

                result = True

        return result
    else:
        filepath = join(path, filename)

        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)

            return True
        else:
            return False


def get_list(path, extension=None):
    """
    Retrieves a list of cover letters from the selected path located within a
    configurator.Config() object. Cover letter file extensions must match the
    extension specified within the get_config().file_type_letters attribute.
    """
    file_list = []
    directory_list = os.listdir(path)

    # remove all directories in the list
    for item in directory_list:
        if os.path.isfile(os.path.join(path, item)):
            if not extension:
                file_list.append(item)
            elif extension in item[len(item)-len(extension):]:
                file_list.append(item)

    return file_list
