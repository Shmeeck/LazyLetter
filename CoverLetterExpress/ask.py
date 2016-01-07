def list_options(ls, options=None, pre_spaces=4):
    result = ""
    for i, option in enumerate(ls):
        result += ' '*pre_spaces + '[' + str(i+1) + '] ' + option

        if not i == len(ls)-1:
            result += '\n'

    return result
