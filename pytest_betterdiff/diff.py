import difflib

from pytest_betterdiff.terminal import Color, _deleted_text, _inserted_text, _pformat_no_color
from pytest_betterdiff.util import ecu, auto_repr


def build_split_diff(lhs, rhs):
    width = 60

    if len(repr(lhs)) > width or len(repr(rhs)) > width:
        lhs_repr, rhs_repr = _pformat_no_color(lhs, 1), _pformat_no_color(rhs, 1)
    else:
        lhs_repr, rhs_repr = auto_repr(lhs), auto_repr(rhs)

    lhs_out, rhs_out = ecu(Color.stop), ecu(Color.stop)

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
