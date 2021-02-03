import sys


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
            sys.stdout.write("Please only respond with 'kill' or 'shutdown'\n"
                             "If you want do keep it running you don't have to do anything\n")