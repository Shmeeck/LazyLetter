import os
import sys
import json

print(os.path.dirname(os.path.abspath(__file__)))


class Config(object):

    """
    Stores the application's basic settings and user preferences.
    """

    def __init__(self, path_letters='coverletters', path_save='config',
                 greeting=None, copy=False, debugout=None):
        # designated path to the directory containing the cover letter .txt's
        self.path_letters = self.default_path(path_letters)
        self.path_save = self.default_path(path_save)

        if not greeting:
            self.greeting = "To Whom It May Concern"
        else:
            self.greeting = greeting

        if not debugout:
            self.debugout = sys.stdout
        else:
            self.debugout = debugout

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

    def load_dict(self, indict):
        """
        Loads configuration settings from a dictionary object
        """
        for key in indict:
            if hasattr(self, key):
                self.__dict__[key] = indict[key]
            elif self.debugout:
                output = str("[DEBUG] "+__name__ +
                             " cannot load invalid key: "+key +
                             "[value: "+indict[key]+"]"
                             )

                self.debugout.write(output)

    def save(self, filename="LazyLetter.config"):
        fpath = os.path.join(self.save_path, filename)
        temppath = os.path.join(fpath, '.temp')

        f = open(temppath, 'w')
        f.write(json.dumps(self.__dict__))
        f.close()

        os.rename(temppath, fpath)

    def load(self, filename="LazyLetter.config"):
        fpath = os.path.join(self.save_path, filename)

        f = open(fpath, 'r')
        self.load_dict(json.loads(f.read()))
        f.close()


def config_setup(path=None):
    pass
