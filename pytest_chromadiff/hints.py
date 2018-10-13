from collections import Sequence

from pytest_chromadiff.output import (
    BgColour,
    deleted_text,
    hint_body_text,
    hint_text,
    inserted_text,
)
from pytest_chromadiff.util import has_differing_len, pformat_no_color, possibly_missing_eq


def _different_types(lhs, rhs):
    return hint_text(
        "left and right have different types"
        "type(left) == {}, type(right) == {}".format(type(lhs), type(rhs))
    )


def hints_for(op, lhs, rhs):
    hints = [""]  # immediate newline

    if op == "==":

        if has_differing_len(lhs, rhs):
            hints += [
                hint_text("left and right have different lengths:"),
                hint_body_text("  len(left) == {}, len(right) == {}".format(len(lhs), len(rhs))),
            ]

        if possibly_missing_eq(lhs, rhs):
            hints += [
                hint_text("left and right are equal in data and in type: "),
                hint_body_text("perhaps you forgot to implement __eq__ and __ne__?"),
            ]

        both_sequences = isinstance(lhs, Sequence) and isinstance(rhs, Sequence)
        both_dicts = isinstance(lhs, dict) and isinstance(rhs, dict)

        if both_dicts:
            lhs, rhs = lhs.items(), rhs.items()

        if both_sequences or both_dicts:
            num_extras, lines = find_extras(lhs, rhs, inserted_text, BgColour.green, "+")
            hints += [hint_text("{} items in left, but not right:".format(num_extras))] + lines

            num_extras, lines = find_extras(rhs, lhs, deleted_text, BgColour.red, "-")
            hints += [hint_text("{} items in right, but not left:".format(num_extras))] + lines

    return hints


def find_extras(lhs, rhs, text_fn, gutter_colour, item_marker):
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
