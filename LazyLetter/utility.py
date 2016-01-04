import os


def list_options(options, pre_spaces=4):
    result = ""
    for i, option in enumerate(options):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option

        if not i == len(options)-1:
            result += '\n'

    return result


def clear_screen():
    try:
        clear = os.system('cls')
    except clear == 1:
        clear = os.system('clear')


def timedelta_string(delta):
    minutes, remainder = divmod(abs(delta.seconds), 60)
    seconds = remainder
    milliseconds = abs(delta.microseconds) // 10**3

    return str(minutes), str(seconds), str(milliseconds)
