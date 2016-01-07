from . import search
from .receive import user_input

msg_multiple = "Your answer matched more than one possible option:"
msg_noresult = "Sorry, couldn't understand that..."
option_redo = "None of These"


def down_to_one(li, question):
    """
    Accepts a list of options and a question to display to the user, an
    enumerated version of the list is always displayed after the question,
    the function will continuously filter the user's answer and the list
    until the following is satisfied:
        1. The result is not blank
        2. There is only a single result

    If there are multiple options in the result after filtering, a
    recursive call is made with the remaining options only if the
    options were narrowed since the last recurse, otherwise, continue.
    An option to leave the narrowed listings is made available in this
    stage of filtering.
    """
    result = []

    while True:
        result = li

        answer = user_input().get(result, question)
        result = search.everything(result, answer)

        if not result or not answer:
            print(msg_noresult)
            continue
        elif len(result) > 1:
            # add the ability to display the whole list again
            if not li[len(li)-1] == option_redo:
                result.append(option_redo)
            elif result == li[:len(li)-1]:
                continue

            # let's go again with only the remaining options
            result = down_to_one(result, msg_multiple)

        if result == option_redo:
            # we gotta go back to the start of the stack...
            if not li[len(li)-1] == option_redo:
                continue

        break

    return result[0]
