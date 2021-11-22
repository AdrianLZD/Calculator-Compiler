
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[33m"
RESET = "\033[37m"

def error(msg):
    print(RED + msg + RESET)


def error_prefix(prefix, msg):
    print(RED + prefix + RESET + msg)


def info(msg):
    print(BLUE + msg + RESET)


def info_prefix(prefix, msg):
    print(BLUE + prefix + RESET + msg)


def success(msg):
    print(GREEN + msg + RESET)


def success_prefix(prefix, msg):
    print(GREEN + prefix + RESET + msg)
