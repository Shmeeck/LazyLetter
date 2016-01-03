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

    welcome = "This is a welcome message of a base Menu object."
    options = ['Please', 'Subclass', 'Me']
    local_map = {}

    def enter(self):
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

        result = navigate(self.local_map, result)

        return result


class MainMenu(Menu):
    options = ['Generate Cover Letter', 'Settings', 'Exit', 'Test']
    option_back = None
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )


class Settings(Menu):
    options = ['Cover Letter Directory',
               'Copy to Clipboard by Default',
               'Debug Mode',
               ]

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

    def enter(self):
        sys.exit(0)


def navigate(wonderous_map, start):
    destination = wonderous_map.get(start)
    heading = start
    origin = start

    while True:
        if not destination:
            break

        heading = destination.enter()

        destination = wonderous_map.get(heading)
        destination.origin = origin
        origin = heading

    return heading


world_map = {
             'Main Menu': MainMenu(),
             'Exit': Exit(),
             'Settings': Settings(),
             }


def hub_navigation(start='Main Menu'):
    navigate(world_map, start)
