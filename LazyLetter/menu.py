import sys

from . import utility
from . import question
from .configurator import get_config as config


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

    welcome = "This is a welcome message of a base Menu object:"
    options = ['Please', 'Subclass', 'Me']
    name = 'Base Menu'
    local_map = {}

    def enter(self):
        result = self.get_answer()
        return navigate(self.local_map, result, self.name)

    def get_answer(self):
        utility.clear_screen()
        go_back = ''

        if self.option_back:
            go_back = self.option_back.format(self.origin)
            self.options.append(go_back)

        result = question.handler(self.options, self.welcome,
                                  self.option_redo, self.msg_noresult,
                                  self.msg_multiple,
                                  )

        if self.option_back:
            self.options.pop()
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


class MainMenu(Menu):
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )
    name = 'Main Menu'
    options = ['Generate Cover Letter', 'Settings', 'Exit']
    option_back = None


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
    options = ['Cover Letter Directory',
               'Copy to Clipboard by Default',
               'Debug Mode',
               ]
    local_map = {'Debug Mode': ToggleDebug(),
                 }

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


def navigate(wonderous_map, start, origin=None):
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
    if not origin:
        origin = start
    else:
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


# deals with the main overworld menu options
world_map = {
             'Main Menu': MainMenu(),
             'Exit': Exit(),
             'Settings': Settings(),
             }


def hub_navigation(start='Main Menu'):
    """
    This function initiates the entire shabangbang!
    """
    navigate(world_map, start)
