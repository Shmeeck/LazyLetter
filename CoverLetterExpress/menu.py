import sys
import os

from . import utility
from . import question
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

    msg_multiple = "Your answer matched more than one possible option:"
    msg_noresult = "Sorry, couldn't understand that..."
    option_redo = "None of These"
    option_back = "Back to {}"

    origin = ''
    welcome = "This is a welcome message of a base Menu object:"
    name = 'Base Menu'
    local_map = WonderousMap()

    def __init__(self):
        self.update_welcome()

    def enter(self):
        while True:
            result = self.get_answer(self.local_map.keys)
            result = navigate(self.local_map, result, self.name)

            if result == self.name:
                continue
            else:
                return result

    def get_answer(self, li):
        utility.clear_screen()
        go_back = ''

        if self.option_back:
            go_back = self.option_back.format(self.origin)
            li.append(go_back)

        self.update_welcome()
        result = question.handler(li, self.welcome,
                                  self.option_redo, self.msg_noresult,
                                  self.msg_multiple,
                                  )

        if self.option_back:
            li.pop()

            if result == go_back:
                return self.origin

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
        result = self.get_answer(self.options)
        return self.do_action(result)

    def do_action(self, answer):
        print("Base MenuFuncton did nothing on " + answer)

        return self.origin


# ============================================================================
# --------------------------------- Settings ---------------------------------
class ToggleCopy(MenuFunction):

    name = 'Copy to Clipboard by Default'
    options = ['Yes', 'No']

    def do_action(self, answer):
        if answer == 'Yes':
            config().copy = not config().copy
            config().save()

        return self.origin

    def update_welcome(self):
        self.welcome = "Set copy by default to " + str(not config().copy) + \
            '?'


class ToggleDebug(MenuFunction):

    name = 'Debug Mode'
    options = ['Yes', 'No']

    def do_action(self, answer):
        if answer == 'Yes':
            result = not config().debug
            config().debug = result

            if result:
                config().debuglog = 'debug.log'
            else:
                config().debuglog = None

            config().save()

        return self.origin

    def update_welcome(self):
        self.welcome = "Set debug mode to " + str(not config().debug) + "?"


class CoverLetterDir(MenuFunction):

    name = 'Cover Letter Directory'
    welcome = "Please select a directory where your cover letters & " + \
        "templates are..."
    options = ['Yes', 'No']
    option_back = None

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
    option_back = None

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
