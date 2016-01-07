import os

from tkinter import *
from CoverLetterExpress import filewalker
from CoverLetterExpress import utility
from CoverLetterExpress import question
from CoverLetterExpress.configurator import get_config as config

while True:
    utility.clear_screen()
    result = None

    li = []

    if os.path.exists(config().path_letters):
        li = filewalker.get_list(config().path_letters, '.txt')
    else:
        os.makedirs(config().path_letters)
    if not li:
        print("I couldn't find anything in this directory :(\n" +
              "'" + config().path_letters + "'\n")
        break

    if len(li) > 1:
        utility.list_options(li)

        result = question.handler(li, "Which cover letter do you want to use?",
                                  "None of these",
                                  "I couldn't find that letter...",
                                  "Your answer matched more than one " +
                                  "possible option:",
                                  )
    else:
        result = li[0]

    result = os.path.join(config().path_letters, result)

    with open(result, 'r') as f:
        fill = {}
        while True:
            fill['company'] = input("Enter company name: ")

            if not fill['company']:
                continue
            else:
                break

        fill['provide'] = input("Enter qualities this company provides:\n")
        fill['greeting'] = input("Enter greeting (leave blank to use " +
                                 config().greeting + "):\n")
        if not fill['greeting']:
            fill['greeting'] = config().greeting

        coverletter = f.read().format(**fill)
        f.close()

        tk = Tk()
        tk.withdraw()
        tk.clipboard_clear()
        tk.clipboard_append(coverletter)

        tk.update()
        tk.destroy()

    utility.clear_screen()
    result = question.handler(['Yes', 'No'],
                              "Formatted letter copied to clipboard... " +
                              "Do another letter?",
                              "", "Was that a yes or no?",
                              "",
                              )
    if result == 'No':
        break
