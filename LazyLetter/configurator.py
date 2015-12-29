import os
import sys
import json
import datetime

from . import filewalker


def _load_dict(obj, indict):
    """
    Loads configuration settings from a dictionary object.
    """
    for key in indict:
        if hasattr(obj, key):
            setattr(obj, key, indict[key])
        else:
            # FIX THIS
            obj.write_debug(_load_dict.__name__,
                            "Cannot load invalid key: "+key+" (value: " +
                            str(indict[key])+")")


def save(obj, filepath, filename, force):
    """
    Dumps all attributes in dictionary form to a json text file named
    with the current_config string.
    """
    # check to see if the directories exist
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    filepath = os.path.join(filepath, filename)
    temppath = filepath + ".temp"

    # filename.temp is used in the event a write
    # error occurs
    if os.path.exists(temppath):
        os.remove(temppath)

    f = open(temppath, 'w')
    f.write(json.dumps(obj.__dict__))
    f.close()

    if os.path.exists(filepath):
        if force:
            os.remove(filepath)
        else:
            return False

    os.rename(temppath, filepath)

    return True


def load(obj, filepath, filename):
    """
    Loads a json text file into the attributes of the instance, returns T/F
    depending on file existence.
    """
    filepath = os.path.join(filepath, filename)

    try:
        f = open(filepath, 'r')
        _load_dict(obj, json.loads(f.read()))
        f.close()

        return True
    except FileNotFoundError as message:
        # FIX THIS
        obj.write_debug(load.__name__, "Attempted to load " +
                        filename+": "+str(message))
        return False


def default_path(path=None):
        """
        Constructs a path relative to the parent of this file based on 2
        default preferences, None or string, or a path input.
        """
        result = None

        if type(path) == str or not path:
            result = os.path.dirname(os.path.abspath(__file__))
            result = os.path.dirname(result)
            if type(path) == str:
                result = os.path.join(result, path)

        return result


class Config(object):

    """
    Stores the application's basic settings and user preferences.
    """

    def __init__(self,
                 path_letters='cover letters', file_type_letters='.txt',
                 path_configs='config', current_config='default.cfg',
                 greeting="To Whom It May Concern", copy=False,
                 debug=False, debuglog=None,
                 ):
        # designated path to the directory containing the cover letter .txt's
        self.path_letters = default_path(path_letters)
        self.path_configs = default_path(path_configs)

        self.current_config = current_config
        self.greeting = greeting
        self.debug = debug
        self.debuglog = debuglog
        self.copy = copy
        self.file_type_letters = file_type_letters

    def write_debug(self, function_name, message):
        result = "[DEBUG] " + function_name + ': ' + message
        if self.debug:
            print(result)
        if self.debuglog:
            filepath = os.path.join(default_path(), self.debuglog)
            with open(filepath, 'a') as f:
                f.write('['+str(datetime.datetime.now())+'] ' + result)
                f.close()

        return result

    def save(self, force=True):
        return save(self, self.path_configs, self.current_config, force)

    def load(self):
        return load(self, self.path_configs, self.current_config)

    def remove_save(self):
        """
        Removes the associated .cfg save for the current config.

        Returns True on success, otherwise False.
        """
        return filewalker.delete(self.path_configs, self.current_config)

    def rename_current_config(self, new_filename, force=True):
        """
        Renames the current config's .cfg file to the given filename, switches
        the current_config to the argument new_filename.

        Returns back the passed argument on success, otherwise returns the
        filename that existed prior to this function call.
        """
        old_filename = self.current_config

        self.remove_save()
        self.current_config = new_filename

        if self.save(force):
            return new_filename
        else:
            return old_filename

    def change_config(self, new_filename):
        """
        Switches the current config's .cfg file to the given filename, does
        NOT save the previous config before opening the new one.

        Returns back the passed argument or, if loading fails, the
        same current_config that existed before this function call.
        """
        old_filename = self.current_config
        self.current_config = new_filename

        if self.load():
            return new_filename
        else:
            return old_filename


class MetaSaver(object):

    """docstring for ConfigSaver"""

    def __init__(self,
                 path_save=None, path_configs='config',
                 current_save='LazyLatter.save',
                 current_config='default.cfg'
                 ):
        self.path_save = default_path(path_save)
        self.path_configs = default_path(path_configs)
        self.current_save = current_save
        self.current_config = current_config

    def save(self, force=True):
        return save(self, self.path_save, self.current_save)

    def load(self):
        return load(self, self.path_save, self.current_save)



main_config = Config()
saved_meta = MetaSaver()


def get_config():
    if not main_config:
        print("Error: Config not loaded, was LazyLetter.py modified somehow?")
        sys.exit(0)

    return main_config


def set_config(config):
    global main_config
    main_config = config
