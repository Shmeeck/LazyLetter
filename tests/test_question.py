from LazyLetter import question
from nose.tools import *


def test_list_options():
    """
    should accept a list of strings and return a specially formatted list of
    strings with inline 1-based enumeration, also accepts a prefix spacing int
    """
    test_list = ['Poopy', 'I Like Cake', 'test A Pie']
    result = question.list_options(test_list, 3)

    assert_equals(result[:4], '   [')
    assert_in('[1] Poopy', result)
    assert_in('[3] test A Pie', result)


def test_filter_each_letter():
    """
    should accept a list of strings and a letter and return a list consisting
    of only the items that match the letter, the matching option also omits 1
    instance of the letter

    input assumes all characters are lowercase and the first character being
    the original index since the result list the original positions
    """
    test_list = ['i like caake', 'Test Bakery',
                 'who put this here', 'WAFFLES',
                 '']
    result = question.filter_each_letter(test_list, 'a')

    assert_equals('i like caake', result[0])
    assert_equals('Test Bakery', result[1])
    assert_equals('WAFFLES', result[2])
    assert_equals(len(result), 3)

    result = question.filter_each_letter(test_list, 'WAFF')
    assert_equals('WAFFLES', result[0])

    result = question.filter_each_letter(test_list, 'who put this here')
    assert_equals('who put this here', result[0])

    result = question.filter_each_letter(test_list, 'el')
    assert_equals([], result)


def test_filter_entire_string():
    """
    when given a list and an answer as a string, it should return:
        1.  a list with only matches of the full answer
        2.  an empty list if there are no exact matches
        3.  one answer if the answer exactly, minus case, a list
            item
    * spaces count
    """
    test_list = ['I like stripes', 'Stripes are what I like',
                 'Stripes stripes stripes', 'Cake is greater than pie',
                 'I like pie', 'LIKE']
    # --- 1 ---
    assert_equals(question.filter_entire_string(test_list, 'sTrIpEs'),
                  [test_list[0], test_list[1], test_list[2],
                   ])
    assert_equals(question.filter_entire_string(test_list, 'sTRiPES stripES'),
                  [test_list[2]])

    # --- 2 ---
    assert_equals(question.filter_entire_string(test_list, 'Pie is greater'),
                  [])

    # --- 3 ---
    assert_equals(question.filter_entire_string(test_list, 'like'),
                  [test_list[5]])


def test_filter_index():
    """
    when given a list and an answer as an int()-able string, it should return:
        1.  A list with a single string of the matching result, the function
            should convert the user's 1-based response to a 0-based indexable
            one.
        2.  None if the answer is not an int
        3.  [] if the answer is out of bounds
    """
    test_list = ['Woah', 'There', 'Slow', 'Down!']

    # --- 1 ---
    assert_equals(question.filter_index(test_list, 2), [test_list[1]])

    # --- 2 ---
    assert_equals(question.filter_index(test_list, 'pie'), None)

    # --- 3 ---
    assert_equals(question.filter_index(test_list, -99), [])
    assert_equals(question.filter_index(test_list, 1029392), [])


def test_filter_all_timed():
    """
    when given a list of options and an answer (either an int or string), this
    should return:
        1.  an index int of the matching option for use in the original
            options list
        2.  [] if there are no matches
        3.  a list containing all matches, if there are multiple matches
        4.  a list containing matched case results if there are multiple
            matches and a full case match can be found
        5.  a list containing one match if the answer exactly matches a
            list option (exactly doesn't include case)

    case should not be a factor
    """

    test_list = ['Generate Cover Letter', 'Settings', 'Exit', 'Eat Something',
                 'Save and Exit']

    # --- 1 ---
    assert_equals(question.filter_all_timed(test_list, 'gENe'), [test_list[0]])
    assert_equals(question.filter_all_timed(test_list, '2'), [test_list[1]])

    # --- 2 ---
    assert_equals(question.filter_all_timed(test_list, 'setq'), [])
    assert_equals(question.filter_all_timed(test_list, '6'), [])

    # --- 3 ---
    assert_equals(question.filter_all_timed(test_list, 'I'), [test_list[1],
                                                              test_list[2],
                                                              test_list[3],
                                                              test_list[4]
                                                              ])

    # --- 4 ---
    assert_equals(question.filter_all_timed(test_list, 'EAT'), [test_list[3]])

    # --- 5 ---
    assert_equals(question.filter_all_timed(test_list, 'exit'), [test_list[2]])
