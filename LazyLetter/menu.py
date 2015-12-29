import datetime

from . import utility
from .configurator import get_config as config


def _list_options(options, comments=None, pre_spaces=4):
    """
    Prints an enumerated list for the user to select from, said list will be
    1-based for user friendliness. Comments can be added via a separate list
    that much match 1-to-1 indices with the options list.
    """
    result = ""
    for i, option in enumerate(options):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option

        if comments:
            comment = comments.get(i, '')

            if comment:
                result += ' (' + comments[i], ')'

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
    returns any successful matches.
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
    result = -1  # user options list is 1-based

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


def hub():
    options = ['Generate Cover Letter', 'Settings', 'Exit']
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )
    while True:
        utility.clear_screen()

        print(welcome)
        print(_list_options(options))

        user_in = input('> ')
        print(parse_options(options, user_in))

        input('Press ENTER to continue...')


def settings():
    options = ['']
