import datetime

from . import utility
from .configurator import get_config as config
from .input import load_in


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


def filter_index(li, answer):
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
def filter_all(li, answer):
    """
    Takes in a list of options and a user response which can be either an
    int or any combination of letters within a certain option, or options.

    Returns a list of any matching values.
    """
    # check, and return single answer or [], if int
    result = filter_index(li, answer)

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


def handler(li, question,
            option_redo,
            msg_noresult,
            msg_multiple=None,
            ):
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

        answer = load_in().get(result, question)
        result = filter_all(result, answer)

        if not result or not answer:
            print(msg_noresult)
            continue
        elif len(result) > 1:
            # add the ability to display the whole list again
            if not li[len(li)-1] == option_redo:
                result.append(option_redo)
            elif result == li[:len(li)-1]:
                continue

            # let's go again with only the remaining options
            if not msg_multiple:
                msg_multiple = question

            result = handler(result, msg_multiple,
                             option_redo,
                             msg_noresult,
                             )

        if result == option_redo:
            # we gotta go back to the start of the stack...
            if not li[len(li)-1] == option_redo:
                continue

        break

    return result[0]
