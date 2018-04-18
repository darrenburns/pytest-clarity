# -*- coding: utf-8 -*-

import difflib
import pprint
from collections import Sized, Iterable
from functools import partial

import six
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
            'left and right contain the same items, but in a different order: '
            'set(left) == set(right)'
        )

    @staticmethod
    def dict_same_keys():
        return _hint_text(
            'left and right have the same keys: '
            'set(left) == set(right)'
        )

    @staticmethod
    def auto_repr(item):
        output = type(item).__name__ + '('
        variables = vars(item).items()

        for i, var in enumerate(variables):
            output += var[0] + '=' + repr(var[1])
            if i != len(variables) - 1:
                output += ', '

        return output + ')'


_deleted_text = partial(colored, color=Color.red, on_color=BgColor.red, attrs=[Attr.bold])
_diff_intro_text = partial(colored, color=Color.cyan, attrs=[Attr.bold])
_inserted_text = partial(colored, color=Color.green, on_color=BgColor.green, attrs=[Attr.bold])


def _hint_text(text):
    return colored(u('  \u2022 ' + 'hint: ' + text), color=Color.cyan)


def _pformat_no_color(s, width):
    return pprint.pformat(s, width=width).replace('\n', '\n' + Color.stop)


def _build_diff(lhs, rhs):
    width = 60

    lhs_repr, rhs_repr = lhs, rhs
    if not isinstance(lhs, six.string_types):
        lhs_repr = _pformat_no_color(lhs, width)
    if not isinstance(rhs, six.string_types):
        rhs_repr = _pformat_no_color(rhs, width)

    lhs_out, rhs_out = Color.stop, Color.stop

    matcher = difflib.SequenceMatcher(None, lhs_repr, rhs_repr)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        lhs_substring = lhs_repr[i1:i2]
        rhs_substring = rhs_repr[j1:j2]

        if op == 'replace':
            lhs_out += _deleted_text(lhs_substring)
            rhs_out += _inserted_text(rhs_substring)
        elif op == 'delete':
            lhs_out += _deleted_text(lhs_substring)
        elif op == 'insert':
            lhs_out += lhs_substring
            rhs_out += _inserted_text(rhs_substring)
        elif op == 'equal':
            lhs_out += lhs_substring
            rhs_out += rhs_substring

    return lhs_out.splitlines(), rhs_out.splitlines()


def _possibly_missing_eq(lhs, rhs):
    try:
        left_dict, right_dict = lhs.__dict__, rhs.__dict__
    except AttributeError:
        return False

    return all([
        isinstance(lhs, type(rhs)),
        lhs != rhs,
        left_dict == right_dict,
    ])


def _has_differing_len(lhs, rhs):
    if isinstance(lhs, Sized) and isinstance(rhs, Sized):
        return len(lhs) != len(rhs)
    return False


def _is_iterable(x):
    return isinstance(x, Iterable)


def _has_default_repr(item):
    return type(item).__repr__ is object.__repr__


def _hints_for(op, lhs, rhs):
    hints = ['']

    if op == '==':
        if _has_differing_len(lhs, rhs):
            hints.append(Hint.different_lens(lhs, rhs))
        if _possibly_missing_eq(lhs, rhs):
            hints.append(Hint.forgot_eq())
        if _has_default_repr(lhs) and _has_default_repr(rhs):
            lhs_auto_repr, rhs_auto_repr = Hint.auto_repr(lhs), Hint.auto_repr(rhs)

            lhs_auto_repr_diff, rhs_auto_repr_diff = _build_diff(lhs_auto_repr, rhs_auto_repr)

            hints.append(_hint_text('No __repr__ found, showing attribute value diff: '))

            if lhs_auto_repr_diff and rhs_auto_repr_diff:
                lhs_auto_repr_diff[0] = Color.stop + \
                    _diff_intro_text(' ' * 4 + 'left attrs:  ') + lhs_auto_repr_diff[0]
                rhs_auto_repr_diff[0] = Color.stop + \
                    _diff_intro_text(' ' * 4 + 'right attrs: ') + rhs_auto_repr_diff[0]

            hints.extend(lhs_auto_repr_diff)
            hints.extend(rhs_auto_repr_diff)

        if _is_iterable(lhs) and _is_iterable(rhs):
            lhs_set, rhs_set = set(lhs), set(rhs)
            if isinstance(lhs, dict) and isinstance(rhs, dict):
                if lhs_set == rhs_set:
                    hints.append(Hint.dict_same_keys())
            if isinstance(lhs, list) and isinstance(rhs, list):
                if lhs_set == rhs_set:
                    hints.append(Hint.list_same_elems())

    return hints


def _display_op_for(pytest_op):
    return '==' if pytest_op == 'equal' else pytest_op


def pytest_assertrepr_compare(config, op, left, right):
    display_op = _display_op_for(op)

    verbose = config.getoption('verbose')

    lhs_diff, rhs_diff = _build_diff(left, right)
    output = [u('left {} right failed, where: ').format(display_op), '']

    if lhs_diff and rhs_diff:
        lhs_diff[0] = Color.stop + _diff_intro_text('left:  ') + lhs_diff[0]
        rhs_diff[0] = Color.stop + _diff_intro_text('right: ') + rhs_diff[0]

    output += lhs_diff + rhs_diff

    # TODO create a config option to enable/disable hints
    if verbose:
        output += _hints_for(op, left, right)

    return output
