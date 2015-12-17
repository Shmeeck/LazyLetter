import os

from LazyLetter import coverletter
from LazyLetter.configurator import Config
from nose.tools import *

test_config = Config(path_letters='test_cover-letters')
test_lettername1 = ['awesomecompany.txt',
                    "I think {company} is great!\n\n\nSincerely,\nMe",
                    ]
test_lettername2 = ['throwaway.txt',
                    "That's why I'm dah BESTEST!",
                    ]
test_lettername3 = ['shouldntwork.tyt',
                    "Dear {greeting},\n\nI got nothing.",
                    ]
test_letterlist = [testlettername1,
                   testlettername2,
                   testlettername3,
                   ]


def setup():
    dirpath = testconfig.path_letters

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    for letter in test_letterlist:
        with open(os.path.join(dirpath, letter[0])) as f:
            # THIS IS WHERE I LEFT OFF
            pass


def test_get_list():
    """
    get_list() should return a list of all of the cover letters within the
    path specified by path_letters in the Config() object
    """
    result = coverletter.get_list(test_config)
    # FINISH ME
