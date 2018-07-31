import pprint
from collections import Sized, Iterable

import six
from six import text_type


def ecu(s):
    try:
        return text_type(s, 'utf-8', 'replace')
    except TypeError:
        return s


def display_op_for(pytest_op):
    return '==' if pytest_op == 'equal' else pytest_op


def has_overriden_repr(item):
    return type(item).__repr__ is not object.__repr__


def possibly_missing_eq(lhs, rhs):
    try:
        left_dict, right_dict = vars(lhs), vars(rhs)
    except TypeError:
        return False

    return all([
        isinstance(lhs, type(rhs)),
        lhs != rhs,
        left_dict == right_dict,
    ])


def has_differing_len(lhs, rhs):
    if isinstance(lhs, Sized) and isinstance(rhs, Sized):
        return len(lhs) != len(rhs)
    return False


def is_iterable(x):
    return isinstance(x, Iterable)


def pformat_no_color(s, width):
    if isinstance(s, six.string_types):
        return '"' + s + '"'
    return pprint.pformat(s, width=width)
