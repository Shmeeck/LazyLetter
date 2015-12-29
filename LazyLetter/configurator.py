import os
import json
import datetime

from . import filewalker


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
        self.path_letters = self.default_path(path_letters)
        self.path_configs = self.default_path(path_configs)

        self.current_config = current_config
        self.greeting = greeting
        self.debug = debug
        self.debuglog = debuglog
        self.copy = copy
        self.file_type_letters = file_type_letters

    def default_path(self, path=None):
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

    def write_debug(self, function_name, message):
        result = "[DEBUG] " + function_name + ': ' + message
        if self.debug:
            print(result)
        if self.debuglog:
            filepath = os.path.join(self.default_path(), self.debuglog)
            with open(filepath, 'a') as f:
                f.write('['+str(datetime.datetime.now())+'] ' + result)
                f.close()

        return result

    def load_dict(self, indict):
        """
        Loads configuration settings from a dictionary object.
        """
        for key in indict:
            if hasattr(self, key):
                self.__dict__[key] = indict[key]
            else:
                self.write_debug(self.load_dict.__name__,
                                 "Cannot load invalid key: "+key+" (value: " +
                                 indict[key]+")")

    def save(self, force=True):
        """
        Dumps all attributes in dictionary form to a json text file named
        with the current_config string.
        """
        # check to see if the directories exist
        if not os.path.exists(self.path_configs):
            os.makedirs(self.path_configs)

        filepath = os.path.join(self.path_configs, self.current_config)
        temppath = filepath + ".temp"

        # self.current_config.temp is used in the event a write
        # error occurs
        if os.path.exists(temppath):
            os.remove(temppath)

        f = open(temppath, 'w')
        f.write(json.dumps(self.__dict__))
        f.close()

        if os.path.exists(filepath):
            if force:
                os.remove(filepath)
            else:
                return False

        os.rename(temppath, filepath)

        return True

    def load(self):
        """
        Loads a json text file into the attributes of the instance, returns T/F
        depending on file existence.
        """
        filepath = os.path.join(self.path_configs, self.current_config)

        try:
            f = open(filepath, 'r')
            self.load_dict(json.loads(f.read()))
            f.close()

            return True
        except FileNotFoundError as message:
            self.write_debug(self.load.__name__, "Attempted to load " +
                             self.current_config+": "+str(message))
            return False

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


class ConfigSaver(Config):

    """docstring for ConfigSaver"""

    def __init__(self, path_configs=None, path_to_configs='config',
                 current_config='LazyLatter.save'):
        self.path_configs = self.default_path(path_configs)
        self.path_to_configs = self.default_path(path_to_configs)
        self.current_config = current_config


main_config = Config(debug=True)


def get_config():
    return main_config
