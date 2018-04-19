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
    return pprint.pformat(s, width=width)


def _splitlines_colored(s):
    """
    :param s: a string to split into a list on the \n characters
    :return: a list of strings, that retains terminal codes between lines
    """
    lines = s.splitlines()
    if len(lines) < 2:
        return lines

    output = []
    output.append(lines[0])
    for i, line in enumerate(lines):
        if i == 0:
            continue

        # attach everything that comes beyond the leftmost terminal code which isnt followed by a stopcode
        prev_l = lines[i - 1]
        rstop_idx = prev_l.rfind(Color.stop)

        print('prev_l: {}'.format(repr(lines[i-1])))
        print('rstop_idx: {}'.format(rstop_idx))

        # collapse a window around the largest sequence of terminal codes
        prev_term_code = prev_l[0 if rstop_idx == -1 else rstop_idx:]
        prev_term_code = prev_term_code[prev_term_code.find('\033['):]
        prev_term_code = prev_term_code[:prev_term_code.rfind('[') + 3]

        print('prev_term_code: {}'.format(repr(prev_term_code)))
        print('line: {}'.format(repr(line)))

        # if the terminal code doesnt reset attributes, check what the code is and re-apply it
        output.append(prev_term_code + line)


    return output


def _build_split_diff(lhs, rhs):
    width = 60
    lhs_repr, rhs_repr = lhs, rhs
    if not isinstance(lhs, six.string_types) and not isinstance(rhs, six.string_types):
        if len(repr(lhs)) > width or len(repr(rhs)) > width:
            lhs_repr, rhs_repr = _pformat_no_color(lhs, 1), _pformat_no_color(rhs, 1)
        else:
            lhs_repr, rhs_repr = repr(lhs), repr(rhs)

    lhs_out, rhs_out = Color.stop, Color.stop

    matcher = difflib.SequenceMatcher(None, lhs_repr, rhs_repr)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():

        lhs_substring_lines = lhs_repr[i1:i2].splitlines()
        rhs_substring_lines = rhs_repr[j1:j2].splitlines()

        for i, lhs_substring in enumerate(lhs_substring_lines):
            if op == 'replace':
                lhs_out += _deleted_text(lhs_substring)
            elif op == 'delete':
                lhs_out += _deleted_text(lhs_substring)
            elif op == 'insert':
                lhs_out += Color.stop + lhs_substring
            elif op == 'equal':
                lhs_out += Color.stop + lhs_substring

            if i != len(lhs_substring_lines) - 1:
                lhs_out += '\n'

        for j, rhs_substring in enumerate(rhs_substring_lines):
            if op == 'replace':
                rhs_out += _inserted_text(rhs_substring)
            elif op == 'insert':
                rhs_out += _inserted_text(rhs_substring)
            elif op == 'equal':
                rhs_out += Color.stop + rhs_substring

            if j != len(rhs_substring_lines) - 1:
                rhs_out += '\n'

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

            lhs_auto_repr_diff, rhs_auto_repr_diff = _build_split_diff(
                lhs_auto_repr, rhs_auto_repr)

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


def pytest_addoption(parser):
    parser.addoption(
        '--no-hints',
        action='store_true',
        default=False,
        help='disable pytest-betterdiff hints (boolean)',
    )


def pytest_assertrepr_compare(config, op, left, right):
    display_op = _display_op_for(op)

    lhs_diff, rhs_diff = _build_split_diff(left, right)

    print(rhs_diff)

    output = [u('left {} right failed, where: ').format(display_op), '']

    if lhs_diff and rhs_diff:
        lhs_diff[0] = Color.stop + _diff_intro_text('left:  ') + lhs_diff[0]
        rhs_diff[0] = Color.stop + _diff_intro_text('right: ') + rhs_diff[0]

    output += lhs_diff + rhs_diff

    if not config.getoption('--no-hints'):
        output += _hints_for(op, left, right)

    return output
