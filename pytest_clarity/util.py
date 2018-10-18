import pprint

import six
from six import text_type


def utf8_replace(s):
    try:
        return text_type(s, "utf-8", "replace")
    except TypeError:
        return s


def direct_type_mismatch(lhs, rhs):
    return type(lhs) is not type(rhs)


def display_op_for(pytest_op):
    return "==" if pytest_op == "equal" else pytest_op


def possibly_missing_eq(lhs, rhs):
    try:
        left_dict, right_dict = vars(lhs), vars(rhs)
        return (type(lhs) is type(rhs)) and lhs != rhs and left_dict == right_dict
    except TypeError:
        return False


def has_differing_len(lhs, rhs):
    try:
        return len(lhs) != len(rhs)
    except TypeError:
        return False


def pformat_no_color(s, width):
    if isinstance(s, six.string_types):
        return '"' + s + '"'
    return pprint.pformat(s, width=width)
