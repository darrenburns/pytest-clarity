from functools import partial

from six import u
from termcolor import colored


class Color(object):
    red = 'red'
    green = 'green'
    cyan = 'cyan'
    yellow = 'yellow'
    stop = '\033[0m'


class BgColor(object):
    red = 'on_red'
    green = 'on_green'


class Attr(object):
    bold = 'bold'


deleted_text = partial(colored, color=Color.red, attrs=[Attr.bold])
diff_intro_text = partial(colored, color=Color.cyan, attrs=[Attr.bold])
inserted_text = partial(colored, color=Color.green, attrs=[Attr.bold])


def _hint_text(text):
    return colored(u('  \u2022 ' + 'hint: ' + text), color=Color.cyan)
