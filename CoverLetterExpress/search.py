import datetime

from . import utility
from .configurator import get_config as config


def debug_timer(func):
    """
    Decorator for any function that needs to be timed, reports it's findings
    to the Config().write_debug() method.
    """
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


def each_letter(li, answer):
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


def entire_string(li, answer):
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


def index(li, answer):
    """
    Converts an string with an int into an int and checks with the bounds of
    the given lists.

    Returns None on fail.
    """
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


@debug_timer
def everything(li, answer):
    """
    Takes in a list of options and a user response which can be either an
    int or any combination of letters within a certain option, or options.

    Returns a list of any matching values.
    """
    # check, and return single answer or [], if int
    result = index(li, answer)

    if result is not None:
        return result

    # search by each letter in the answer, order of letters matter
    # (by order I mean, ingsttse will not return settings)
    result = each_letter(li, answer)
    potential_result = []

    if len(result) > 1:
        # last attempt to narrow down the list by trying to match the
        # entire answer within the each list element
        potential_result = entire_string(result, answer)

        # only return if successful matches were found
        if len(potential_result) > 0:
            return potential_result

    return result
