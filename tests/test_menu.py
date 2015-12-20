from LazyLetter import menu
from nose.tools import *


def test__list_options():
    """
    should accept a list of strings and return a specially formatted list of
    strings with inline 1-based enumeration, also accepts a prefix spacing int
    """
    test_list = ['Poopy', 'I Like Cake', 'test A Pie']
    result = menu._list_options(test_list, 3)

    assert_equals(result[:4], '   [')
    assert_in('[1] Poopy', result)
    assert_in('[3] test A Pie', result)


def test__filter_options():
    """
    should accept a list of strings and a letter and return a list consisting
    of only the items that match the letter, the matching option also omits 1
    instance of the letter

    input assumes all characters are lowercase and the first character being
    the original index since the result list the original positions
    """
    test_list = ['0i like caake', '1test bakery',
                 '2who put this here', '3waffles',
                 '4']
    result = menu._filter_options(test_list, 'a')

    assert_equals('0i like cake', result[0])
    assert_equals('1test bkery', result[1])
    assert_equals('3wffles', result[2])
    assert_equals(len(result), 3)


def test__parse_options():
    """
    when given a list of options and an answer (either an int or string), this
    should return:
        1.  an index int of the matching option for use in the original
            options list
        2.  -1 if there are no matches
        3.  -2 if there are multiple matches

    case should not be a factor
    """
    test_list = ['Generate Cover Letter', 'Settings', 'Exit']

    # --- 1 ---
    assert_equals(menu._parse_options(test_list, 'eXiT'), 2)
    assert_equals(menu._parse_options(test_list, '2'), 1)

    # --- 2 ---
    assert_equals(menu._parse_options(test_list, 'setq'), -1)
    assert_equals(menu._parse_options(test_list, '4'), -1)

    # --- 3 ---
    assert_equals(menu._parse_options(test_list, 'I'), -2)
