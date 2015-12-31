import os

from LazyLetter import filewalker
from LazyLetter import configurator
from LazyLetter.configurator import get_config as config
from nose.tools import *

default_config = configurator.Config()


# ========================= default_path() test =========================

def test_default_path():
    """
    default_path method should return:
        1.  if the 'path' kwarg is none, the path of the parent directory of
            configurator.py file
        2.  if the 'path' kwarg is a string, a path with a directory within
            the parent directory of configurator.py, named as the string
        3.  if the 'path' kwarg is an actual path, then it will return the
            same path
    """
    base_path = os.path.dirname(os.path.abspath(configurator.__file__))

    # --- 1 ---
    result_path = os.path.dirname(base_path)
    assert_equals(configurator.default_path(None), result_path)

    # --- 2 ---
    result_path = os.path.join(os.path.dirname(base_path), "test")
    assert_equals(configurator.default_path("test"), result_path)

    # --- 3 ---
    result_path = os.path.join(base_path, "cheese")
    assert_equals(configurator.default_path(result_path), result_path)

# =======================================================================


# ========================== write_debug() test =========================

def setup_test_write_debug():
    config().debug = True


def teardown_test_write_debug():
    filewalker.delete(configurator.default_path(), 'test_debug.log')

    config().debug = default_config.debug
    config().debuglog = default_config.debuglog


@with_setup(setup_test_write_debug, teardown_test_write_debug)
def test_write_debug():
    """
    write_debug() method should return:
        1.  an error string containing the function where the bug occurred and
            the detailed message, no file if debuglog is unspecified
        2.  a file containing something similar to the above string is debuglog
            is a string
    """
    filepath = os.path.join(configurator.default_path(),
                            'test_debug.log')

    # --- 1 ---
    result = config().write_debug(test_write_debug.__name__,
                                  "failed because reasons")
    assert_in("test_write_debug", result)
    assert_in("failed because reasons", result)
    assert_raises(FileNotFoundError, open, filepath, 'r')

    # --- 2 ---
    config().debuglog = "test_debug.log"
    config().write_debug(test_write_debug.__name__,
                         "failed because reasons again")

    with open(filepath, 'r') as f:
        assert_in("failed because reasons again", f.read())
        f.close()

# =======================================================================


# =========================== load_dict() test ==========================

def teardown_load_dict():
    if hasattr(config, 'shouldntexist'):
        del config().shouldntexist


@with_setup(None, teardown_load_dict)
def test_load_dict():
    """
    load_dict method should save the following into the Config object:
        1.  a dict containing a key 'path_letters' should save its value into
            the object's attribute with the matching name.
        2.  a dict containing a key that's not an attribute shouldn't save into
            the Config() object
        3.  both 1 and 2 combined should still work as the method should just
            omit 2's input
    """

    # --- 1 ---
    test_dict = {'path_letters': os.path.abspath(configurator.__file__)}
    config()._load_dict(test_dict)

    assert_equals(config().path_letters, test_dict['path_letters'])

    # --- 2 ---
    test_dict2 = {'shouldntexist': "butts"}
    config()._load_dict(test_dict2)

    assert_equals(hasattr(config, 'shouldntexist'), False)

    # --- 3 ---
    config().path_letters = default_config.path_letters

    test_dict = {**test_dict, **test_dict2}
    config()._load_dict(test_dict)

    assert_equals(hasattr(config, 'shouldntexist'), False)
    assert_equals(config().path_letters, test_dict['path_letters'])

# =======================================================================


# =========================== save_load() test ==========================

def setup_save_load():
    config().path_letters = configurator.default_path("testletters")
    config().greeting = "GLaDOS"


def teardown_save_load():
    filewalker.delete(config()._path_config, [config()._name_config,
                                              config()._name_config+'.temp',
                                              ])

    config().path_letters = default_config.path_letters
    config().greeting = default_config.greeting


@with_setup(setup_save_load, teardown_save_load)
def test_save_load():
    """
    Config should save all attributes and values as a dict into a json file
    and then be read back into the config object. If save(force=False) then a
    FileExistsError exception should be raised if the save was already done.
    """

    config().save()
    result_config = configurator.Config.load()

    assert_equals(result_config.path_letters, config().path_letters)
    assert_equals(result_config.greeting, config().greeting)

    assert_raises(FileExistsError, config().save, force=False)

# =======================================================================


# ========================= cleanup directories =========================

def teardown():
    """
    if the config directory had to be made just for this test, remove it
    """

    if not os.listdir(config()._path_config):
        os.removedirs(config()._path_config)

# =======================================================================
