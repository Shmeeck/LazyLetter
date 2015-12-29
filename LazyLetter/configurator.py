import os
import json
import datetime


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

    _path_config = default_path('config')
    _name_config = 'LazyLetter.cfg'

    continue_msg = 'Press ENTER to continue...'

    def __init__(self,
                 path_letters='cover letters', file_type_letters='.txt',
                 greeting="To Whom It May Concern", copy=None,
                 debug=False, debuglog=None,
                 ):
        # designated path to the directory containing the cover letter .txt's
        self.path_letters = default_path(path_letters)

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
        """
        Dumps all attributes in dictionary form to a json text file named
        with the _name_config string.
        """
        # check to see if the directories exist
        if not os.path.exists(self._path_config):
            os.makedirs(self._path_config)

        filepath = os.path.join(self._path_config, self._name_config)
        temppath = filepath + ".temp"

        # self._name_config.temp is used in the event a write
        # error occurs
        if os.path.exists(temppath):
            os.remove(temppath)

        f = open(temppath, 'w')
        f.write(json.dumps(self.__dict__))
        f.close()

        if os.path.exists(filepath):
            if force:
                os.remove(filepath)

        os.rename(temppath, filepath)

    def _load_dict(self, indict):
        """
        Loads configuration settings from a dictionary object.
        """
        for key in indict:
            if hasattr(self, key):
                setattr(self, key, indict[key])
            else:
                self.write_debug(self._load_dict.__name__,
                                 "Cannot load invalid key: "+key+" (value: " +
                                 str(indict[key])+")")

    @classmethod
    def load(cls):
        """
        Loads a json text file into the attributes of the instance, returns T/F
        depending on file existence.
        """
        result = cls()
        filepath = os.path.join(result._path_config, result._name_config)

        f = open(filepath, 'r')
        result._load_dict(json.loads(f.read()))
        f.close()

        return result

main_config = Config()


def get_config():
    return main_config


def set_config(config):
    global main_config
    main_config = config
