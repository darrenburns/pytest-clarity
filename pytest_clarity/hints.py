from collections import Sequence

from pytest_clarity.output import deleted_text, hint_body_text, hint_text, inserted_text
from pytest_clarity.util import (
    direct_type_mismatch,
    has_differing_len,
    pformat_no_color,
    possibly_missing_eq,
)


def hints_for(op, lhs, rhs):
    hints = [""]  # immediate newline

    if op == "==":

        if direct_type_mismatch(lhs, rhs):
            lhs_type, rhs_type = inserted_text(type(lhs)), deleted_text(type(rhs))
            hints += [
                hint_text("left and right are different types:"),
                hint_body_text(
                    "  type(left) is {}, type(right) is {}".format(lhs_type, rhs_type)
                ),
            ]

        if has_differing_len(lhs, rhs):
            lhs_len, rhs_len = inserted_text(len(lhs)), deleted_text(len(rhs))
            hints += [
                hint_text("left and right have different lengths:"),
                hint_body_text(
                    "  len(left) == {}, len(right) == {}".format(lhs_len, rhs_len)
                ),
            ]

        if possibly_missing_eq(lhs, rhs):
            hints += [
                hint_text("left and right are equal in data and in type: "),
                hint_body_text("  perhaps you forgot to implement __eq__ and __ne__?"),
            ]

        both_sequences = isinstance(lhs, Sequence) and isinstance(rhs, Sequence)
        both_dicts = isinstance(lhs, dict) and isinstance(rhs, dict)

        if both_dicts:
            lhs, rhs = lhs.items(), rhs.items()

        if both_sequences or both_dicts:
            num_extras, lines = find_extras(lhs, rhs, inserted_text, "+")
            hints += [
                         hint_text("{} items in left, but not right:".format(num_extras))
                     ] + lines

            num_extras, lines = find_extras(rhs, lhs, deleted_text, "-")
            hints += [
                         hint_text("{} items in right, but not left:".format(num_extras))
                     ] + lines

    return hints


def find_extras(lhs, rhs, text_fn, item_marker):
    lhs_extras_lines = []
    num_extras = 0
    for item in lhs:
        if item not in rhs:
            num_extras += 1
            for i, line in enumerate(pformat_no_color(item, 80).splitlines()):
                gutter_content = item_marker if i == 0 else " "
                coloured_line = "{gutter_content}{spacing}{line}".format(
                    gutter_content=text_fn(gutter_content),
                    spacing=" ",
                    line=text_fn(line),
                )
                lhs_extras_lines.append(coloured_line)

    return num_extras, lhs_extras_lines
