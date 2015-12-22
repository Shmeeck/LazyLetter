import os

from LazyLetter import configurator
from LazyLetter.configurator import main_config
from nose.tools import *

# ==================== Config() Class Tests ====================


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
    main_config.__init__()
    base_path = os.path.dirname(os.path.abspath(configurator.__file__))

    # --- 1 ---
    result_path = os.path.dirname(base_path)
    assert_equals(main_config.default_path(None), result_path)

    # --- 2 ---
    result_path = os.path.join(os.path.dirname(base_path), "test")
    assert_equals(main_config.default_path("test"), result_path)

    # --- 3 ---
    result_path = os.path.join(base_path, "cheese")
    assert_equals(main_config.default_path(result_path), result_path)


def test_write_debug():
    """
    write_debug() method should return:
        1.  an error string containing the function where the bug occurred and
            the detailed message, no file if debuglog is unspecified
        2.  a file containing something similar to the above string is debuglog
            is a string
    """
    main_config.__init__(debug=True)
    filepath = os.path.join(main_config.default_path(), 'test_debug.log')

    # --- 1 ---
    result = main_config.write_debug(test_write_debug.__name__,
                                     "failed because reasons")
    assert_in("test_write_debug", result)
    assert_in("failed because reasons", result)
    assert_raises(FileNotFoundError, open, filepath, 'r')

    # --- 2 ---
    main_config = configurator.Config(debug=True, debuglog="test_debug.log")
    main_config.write_debug(test_write_debug.__name__,
                            "failed because reasons again")

    with open(filepath, 'r') as f:
        assert_in("failed because reasons again", f.read())


def test_load_dict():
    """
    load_dict method should save the following into the Config object:
        1.  a dict containing a key 'path_save' should save its value into the
            object's attribute with the matching name.
        2.  a dict containing a key that's not an attribute shouldn't save into
            the Config() object
        3.  both 1 and 2 combined should still work as the method should just
            omit 2's input
    """
    main_config.__init__()

    # --- 1 ---
    test_dict = {'path_save': os.path.abspath(configurator.__file__)}
    main_config.load_dict(test_dict)

    assert_equals(main_config.path_save, test_dict['path_save'])

    # --- 2 ---
    test_dict2 = {'shouldntexist': "butts"}
    main_config.load_dict(test_dict2)

    assert_equals(main_config.__dict__.get('shouldntexist'), None)

    # --- 3 ---
    main_config.__init__()  # reset the object
    test_dict = {**test_dict, **test_dict2}
    main_config.load_dict(test_dict)

    assert_equals(main_config.__dict__.get('shouldntexist'), None)
    assert_equals(main_config.path_save, test_dict['path_save'])

test_path_save = "main_config"
test_cfg_name = "test.cfg"


def test_save_load():
    """
    Config should save all attributes and values into a json file and then
    be read back into the config object. Also, a failed load should return
    False.
    """
    main_config.__init__(path_letters="testletters",
                         greeting="GLaDOS",
                         path_save=test_path_save,
                         current_filename=test_cfg_name,
                         )
    result_config = configurator.Config(path_save=test_path_save,
                                     current_filename=test_cfg_name,
                                     )

    main_config.save()
    result_config.load()

    assert_equals(result_config.path_letters, main_config.path_letters)
    assert_equals(result_config.greeting, main_config.greeting)

    # failed load testing
    sillyname = "testtestshouldntevereverexisteverneverever20198211029.cfpoop"
    main_config = configurator.Config(current_filename=sillyname)
    assert_equals(main_config.load(), False)


def test_remove_save():
    """
    after a Config() object is saved, remove_save() should be able to remove it
    and return True, otherwise, False
    """
    main_config = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name)

    main_config.save()
    assert_equals(main_config.remove_save(), True)
    assert_equals(main_config.remove_save(), False)


def test_rename_current_filename():
    """
    rename_current_filename() should be able to change the value of
    current_filename and alter the save file, should pass back the new name
    """
    main_config = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name)

    main_config.save()
    assert_equals(main_config.rename_current_filename(test_cfg_name+'2'),
                  test_cfg_name+'2')
    assert_equals(main_config.current_filename, test_cfg_name+'2')


def test_change_config():
    """
    change_config() should switch to the given filename.cfg and return said
    name; if the new filename does not exist, then return the old name that
    existed prior to the function call
    """
    main_config = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name+'3')
    dest_config = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name+'4')

    # return the old name
    main_config.save()
    assert_equals(main_config.change_config(test_cfg_name+'4'), test_cfg_name+'3')

    # return the new name because it's save file actually exists
    dest_config.save()
    assert_equals(main_config.change_config(test_cfg_name+'4'), test_cfg_name+'4')


def teardown():
    """
    clears out any files that stick around if the save_load test fails
    """
    main_config = configurator.Config(path_save=test_path_save)

    filepath = os.path.join(main_config.path_save, test_cfg_name)
    temppath = filepath + '.temp'
    logpath = os.path.join(main_config.default_path(), 'test_debug.log')

    if os.path.exists(logpath):
        os.remove(logpath)

    if os.path.exists(main_config.path_save):
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(temppath):
            os.remove(temppath)
        for i in range(2, 5):
            if os.path.exists(filepath+str(i)):
                os.remove(filepath+str(i))

        # if the config directory had to be made just for this test, remove it
        if not os.listdir(main_config.path_save):
            os.removedirs(main_config.path_save)
