from pytest_chromadiff.terminal import _hint_text
from pytest_chromadiff.util import (
    possibly_missing_eq,
    has_differing_len,
    is_iterable,
)


def _forgot_eq():
    return _hint_text(
        'left and right are equal in data and in type: '
        'perhaps you forgot to implement __eq__ and __ne__?'
    )


def _different_lens(lhs, rhs):
    return _hint_text(
        'left and right have different lengths'
        'len(left) == {}, len(right) == {}'.format(len(lhs), len(rhs))
    )


def _different_types(lhs, rhs):
    return _hint_text(
        'left and right have different types'
        'type(left) == {}, type(right) == {}'.format(type(lhs), type(rhs))
    )


def _list_same_elems():
    return _hint_text(
        'left and right are lists with the same items, but in a different order: '
        'set(left) == set(right)'
    )


def _dict_same_keys():
    return _hint_text(
        'left and right are dicts with the same keys'
        'set(left) == set(right)'
    )


def hints_for(op, lhs, rhs):
    hints = ['']

    if op == '==':
        if has_differing_len(lhs, rhs):
            hints.append(_different_lens(lhs, rhs))
        if possibly_missing_eq(lhs, rhs):
            hints.append(_forgot_eq())
        if is_iterable(lhs) and is_iterable(rhs):
            lhs_set, rhs_set = set(lhs), set(rhs)
            if isinstance(lhs, dict) and isinstance(rhs, dict):
                if lhs_set == rhs_set:
                    hints.append(_dict_same_keys())
            if isinstance(lhs, list) and isinstance(rhs, list):
                if lhs_set == rhs_set:
                    hints.append(_list_same_elems())

    return hints
