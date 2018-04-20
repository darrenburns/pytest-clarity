import pprint
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


class Hint(object):
    @staticmethod
    def forgot_eq():
        return _hint_text(
            'left and right are equal in data and in type: '
            'perhaps you forgot to implement __eq__ and __ne__?'
        )

    @staticmethod
    def different_lens(lhs, rhs):
        return _hint_text(
            'left and right differ in length: '
            'len(left) == {}, len(right) == {}'.format(len(lhs), len(rhs))
        )

    @staticmethod
    def different_types(lhs, rhs):
        return _hint_text(
            'left and right differ in type: '
            'type(left) == {}, type(right) == {}'.format(type(lhs), type(rhs))
        )

    @staticmethod
    def list_same_elems():
        return _hint_text(
            'left and right are lists with the same items, but in a different order: '
            'set(left) == set(right)'
        )

    @staticmethod
    def dict_same_keys():
        return _hint_text(
            'left and right are dicts with the same keys: '
            'set(left) == set(right)'
        )


_deleted_text = partial(colored, color=Color.red, on_color=BgColor.red, attrs=[Attr.bold])
_diff_intro_text = partial(colored, color=Color.cyan, attrs=[Attr.bold])
_inserted_text = partial(colored, color=Color.green, on_color=BgColor.green, attrs=[Attr.bold])


def _hint_text(text):
    return colored(u('  \u2022 ' + 'hint: ' + text), color=Color.cyan)


def _pformat_no_color(s, width):
    return pprint.pformat(s, width=width)
