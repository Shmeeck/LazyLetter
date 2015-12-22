import os

from LazyLetter import utility
from LazyLetter import coverletter
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
    result = coverletter.get_list()

    assert_equals(result, test_letternamelist)


def test_get():
    """
    get() should return:
        1.  the contents of the cover letter file with the name of the passed
            string.
        2.  a blank string if there's no file
    """
    # --- 1 ---
    result = coverletter.get(test_lettername1[0])
    assert_equals(result, test_lettername1[1])

    # --- 2 ---
    result = coverletter.get("THISSOULDNTeverexistnever20193")
    assert_equals(result, "")


def test_delete():
    """
    delete() should return:
        1.  True if the file exists and was deleted successfully.
        2.  False if otherwise
    """
    # --- 1 ---
    assert_equals(coverletter.delete(test_lettername1[0]), True)

    # --- 2 ---
    assert_equals(coverletter.delete(test_lettername1[0]), False)


def teardown():
    dirpath = get_config().path_letters

    for letter in test_letterlist:
        utility.delete_file(dirpath, letter[0])

    if not os.listdir(dirpath):
        os.removedirs(dirpath)

    get_config().path_letters = default_config.path_letters
