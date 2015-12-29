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


def _filter_options(li, answer):
    """
    Takes a list of lower-cased options and a letter and returns back a list
    of options that only contain said letter.
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


def _search_entire(li, answer):
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
    result = _filter_options(li, answer)
    potential_result = []

    if len(result) > 1:
        # last attempt to narrow down the list by trying to match the
        # entire answer within the each list element
        potential_result = _search_entire(result, answer)

        # only return if successful matches were found
        if len(potential_result) > 0:
            return potential_result

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

    multiple_result_msg = "Your answer matched more than one possible option:"
    no_result_msg = "Sorry, couldn't understand that..."
    redo_menu_option = "None of These"

    def __init__(self):
        self.welcome = "This is a welcome message of a base Menu object."
        self.options = ['Please', 'Subclass', 'Me']
        self.local_map = {}

    def enter(self):
        while True:
            utility.clear_screen()

            print(self.welcome)
            print(list_options(self.options))

            result = input(config().prompt)
            result = parse_options(self.options, result)
            result = self.multiple_result_handler(result)

            if not result:
                continue
            else:
                result = navigate(self.local_map, result[0])
                return result[0]

    def multiple_result_handler(self, li):
        while True:
            if len(li) > 1:
                li.append(self.redo_menu_option)

                print(self.multiple_result_msg)
                print(list_options(li))

                result = input(config().prompt)
                result = parse_options(li, result)

                if not result:
                    print(self.no_result_msg)
                    continue

                li = result
            elif li[0] == self.redo_menu_option:
                return []
            else:
                return li


def hub():
    options = ['Generate Cover Letter', 'Settings', 'Exit']
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )
    while True:
        utility.clear_screen()

        print(welcome)
        print(list_options(options))

        user_in = input('> ')
        print(parse_options(options, user_in))

        input(config().continue_msg)


def settings():
    options = ['']


def exit():
    pass


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
