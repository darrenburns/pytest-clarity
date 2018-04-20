# -*- coding: utf-8 -*-
from pytest_betterdiff.diff import build_split_diff
from pytest_betterdiff.terminal import Color, Hint, _diff_intro_text, _hint_text
from pytest_betterdiff.util import has_overriden_repr, _possibly_missing_eq, _has_differing_len, _is_iterable, auto_repr


def _hints_for(op, lhs, rhs):
    hints = ['']

    if op == '==':
        if _has_differing_len(lhs, rhs):
            hints.append(Hint.different_lens(lhs, rhs))
        if _possibly_missing_eq(lhs, rhs):
            hints.append(Hint.forgot_eq())
        if not has_overriden_repr(lhs) and not has_overriden_repr(rhs):
            lhs_auto_repr, rhs_auto_repr = auto_repr(lhs), auto_repr(rhs)

            lhs_auto_repr_diff, rhs_auto_repr_diff = build_split_diff(
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
