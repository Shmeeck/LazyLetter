import os

from LazyLetter import filewalker
from LazyLetter import configurator
from LazyLetter.configurator import get_config
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
    assert_equals(get_config().default_path(None), result_path)

    # --- 2 ---
    result_path = os.path.join(os.path.dirname(base_path), "test")
    assert_equals(get_config().default_path("test"), result_path)

    # --- 3 ---
    result_path = os.path.join(base_path, "cheese")
    assert_equals(get_config().default_path(result_path), result_path)

# =======================================================================


# ========================== write_debug() test =========================

def setup_test_write_debug():
    get_config().debug = True


def teardown_test_write_debug():
    filewalker.delete(get_config().default_path(), 'test_debug.log')

    get_config().debug = default_config.debug
    get_config().debuglog = default_config.debuglog


@with_setup(setup_test_write_debug, teardown_test_write_debug)
def test_write_debug():
    """
    write_debug() method should return:
        1.  an error string containing the function where the bug occurred and
            the detailed message, no file if debuglog is unspecified
        2.  a file containing something similar to the above string is debuglog
            is a string
    """
    filepath = os.path.join(get_config().default_path(), 'test_debug.log')

    # --- 1 ---
    result = get_config().write_debug(test_write_debug.__name__,
                                      "failed because reasons")
    assert_in("test_write_debug", result)
    assert_in("failed because reasons", result)
    assert_raises(FileNotFoundError, open, filepath, 'r')

    # --- 2 ---
    get_config().debuglog = "test_debug.log"
    get_config().write_debug(test_write_debug.__name__,
                             "failed because reasons again")

    with open(filepath, 'r') as f:
        assert_in("failed because reasons again", f.read())
        f.close()

# =======================================================================


# =========================== load_dict() test ==========================

def teardown_load_dict():
    if hasattr(get_config(), 'shouldntexist'):
        del get_config().shouldntexist

    get_config().path_configs = default_config.path_configs


@with_setup(None, teardown_load_dict)
def test_load_dict():
    """
    load_dict method should save the following into the Config object:
        1.  a dict containing a key 'path_configs' should save its value into
            the object's attribute with the matching name.
        2.  a dict containing a key that's not an attribute shouldn't save into
            the Config() object
        3.  both 1 and 2 combined should still work as the method should just
            omit 2's input
    """

    # --- 1 ---
    test_dict = {'path_configs': os.path.abspath(configurator.__file__)}
    get_config().load_dict(test_dict)

    assert_equals(get_config().path_configs, test_dict['path_configs'])

    # --- 2 ---
    test_dict2 = {'shouldntexist': "butts"}
    get_config().load_dict(test_dict2)

    assert_equals(hasattr(get_config(), 'shouldntexist'), False)

    # --- 3 ---
    get_config().path_configs = get_config().default_path('config')

    test_dict = {**test_dict, **test_dict2}
    get_config().load_dict(test_dict)

    assert_equals(hasattr(get_config(), 'shouldntexist'), False)
    assert_equals(get_config().path_configs, test_dict['path_configs'])

test_path_configs = "test_config"
test_cfg_name = "test.cfg"

# =======================================================================


# =========================== save_load() test ==========================

def setup_save_load():
    get_config().path_letters = get_config().default_path("testletters")
    get_config().greeting = "GLaDOS"
    get_config().path_configs = get_config().default_path(test_path_configs)
    get_config().current_config = test_cfg_name


def teardown_save_load():
    filewalker.delete(get_config().path_configs, [test_cfg_name,
                                                    test_cfg_name+'.temp',
                                                    ])

    get_config().path_letters = default_config.path_letters
    get_config().greeting = default_config.greeting
    get_config().path_configs = default_config.path_configs
    get_config().current_config = default_config.current_config


@with_setup(setup_save_load, teardown_save_load)
def test_save_load():
    """
    Config should save all attributes and values into a json file and then
    be read back into the config object. Also, a failed load should return
    False.
    """
    result_config = configurator.Config(path_configs=test_path_configs,
                                        current_config=test_cfg_name,
                                        )

    get_config().save()
    result_config.load()

    assert_equals(result_config.path_letters, get_config().path_letters)
    assert_equals(result_config.greeting, get_config().greeting)

    # failed load testing
    sillyname = "testtestshouldntevereverexisteverneverever20198211029.cfpoop"
    get_config().current_config = sillyname
    assert_equals(get_config().load(), False)

# =======================================================================


# ========================== remove_save() test =========================

def setup_test_remove_save():
    get_config().path_configs = test_path_configs
    get_config().current_config = test_cfg_name


def teardown_test_remove_save():
    filewalker.delete(get_config().path_configs, [test_cfg_name,
                                                    test_cfg_name+'.temp',
                                                    ])

    get_config().path_configs = default_config.path_configs
    get_config().current_config = default_config.current_config


@with_setup(setup_test_remove_save, teardown_test_remove_save)
def test_remove_save():
    """
    after a Config() object is saved, remove_save() should be able to remove it
    and return True, otherwise, False
    """

    get_config().save()
    assert_equals(get_config().remove_save(), True)
    assert_equals(get_config().remove_save(), False)

# =======================================================================


# ==================== rename_current_config() test ===================

def setup_test_rename_current_config():
    get_config().path_configs = test_path_configs
    get_config().current_config = test_cfg_name


def teardown_test_rename_current_config():
    filewalker.delete(get_config().path_configs, [test_cfg_name,
                                                    test_cfg_name+'.temp',
                                                    test_cfg_name+'2',
                                                    test_cfg_name+'2.temp',
                                                    ])

    get_config().path_configs = default_config.path_configs
    get_config().current_config = default_config.current_config


@with_setup(setup_test_rename_current_config,
            teardown_test_rename_current_config)
def test_rename_current_config():
    """
    rename_current_config() should be able to change the value of
    current_config and alter the save file, should pass back the new name
    """

    get_config().save()
    assert_equals(get_config().rename_current_config(test_cfg_name+'2'),
                  test_cfg_name+'2')
    assert_equals(get_config().current_config, test_cfg_name+'2')

# =======================================================================


# ========================= change_config() test ========================

def setup_test_change_config():
    get_config().path_configs = test_path_configs
    get_config().current_config = test_cfg_name


def teardown_test_change_config():
    filewalker.delete(get_config().path_configs, [test_cfg_name,
                                                    test_cfg_name+'.temp',
                                                    test_cfg_name+'2',
                                                    test_cfg_name+'2.temp',
                                                    ])

    get_config().path_configs = default_config.path_configs
    get_config().current_config = default_config.current_config


@with_setup(setup_test_change_config, teardown_test_change_config)
def test_change_config():
    """
    change_config() should switch to the given filename.cfg and return said
    name; if the new filename does not exist, then return the old name that
    existed prior to the function call
    """
    dest_config = configurator.Config(path_configs=test_path_configs,
                                      current_config=test_cfg_name+'2')

    # return the old name
    get_config().save()
    assert_equals(get_config().change_config(test_cfg_name+'2'),
                  test_cfg_name)

    # return the new name because it's save file actually exists
    dest_config.save()
    assert_equals(get_config().change_config(test_cfg_name+'2'),
                  test_cfg_name+'2')

# =======================================================================


# ========================= cleanup directories =========================

def teardown():
    """
    if the config directory had to be made just for this test, remove it
    """
    get_config().path_configs = test_path_configs

    if not os.listdir(get_config().path_configs):
        os.removedirs(get_config().path_configs)

    get_config().path_configs = default_config.path_configs

# =======================================================================
