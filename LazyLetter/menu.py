import datetime

from . import utility
from .configurator import get_config


def _list_options(options, pre_spaces=4):
    result = ""
    for i, option in enumerate(options):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option

        if not i == len(options)-1:
            result += '\n'

    return result


def _filter_options(lower_options, letter):
    """
    Takes a list of lower-cased options and a letter and returns back a list
    of options that only contain said letter.
    """
    working_options = []

    for option in lower_options:
        if len(option[1]) == 0:
            continue
        if letter in option[1]:
            letter_pos = option[1].find(letter)

            new_option = [option[0], option[1][letter_pos+1:]]
            working_options.append(new_option)

    return working_options


def _parse_options(options, answer):
    """
    WIP - instead of a -2 return, maybe a tuple of the many options?
    WIP - bug if options are akin to 'Exit' and 'Save and Exit' will return
          -2 if 'Exit' is passed.

    Takes in a list of options and a user response which can be either an
    int or any combination of letters within a certain option, or options.

    Returns the index-value of the matching option, -1 if nothing matches, or
    -2 if too many things match.
    """
    try:
        answer = int(answer)
        answer -= 1  # user options list is 1-based

        if answer >= 0 and answer < len(options):
            return answer
        else:
            return -1
    except ValueError:
        # --- Remove case sensitivity issues ---
        lower_options = [None] * len(options)

        for i, option in enumerate(options):
            lower_options[i] = [i, option.lower()]

        answer = answer.replace(' ', '').lower()
        # --------------------------------------

        for letter in answer:
            lower_options = _filter_options(lower_options, letter)

            if len(lower_options) == 0:
                return -1

        if len(lower_options) > 1:
            # before returning -2 for 2+ results, check to see if the full
            # answer matches any of the remaining options
            # WIP - Works well for longer answers, not so much for fragments of
            #       words (i.e 'ett' defaults to the first encounter, letter)
            single_result = None
            for option in lower_options:
                if answer in options[option[0]].lower():
                    if not single_result:
                        single_result = option[0]
                    else:
                        return -2

            if single_result:
                return single_result
            else:
                return -2
        else:
            return lower_options[0][0]


def debug_timer(func):
    def inner(*args, **kwargs):
        if get_config().debug:
            start_time = datetime.datetime.now()

            result = func(*args, **kwargs)

            delta = datetime.datetime.now() - start_time
            delta_string = utility.timedelta_string(delta)

            message = str("completed in " +
                          delta_string[0] + 'm, ' + delta_string[1] + 's, ' +
                          delta_string[2] + 'ms'
                          )
            get_config().write_debug(func.__name__, message)
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
