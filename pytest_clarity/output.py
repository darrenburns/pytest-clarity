from functools import partial

from termcolor import colored


class Colour(object):
    red = "red"
    green = "green"
    cyan = "cyan"
    yellow = "yellow"
    stop = "\033[0m"


class BgColour(object):
    red = "on_red"
    green = "on_green"


class Attr(object):
    bold = "bold"


deleted_text = partial(colored, color=Colour.red, attrs=[Attr.bold])
diff_intro_text = partial(colored, color=Colour.cyan, attrs=[Attr.bold])
inserted_text = partial(colored, color=Colour.green, attrs=[Attr.bold])
header_text = partial(colored, color=Colour.yellow, attrs=[Attr.bold])


def non_formatted(text):
    return Colour.stop + text


def hint_text(text):
    bold_cyan = colored(text, color=Colour.cyan, attrs=[Attr.bold])
    return bold_cyan


def hint_body_text(text):
    bold_red = colored(Colour.stop + text, color=Colour.red, attrs=[Attr.bold])
    return bold_red
