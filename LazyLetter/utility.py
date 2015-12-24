import os
import sys


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
