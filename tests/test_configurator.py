import os

from LazyLetter import configurator
from io import StringIO
from nose.tools import *


def test_Config():
    """
    default_path method should return:
        1.  just the parent directory if 'path' is none
        2.  a subdirectory of parent named with 'path' if it's a string
        3.  'path' if it is a os.path string
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
        1.  a dict containing the key path_save should save its value into the
            object's attribute with the same name.
        2.  a dict containing a key that's not an attribute should receive a
            debug output
        3.  both 1 and 2 combined should still work as the method should just
            omit 2's input
    """
    test_obj = configurator.Config()

    # --- 1 ---
    test_dict = {'path_save': os.path.abspath(configurator.__file__)}
    test_obj.load_dict(test_dict)
    assert_equals(test_obj.path_save, test_dict['path_save'])

    # --- 2 ---
    resultout = StringIO()
    test_dict2 = {'shouldntexist': "butts"}

    test_obj.debugout = resultout
    test_obj.load_dict(test_dict2)
    result = resultout.getvalue()

    assert_in('debug', result.lower())

    # --- 3 ---
    test_obj = configurator.Config()  # reset the object
    resultout = StringIO()
    test_obj.debugout = resultout

    test_dict = {**test_dict, **test_dict2}
    test_obj.load_dict(test_dict)
    result = resultout.getvalue()

    assert_equals(test_obj.path_save, test_dict['path_save'])
    assert_in('debug', result.lower())

    resultout.close()


def test_save_load():
    """
    Config should save all attributes and values into a json file and then
    be read back into the config object
    """
    test_obj = configurator.Config(path_letters="testletters",
                                   greeting="GLaDOS",
                                   )
    test_obj.save('test.config')
    test_obj = configurator.Config()
    test_obj.load('test.config')

    assert_equals(test_obj.path_letters, "testletters")
    assert_equals(test_obj.greeting, "GLaDOS")

    os.remove(os.path.join(test_obj.path_save, test.config))
