import os

from LazyLetter import configurator
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
    test_obj = configurator.Config()
    base_path = os.path.dirname(os.path.abspath(configurator.__file__))

    # --- 1 ---
    result_path = os.path.dirname(base_path)
    assert_equals(test_obj.default_path(None), result_path)

    # --- 2 ---
    result_path = os.path.join(os.path.dirname(base_path), "test")
    assert_equals(test_obj.default_path("test"), result_path)

    # --- 3 ---
    result_path = os.path.join(base_path, "cheese")
    assert_equals(test_obj.default_path(result_path), result_path)


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
    test_obj = configurator.Config()

    # --- 1 ---
    test_dict = {'path_save': os.path.abspath(configurator.__file__)}
    test_obj.load_dict(test_dict)

    assert_equals(test_obj.path_save, test_dict['path_save'])

    # --- 2 ---
    test_dict2 = {'shouldntexist': "butts"}
    test_obj.load_dict(test_dict2)

    assert_equals(test_obj.__dict__.get('shouldntexist'), None)

    # --- 3 ---
    test_obj = configurator.Config()  # reset the object
    test_dict = {**test_dict, **test_dict2}
    test_obj.load_dict(test_dict)

    assert_equals(test_obj.__dict__.get('shouldntexist'), None)
    assert_equals(test_obj.path_save, test_dict['path_save'])


def test_save_load():
    """
    Config should save all attributes and values into a json file and then
    be read back into the config object
    """
    test_obj = configurator.Config(path_letters="testletters",
                                   greeting="GLaDOS",
                                   )
    test_obj.save('test.cfg')
    result_obj = configurator.Config()
    result_obj.load('test.cfg')

    assert_equals(result_obj.path_letters, test_obj.path_letters)
    assert_equals(result_obj.greeting, test_obj.greeting)


def teardown():
    test_obj = configurator.Config()
    filepath = os.path.join(test_obj.path_save, 'test.cfg')
    temppath = filepath + '.temp'

    if os.path.exists(filepath):
        os.remove(os.path.join(test_obj.path_save, 'test.cfg'))
    if os.path.exists(temppath):
        os.remove(os.path.join(test_obj.path_save, 'test.cfg.temp'))

    # if the config directory had to be made just for this test, remove it
    if not os.listdir(test_obj.path_save):
        os.removedirs(test_obj.path_save)
