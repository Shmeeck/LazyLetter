import sys

from . import utility
from . import question
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

    def enter(self):
        while True:
            result = self.get_answer()
            result = navigate(self.local_map, result, self.name)

            if result == self.name:
                continue
            else:
                return result

    def get_answer(self):
        utility.clear_screen()
        go_back = ''

        if self.option_back:
            go_back = self.option_back.format(self.origin)
            self.local_map.keys.append(go_back)

        result = question.handler(self.local_map.keys, self.welcome,
                                  self.option_redo, self.msg_noresult,
                                  self.msg_multiple,
                                  )

        if self.option_back:
            self.local_map.keys.pop()
        if result == go_back:
            return self.origin

        return result


class MenuFunction(Menu):

    """
    A base object for performing a specific action within a Menu object.
    """

    welcome = "This is a welcome message of a base MenuFunction object:"
    name = 'Base Menu Function'
    options = []

    def enter(self):
        result = self.get_answer()
        return self.do_action(result)

    def do_action(self, answer):
        print("Base MenuFuncton did nothing on " + answer)

        return self.origin


class ToggleDebug(MenuFunction):

    welcome = "Set debug mode to " + str(not config().debug) + "?"
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

        return self.origin


class Settings(Menu):
    name = 'Settings'
    local_map = WonderousMap([ToggleDebug(),
                              ])

    def enter(self):
        self.welcome = self.get_current_settings() + \
            str("Select which setting you would like to modify:")

        return super().enter()

    def get_current_settings(self):
        result = 'Cover Letter Directory: ' + str(config().path_letters) + \
                 '\n' + 'Copy to Clipboard by Default: ' + \
                 str(config().copy) + '\n' + 'Debug Mode: ' + \
                 str(config().debug) + '\n\n'

        return result


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
