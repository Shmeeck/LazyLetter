import os

from LazyLetter import filewalker
from LazyLetter import configurator
from LazyLetter.configurator import get_config
from nose.tools import *

test_lettername1 = ['test_awesomecompany' + get_config().file_type_letters,
                    "I think {company} is great!\n\n\nSincerely,\nMe",
                    ]
test_lettername2 = ['test_throwaway' + get_config().file_type_letters,
                    "That's why I'm dah BESTEST!",
                    ]
test_lettername3 = ['test_shouldntwork' + get_config().file_type_letters+'2',
                    "Dear {greeting},\n\nI got nothing.",
                    ]
test_letterlist = [test_lettername1,
                   test_lettername2,
                   test_lettername3,
                   ]
test_letternamelist = [test_lettername1[0],
                       test_lettername2[0],
                       ]

default_config = configurator.Config()


def setup():
    get_config().path_letters = get_config().default_path('test_cover-letters')
    get_config().file_type_letters = '.txt'

    dirpath = get_config().path_letters

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
    result = filewalker.get_list(get_config().path_letters,
                                 get_config().file_type_letters)

    assert_equals(result, test_letternamelist)


def teardown():
    dirpath = get_config().path_letters

    for letter in test_letterlist:
        filewalker.delete(dirpath, letter[0])

    if not os.listdir(dirpath):
        os.removedirs(dirpath)

    get_config().path_letters = default_config.path_letters
    get_config().file_type_letters = default_config.file_type_letters
