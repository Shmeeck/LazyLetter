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

test_path_save = "test_config"
test_cfg_name = "test.cfg"


def test_save_load():
    """
    Config should save all attributes and values into a json file and then
    be read back into the config object. Also, a failed load should return
    False.
    """
    test_obj = configurator.Config(path_letters="testletters",
                                   greeting="GLaDOS",
                                   path_save=test_path_save,
                                   current_filename=test_cfg_name,
                                   )
    result_obj = configurator.Config(path_save=test_path_save,
                                     current_filename=test_cfg_name,
                                     )

    test_obj.save()
    result_obj.load()

    assert_equals(result_obj.path_letters, test_obj.path_letters)
    assert_equals(result_obj.greeting, test_obj.greeting)

    # failed load testing
    sillyname = "testtestshouldntevereverexisteverneverever20198211029.cfpoop"
    test_obj = configurator.Config(current_filename=sillyname)
    assert_equals(test_obj.load(), False)


def test_remove_save():
    """
    after a Config() object is saved, remove_save() should be able to remove it
    and return True, otherwise, False
    """
    test_obj = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name)

    test_obj.save()
    assert_equals(test_obj.remove_save(), True)
    assert_equals(test_obj.remove_save(), False)


def test_rename_save():
    """
    rename_save() should be able to change the value of current_filename
    and alter the save file, should pass back the new name
    """
    test_obj = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name)

    test_obj.save()
    assert_equals(test_obj.rename_save(test_cfg_name+'2'), test_cfg_name+'2')
    assert_equals(test_obj.current_filename, test_cfg_name+'2')


def test_change_save():
    """
    change_save() should switch to the given filename.cfg and return said name,
    if the new filename does not exist, than return the old name that existed
    prior to the function call.
    """
    test_obj = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name+'3')
    dest_obj = configurator.Config(path_save=test_path_save,
                                   current_filename=test_cfg_name+'4')

    # return the old name
    test_obj.save()
    assert_equals(test_obj.change_save(test_cfg_name+'4'), test_cfg_name+'3')

    # return the new name because it's save file actually exists
    dest_obj.save()
    assert_equals(test_obj.change_save(test_cfg_name+'4'), test_cfg_name+'4')



def teardown():
    """
    clears out any files that stick around if the save_load test fails
    """
    test_obj = configurator.Config(path_save=test_path_save)

    filepath = os.path.join(test_obj.path_save, test_cfg_name)
    temppath = filepath + '.temp'

    if os.path.exists(test_obj.path_save):
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(temppath):
            os.remove(temppath)
        for i in range(2, 5):
            if os.path.exists(filepath+str(i)):
                os.remove(filepath+str(i))

        # if the config directory had to be made just for this test, remove it
        if not os.listdir(test_obj.path_save):
            os.removedirs(test_obj.path_save)
