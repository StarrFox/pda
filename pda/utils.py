import sys
from pathlib import Path
from operator import itemgetter

import appdirs


# program name
PROG_NAME = "pda"

# priority symbolic constants
URGENT_MUSTDO = 5
MUSTDO = 4
HIGH_IMPORTANCE = 3
MEDIUM_IMPORTANCE = 2
LOW_IMPORTANCE = 1


def get_data_dir() -> Path:
    """
    Get the pda data dir
    """
    app_name = "pda"
    app_author = "StarrFox"
    cache_dir = Path(appdirs.user_data_dir(app_name, app_author))

    cache_dir.mkdir(parents=True, exist_ok=True)

    return cache_dir


# TODO: 3.10 switch to match-case
def convert_prio_int_to_txt(priority):
    """map integer priority to its text equivalent
    :param priority: integer
    :rtype: string
    """

    # dictionary-based 'switch' statement
    # None is default if priority is not found
    return (
        {
            URGENT_MUSTDO: "urgmust",
            MUSTDO: "must",
            HIGH_IMPORTANCE: "high",
            MEDIUM_IMPORTANCE: "medium",
            LOW_IMPORTANCE: "low",
        }.get(priority, None)
        if priority
        else None
    )


# TODO: 3.10 switch to match-case
def ord_prio(prio):
    """Compute the ordinal number of a text priority
    :param prio: string
    :rtype: integer
    """

    return {"urgmust": 1, "must": 2, "high": 3, "medium": 4, "low": 5}.get(prio, 5)


# TODO: 3.10 switch to match-case
def ord_time(time):
    """Compute the ordinal number of a text milestone
    :param time: string
    :rtype: integer
    """

    return {"day": 1, "week": 2, "month": 3, "season": 4, "year": 5}.get(time, 5)


def sorted_tasks(shelf):
    """Sort tasks stored locally and return the sorted list
    :param shelf: :class: `shelve <shelve>` object
    :rtype: a list of strings
    """

    # create a list of tuples which will be used for sorting
    task_tuples = [
        (
            int(key),
            ord_time(shelf[key]["milestone"]),
            ord_prio(shelf[key]["priority"]),
            shelf[key]["type"],
        )
        for key in shelf
        if key != "CMDS_HISTORY"
    ]

    # multiple levels of sorting based on the milestone (2nd element),
    # then priority (3rd element), then alphabetical order of list types
    # (4th element), and finally by task number (1st element) in the tuples
    sorted_tuples = sorted(task_tuples, key=itemgetter(1, 2, 0))

    # return a list of sorted task numbers
    return [str(tup[0]) for tup in sorted_tuples]


def print_header():
    """Print pretty header of list content

    The head contains 5 columns, each column has a differnt string length.
    """
    print(f"\n{'TASK#':<5}  {'SUMMARY':<60}  {'LIST TYPE':<9}  {'DUE TIME':<8}  {'PRIORITY':<8}")
    print(f"{'':=<5}  {'':=<60}  {'':=<9}  {'':=<8}  {'':=<8}")


def cry_msg(prog, err_str="", msg=""):
    """Emit error messages for pda
    :param prog:    string
    :param err_str: string
    :param msg:     string
    """
    print("{0}: {1}{2}".format(prog, err_str, msg))


def die_msg(prog, msg=""):
    """Crash pda with an error message -> used for more fatal errors
    :param prog:    string
    :param msg:     string
    """

    print("{0}: error: {1}".format(prog, msg))
    sys.exit(1)
