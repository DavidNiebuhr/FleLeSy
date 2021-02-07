import sys


def query_yes_no(question):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [y/n] "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def query_alias(question):
    prompt = "\nEnter your alias: "

    while True:
        choice = None
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        sys.stdout.write("\nAlright alias is now %s" % choice)
        if choice is not None:
            return choice


def query_number(question, min_value, max_value):
    prompt = " Enter one of the shown numbers.\n"
    while True:
        sys.stdout.write(question + prompt)
        choice = int(raw_input())
        if min_value <= choice < max_value:
            return choice
        else:
            sys.stdout.write("Invalid!")


def query_kill(question):
    valid = {"kill": True, "k": True, "killl": True,
             "shutdown": True}
    prompt = " If yes write 'kill' "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\nPlease only respond with 'kill' or 'shutdown'\n"
                             "If you want do keep it running you don't have to do anything\n")
