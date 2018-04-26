from pytest_betterdiff.diff import build_split_diff
from pytest_betterdiff.terminal import Color, Hint, _diff_intro_text, _hint_text
from pytest_betterdiff.util import (
    has_overriden_repr,
    possibly_missing_eq,
    has_differing_len,
    is_iterable,
    auto_repr,
    ecu,
)


def _hints_for(op, lhs, rhs):
    hints = ['']

    if op == '==':
        if has_differing_len(lhs, rhs):
            hints.append(Hint.different_lens(lhs, rhs))
        if possibly_missing_eq(lhs, rhs):
            hints.append(Hint.forgot_eq())
        if not has_overriden_repr(lhs) and not has_overriden_repr(rhs):
            lhs_auto_repr, rhs_auto_repr = ecu(auto_repr(lhs)), ecu(auto_repr(rhs))

            lhs_auto_repr_diff, rhs_auto_repr_diff = build_split_diff(
                lhs_auto_repr, rhs_auto_repr
            )

            hints.append(ecu(_hint_text('No __repr__ found, showing attribute value diff: ')))

            if lhs_auto_repr_diff and rhs_auto_repr_diff:
                lhs_auto_repr_diff[0] = Color.stop + \
                    _diff_intro_text(' ' * 4 + 'left attrs:  ') + lhs_auto_repr_diff[0]
                rhs_auto_repr_diff[0] = Color.stop + \
                    _diff_intro_text(' ' * 4 + 'right attrs: ') + rhs_auto_repr_diff[0]

            hints.extend([ecu(l) for l in lhs_auto_repr_diff])
            hints.extend([ecu(l) for l in rhs_auto_repr_diff])

        if is_iterable(lhs) and is_iterable(rhs):
            lhs_set, rhs_set = set(lhs), set(rhs)
            if isinstance(lhs, dict) and isinstance(rhs, dict):
                if lhs_set == rhs_set:
                    hints.append(Hint.dict_same_keys())
            if isinstance(lhs, list) and isinstance(rhs, list):
                if lhs_set == rhs_set:
                    hints.append(Hint.list_same_elems())

    return hints
