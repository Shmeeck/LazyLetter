from .ask import list_options
from .configurator import get_config as config


class Womp(object):

    def __init__(self, test_inputs=None):
        self.test_inputs = test_inputs
        self._i = 0

    def get(self, li=None, question=None):
        if self.test_inputs:
            return self.get_next()
        else:
            if question:
                print(question)
            if li:
                print(list_options(li))

            result = input(config().prompt)

            return result

    def get_next(self):
        result = self.test_inputs[self._i]
        self._i += 1

        return result

    def set_test(self, test_inputs):
        self.test_inputs = test_inputs
        self._i = 0


main_womper = Womp()


def load_in():
    return main_womper
