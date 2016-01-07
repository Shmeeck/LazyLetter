import sys
import os

from . import utility
from . import answer
from . import configurator
from tkinter import *
from tkinter import filedialog
from .configurator import get_config as config


class WonderousMap(object):

    """
    Manages all meta-data and details regarding which key leads to which Menu
    or MenuFunction object.
    """

    def __init__(self, details=None):
        if details:
            self.load(details)

    def load(self, details):
        self.themap = {}
        self.keys = [None] * len(details)

        for i, dest in enumerate(details):
            self.keys[i] = dest.name
            self.themap[dest.name] = details[i]

    def get(self, key, on_fail=None):
        return self.themap.get(key, on_fail)


class Menu(object):

    """
    The base object that acts as a node for the user to navigate between
    application features. local_map can be specified to transfer the user
    between individual methods by mapping the option string to the method
    itself.
    """

    origin = ''
    welcome = "This is a welcome message of a base Menu object:"
    name = 'Base Menu'
    local_map = WonderousMap()
    option_back = ["Go Back"]

    def __init__(self):
        self.update_welcome()

    def enter(self):
        while True:
            utility.clear_screen()
            self.update_welcome()
            result = answer.down_to_one(self.local_map.keys+self.option_back,
                                        self.welcome)

            if [result] == self.option_back:
                return self.origin

            result = navigate(self.local_map, result, self.name)

            if result == self.name:
                continue
            else:
                return result

    def update_welcome(self):
        pass


class MenuFunction(Menu):

    """
    A base object for performing a specific action within a Menu object.
    """

    welcome = "This is a welcome message of a base MenuFunction object:"
    name = 'Base Menu Function'
    options = []

    def enter(self):
        result = answer.down_to_one(self.options, self.welcome)
        return self.do_action(result)

    def do_action(self, answer):
        print("Base MenuFuncton did nothing on " + answer)

        return self.origin


class MenuToggleConfigBoolean(MenuFunction):

    name = 'Base boolen toggle MenuFunction'
    options = ['Yes', 'No']
    option_back = []
    item_attr = None

    def do_action(self, answer):
        if answer == 'Yes' and config() is not None:
            toggle = not getattr(config(), self.item_attr)
            setattr(config(), self.item_attr, toggle)

            if hasattr(config(), 'save'):
                config().save()

        return self.origin

    def update_welcome(self):
        if self.item_attr:
            self.welcome = "Set " + self.name.lower() + " to " + \
                str(not getattr(config(), self.item_attr)) + '?'


# ============================================================================
# --------------------------------- Settings ---------------------------------

class ToggleCopy(MenuToggleConfigBoolean):

    name = 'Copy to Clipboard by Default'
    options = ['Yes', 'No']
    item_attr = 'copy'


class ToggleDebug(MenuToggleConfigBoolean):

    name = 'Debug Mode'
    options = ['Yes', 'No']
    item_attr = 'debug'

    def do_action(self, answer):
        debuglog = None

        if answer == 'Yes' and not getattr(config(),
                                           self.item_attr+'log'):
            debuglog = self.item_attr+'.log'

        setattr(config(), self.item_attr+'log', debuglog)
        super().do_action(answer)

        return self.origin


class CoverLetterDir(MenuFunction):

    name = 'Cover Letter Directory'
    welcome = "Please select a directory where your cover letters & " + \
        "templates are, if the current path is not the default, then " + \
        "exit the window to be prompted to set back to default..."
    options = ['Yes', 'No']
    option_back = []

    def enter(self):
        default_path = configurator.Config().path_letters

        utility.clear_screen()
        print(self.welcome)
        result = self.do_action()

        if not result and config().path_letters != default_path:
            old_welcome = self.welcome

            self.welcome = "Current path: " + config().path_letters + "\n" + \
                "Default path: " + default_path + "\n\n" + \
                "No selection was made, reset back to default?"

            if self.get_answer(self.options) == 'Yes':
                config().path_letters = default_path
                config().save()

            self.welcome = old_welcome

        return self.origin

    def do_action(self):
        root = Tk()
        root.withdraw()

        path = filedialog.askdirectory()
        root.destroy()

        if path:
            path = os.path.abspath(path)
            config().path_letters = path
            config().save

        return path


class Settings(Menu):
    name = 'Settings'
    local_map = WonderousMap([ToggleDebug(),
                              ToggleCopy(),
                              CoverLetterDir(),
                              ])

    def get_current_settings(self):
        result = 'Cover Letter Directory: ' + str(config().path_letters) + \
                 '\n' + 'Copy to Clipboard by Default: ' + \
                 str(config().copy) + '\n' + 'Debug Mode: ' + \
                 str(config().debug) + '\n\n'

        return result

    def update_welcome(self):
        self.welcome = self.get_current_settings() + \
            str("Select which setting you would like to modify:")


class Exit(Menu):
    name = 'Exit'

    def enter(self):
        sys.exit(0)


class MainMenu(Menu):
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )
    name = 'Main Menu'
    option_back = []

    def __init__(self):
        self.local_map = WonderousMap([Settings(),
                                       Exit(),
                                       ])


def navigate(wonderous_map, start, origin):
    """
    Accepts a dictionary which maps strings to Menu or MenuFunction objects
    and one string that equals a dictionary key. The string goes through the
    dictionary of objects and enter() gets called on the result. Within each
    Menu object is a local_map and calls this same function for that map as
    well.

    Loops until a Menu/MenuFunction returns a non-matching key for the active
    map and sends said key up to the previous active map or exits the function
    if we're already at the world_map.
    """
    destination = wonderous_map.get(start)
    heading = start

    if destination:
        destination.origin = origin

    while True:
        if not destination:
            break

        heading = destination.enter()

        destination = wonderous_map.get(heading)

        if destination:
            destination.origin = origin
            origin = heading

    return heading


def hub_navigation():
    """
    This function initiates the entire shabangbang!
    """
    MainMenu().enter()
