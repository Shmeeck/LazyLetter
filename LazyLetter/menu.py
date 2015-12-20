import os

from . import coverletter


def _list_options(options, pre_spaces=4):
    result = ""
    for i, option in enumerate(options):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option + '\n'

    return result


def _filter_options(lower_options, letter):
    """
    Takes a lise of lower-cased options and a letter and returns back a list
    of options that only contain said letter.
    """
    working_options = []

    for option in lower_options:
        # start after 0 position, 0th letter is the overall index value
        if len(option) <= 1:
            continue
        if letter in option[1:]:
            new_option = option.replace(letter, '', 1)
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
            lower_options[i] = str(i) + option.lower()

        answer = answer.replace(' ', '').lower()
        # --------------------------------------

        for letter in answer:
            lower_options = _filter_options(lower_options, letter)

            if len(lower_options) == 0:
                return -1

        if len(lower_options) > 1:
            return -2
        else:
            return int(lower_options[0][0])


def hub(config):
    options = ['Generate Cover Letter', 'Settings', 'Exit']
    welcome = str("Navigate through the various menus by entering the " +
                  "option, or option number, below:"
                  )
    while True:
        print(welcome)
        print(_list_options(options))
