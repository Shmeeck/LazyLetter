import os

from LazyLetter import coverletter
from LazyLetter.configurator import Config
from nose.tools import *

test_config = Config(path_letters='test_cover-letters')
test_lettername1 = ['test_awesomecompany.txt',
                    "I think {company} is great!\n\n\nSincerely,\nMe",
                    ]
test_lettername2 = ['test_throwaway.txt',
                    "That's why I'm dah BESTEST!",
                    ]
test_lettername3 = ['test_shouldntwork.tyt',
                    "Dear {greeting},\n\nI got nothing.",
                    ]
test_letterlist = [test_lettername1,
                   test_lettername2,
                   test_lettername3,
                   ]
test_letternamelist = [test_lettername1[0],
                       test_lettername2[0],
                       ]


def setup():
    dirpath = test_config.path_letters

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    for letter in test_letterlist:
        with open(os.path.join(dirpath, letter[0]), 'w') as f:
            f.write(letter[1])
            f.close()


def test_get_list():
    """
    get_list() should return a list of all of the cover letters within the
    path specified by path_letters in the Config() object
    """
    result = coverletter.get_list(test_config)

    assert_equals(result, test_letternamelist)


def test_get():
    """
    get() should return:
        1.  the contents of the cover letter file with the name of the passed
            string.
        2.  # THIS IS WHERE I LEFT OFF
    """
    # FINISH ME


def teardown():
    dirpath = test_config.path_letters

    for letter in test_letterlist:
        filepath = os.path.join(dirpath, letter[0])

        if os.path.exists(filepath):
            os.remove(filepath)

    if not os.listdir(dirpath):
        os.removedirs(dirpath)
