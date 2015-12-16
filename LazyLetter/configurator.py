import os
import sys
import json

print(os.path.dirname(os.path.abspath(__file__)))


class Config(object):

    """
    Stores the application's basic settings and user preferences.
    """

    def __init__(self, path_letters='coverletters', path_save='config',
                 greeting=None, copy=False, debug=False):
        # designated path to the directory containing the cover letter .txt's
        self.path_letters = self.default_path(path_letters)
        self.path_save = self.default_path(path_save)

        if not greeting:
            self.greeting = "To Whom It May Concern"
        else:
            self.greeting = greeting

        if not debug:
            self.debug = False
        else:
            self.debug = debug

        self.copy = copy

    def default_path(self, path):
        """
        Constructs a path relative to the parent of this file based on 2
        default preferences, None or string, or a path input
        """
        result = None

        if type(path) == str or not path:
            result = os.path.dirname(os.path.abspath(__file__))
            result = os.path.dirname(result)
            if type(path) == str:
                result = os.path.join(result, path)

        return result

    def load_dict(self, indict, debugout=sys.stdout):
        """
        Loads configuration settings from a dictionary object
        """
        for key in indict:
            if hasattr(self, key):
                self.__dict__[key] = indict[key]
            elif self.debug:
                print("[DEBUG] "+__name__ +
                      " cannot load invalid key: "+key +
                      "[value: "+indict[key]+"]"
                      )

    def save(self, filename="LazyLetter.cfg"):
        # check to see if the directories exist
        # if not, make them
        if not os.path.exists(self.path_save):
            os.makedirs(self.path_save)

        filepath = os.path.join(self.path_save, filename)
        temppath = filepath + ".temp"

        # 'filename'.temp is used in the event a write error occurs
        # if the .temp file already exists, it gets discarded
        if os.path.exists(temppath):
            os.remove(temppath)

        f = open(temppath, 'w')
        f.write(json.dumps(self.__dict__))
        f.close()

        if os.path.exists(filepath):
            os.remove(filepath)

        os.rename(temppath, filepath)

    def load(self, filename="LazyLetter.cfg"):
        filepath = os.path.join(self.path_save, filename)

        f = open(filepath, 'r')
        self.load_dict(json.loads(f.read()))
        f.close()


def config_setup(path=None):
    pass
