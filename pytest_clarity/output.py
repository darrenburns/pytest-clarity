import os
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

def _colored(text, color, attrs):
    if 'NO_COLOR' in os.environ:
        return text
    return colored(text, color=color, attrs=attrs)
    
deleted_text = partial(_colored, color=Colour.red, attrs=[Attr.bold])
diff_intro_text = partial(_colored, color=Colour.cyan, attrs=[Attr.bold])
inserted_text = partial(_colored, color=Colour.green, attrs=[Attr.bold])
header_text = partial(_colored, color=Colour.yellow, attrs=[Attr.bold])
hint_text = partial(_colored, color=Colour.cyan, attrs=[Attr.bold])
non_formatted = partial(_colored, color=Colour.stop)

def hint_body_text(text):
    bold_red = _colored(Colour.stop + text, color=Colour.red, attrs=[Attr.bold])
    return bold_red




