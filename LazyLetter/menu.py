import datetime
import sys

from . import utility
from .configurator import get_config as config


def list_options(options, pre_spaces=4):
    result = ""
    for i, option in enumerate(options):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option

        if not i == len(options)-1:
            result += '\n'

    return result


def filter_each_letter(li, answer):
    """
    Takes a list of lower-cased options and a string and returns back a list
    of options that only contain all letters of the string with order.
    """
    result = []
    answer = answer.replace(' ', '')

    for item in li:
        letter_pos = 0
        success = True

        for letter in answer.lower():
            letter_pos = item.lower().find(letter, letter_pos)

            if letter_pos < 0:
                success = False
                break

        if success:
            result.append(item)

    return result


def filter_entire_string(li, answer):
    """
    Attempts to match a given response's entire case within a list of values,
    returns any successful matches. An exact answer to list element match takes
    immediate priority and returns a list with just that element.
    """
    result = []
    answer = answer.lower()

    for item in li:
        lower_item = item.lower()

        if answer in lower_item:
            if answer == lower_item:
                return [item]

            result.append(item)

    return result


def _search_int(li, answer):
    # user options list is 1-based
    result = -1

    try:
        result += int(answer)
    except ValueError:
        return None

    if result >= 0 and result < len(li):
        return [li[result]]
    else:
        return []


def _parse_options(li, answer):
    """
    WIP - bug if options are akin to 'Exit' and 'Save and Exit' will return
          -2 if 'Exit' is passed.

    Takes in a list of options and a user response which can be either an
    int or any combination of letters within a certain option, or options.

    Returns a list of any matching values.
    """
    # check, and return single answer or [], if int
    result = _search_int(li, answer)

    if result is not None:
        return result

    # search by each letter in the answer, order of letters matter
    # (by order I mean, ingsttse will not return settings)
    result = filter_each_letter(li, answer)
    potential_result = []

    if len(result) > 1:
        # last attempt to narrow down the list by trying to match the
        # entire answer within the each list element
        potential_result = filter_entire_string(result, answer)

        # only return if successful matches were found
        if len(potential_result) > 0:
            return potential_result

    return result


def ask_input(li, question):
    print(question)
    print(list_options(li))
    result = input(config().prompt)

    return result


def debug_timer(func):
    def inner(*args, **kwargs):
        if config().debug:
            start_time = datetime.datetime.now()

            result = func(*args, **kwargs)

            delta = datetime.datetime.now() - start_time
            delta_string = utility.timedelta_string(delta)

            message = str("completed in " +
                          delta_string[0] + 'm, ' + delta_string[1] + 's, ' +
                          delta_string[2] + 'ms'
                          )
            config().write_debug(func.__name__, message)
        else:
            result = func(*args, **kwargs)

        return result

    return inner


@debug_timer
def parse_options(options, user_in):
    return _parse_options(options, user_in)


class Menu(object):

    """
    The base object that acts as a node for the user to navigate between
    application features. local_map can be specified to transfer the user
    between individual methods by mapping the option string to the method
    itself.
    """

    multiple_result_msg = "Your answer matched more than one possible option:"
    no_result_msg = "Sorry, couldn't understand that..."
    redo_menu_option = "None of These"

    welcome = "This is a welcome message of a base Menu object."
    options = ['Please', 'Subclass', 'Me']
    local_map = {}

    def enter(self):
        utility.clear_screen()

        result = self.question_handler(self.options, self.welcome)
        result = navigate(self.local_map, result)

        return result

    def question_handler(self, li, question):
        """
        Accepts a list of options and a question to display to the user, an
        enumerated version of the list is always displayed after the question,
        the function will continuously filter the user's answer and the list
        until the following is satisfied:
            1. The result is not blank
            2. There is only a single result

        If there are multiple options in the result after filtering, a
        recursive call is made with the remaining options only if the
        options were narrowed since the last recurse, otherwise, continue.
        An option to leave the narrowed listings is made available in this
        stage of filtering.
        """
        result = []

        while True:
            result = li

            answer = ask_input(result, question)
            result = parse_options(result, answer)

            if not result or not answer:
                print(self.no_result_msg)
                continue
            elif len(result) > 1:
                # add the ability to display the whole list again
                if not li[len(li)-1] == self.redo_menu_option:
                    result.append(self.redo_menu_option)
                elif result == li[:len(li)-1]:
                    continue

                # let's go again with only the remaining options
                result = self.question_handler(result,
                                               self.multiple_result_msg,
                                               )

            if result == self.redo_menu_option:
                # we gotta go back to the start of the stack...
                if not li[len(li)-1] == self.redo_menu_option:
                    continue

            break

        return result[0]


class MainMenu(Menu):
    options = ['Generate Cover Letter', 'Settings', 'Exit', 'Test']
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )

    def test(self):
        print("HOORAY!")
        print(self.options)

    local_map = {'Test': test}


class Settings(Menu):
    options = []


class Exit(Menu):

    def enter(self):
        sys.exit(0)


def navigate(wonderous_map, start):
    destination = wonderous_map.get(start)
    heading = start

    while True:
        if not destination:
            break

        if callable(destination):
            heading = destination()
        else:
            heading = destination.enter()

        destination = wonderous_map.get(heading)

    return heading


world_map = {
             'Main Menu': MainMenu(),
             'Exit': Exit(),
             }


def hub_navigation(start='Main Menu'):
    navigate(world_map, start)
