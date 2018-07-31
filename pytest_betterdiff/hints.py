from pytest_betterdiff.terminal import _hint_text
from pytest_betterdiff.util import (
    has_overriden_repr,
    possibly_missing_eq,
    has_differing_len,
    is_iterable,
    ecu,
)


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


def _hints_for(op, lhs, rhs):
    hints = ['']

    if op == '==':
        if has_differing_len(lhs, rhs):
            hints.append(Hint.different_lens(lhs, rhs))
        if possibly_missing_eq(lhs, rhs):
            hints.append(Hint.forgot_eq())
        if not has_overriden_repr(lhs) and not has_overriden_repr(rhs):
            hints.append(ecu(_hint_text('No __repr__ found, showing attribute value diff: ')))
        if is_iterable(lhs) and is_iterable(rhs):
            lhs_set, rhs_set = set(lhs), set(rhs)
            if isinstance(lhs, dict) and isinstance(rhs, dict):
                if lhs_set == rhs_set:
                    hints.append(Hint.dict_same_keys())
            if isinstance(lhs, list) and isinstance(rhs, list):
                if lhs_set == rhs_set:
                    hints.append(Hint.list_same_elems())

    return hints
