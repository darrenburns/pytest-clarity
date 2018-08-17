import difflib

from pytest_chromadiff.terminal import Color, deleted_text, inserted_text
from pytest_chromadiff.util import pformat_no_color


def build_split_diff(lhs, rhs):
    width = 60

    lhs_repr, rhs_repr = pformat_no_color(lhs, width), pformat_no_color(rhs, width)

    print(lhs_repr, rhs_repr)
    lhs_out, rhs_out = '', ''

    matcher = difflib.SequenceMatcher(None, lhs_repr, rhs_repr)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():

        lhs_substring_lines = lhs_repr[i1:i2].splitlines()
        rhs_substring_lines = rhs_repr[j1:j2].splitlines()

        for i, lhs_substring in enumerate(lhs_substring_lines):
            print(lhs_substring)
            if op == 'replace':
                lhs_out += deleted_text(lhs_substring)
            elif op == 'delete':
                lhs_out += deleted_text(lhs_substring)
            elif op == 'insert':
                lhs_out += Color.stop + lhs_substring
            elif op == 'equal':
                lhs_out += Color.stop + lhs_substring

            if i != len(lhs_substring_lines) - 1:
                lhs_out += '\n'

        for j, rhs_substring in enumerate(rhs_substring_lines):
            print(rhs_substring)
            if op == 'replace':
                rhs_out += inserted_text(rhs_substring)
            elif op == 'insert':
                rhs_out += inserted_text(rhs_substring)
            elif op == 'equal':
                rhs_out += Color.stop + rhs_substring

            if j != len(rhs_substring_lines) - 1:
                rhs_out += '\n'

    return lhs_out.splitlines(), rhs_out.splitlines()
