import os
import sys

print(os.path.dirname(os.path.abspath(__file__)))


class Config(object):

    """
    Stores the application's basic settings and user preferences.
    """

    def __init__(self, path_letters=None, path_save=None, greeting=None,
                 copy=False, debug=False):
        # designated path to the directory containing the cover letter .txt's
        self.path_letters = self.default_path(path_letters)
        self.path_save = self.default_path(path_save)

        if not greeting:
            self.greeting = "To Whom It May Concern"
        else:
            self.greeting = greeting

        self.copy = copy
        self.debug = debug

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
        # TODO: Fix and comment me!
        for key in indict:
            if hasattr(self, key):
                self.key = indict[key]
            elif self.debug:
                debugout.write("[DEBUG]", __name__, "cannot load invalid key:",
                               key, "(value:", indict[key], ")")

    def save_json(self):
        pass


def config_setup(path=None):
    pass
