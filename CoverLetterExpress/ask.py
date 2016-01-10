def list_options(ls, pre_spaces):
    result = ""
    for i, option in enumerate(ls):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option

        if not i == len(ls)-1:
            result += '\n'

    return result


def question(ls, question, pre_spaces=4, question_first=True):
    if question_first:
        print(question)

    print(list_options(ls, pre_spaces))

    if not question_first:
        print(question)
