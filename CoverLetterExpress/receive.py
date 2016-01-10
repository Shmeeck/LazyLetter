from . import ask
from .configurator import get_config as config


class UserInput(object):

    def __init__(self, test_inputs=None):
        self.test_inputs = test_inputs
        self._i = 0

    def get(self, li=None, question=None):
        if self.test_inputs:
            return self.get_next()

        ask.question(li, question)
        result = input(config().prompt)

        return result

    def get_next(self):
        result = self.test_inputs[self._i]
        self._i += 1

        return result

    def set_test(self, test_inputs):
        self.test_inputs = test_inputs
        self._i = 0


main_womper = UserInput()


def user_input():
    return main_womper
