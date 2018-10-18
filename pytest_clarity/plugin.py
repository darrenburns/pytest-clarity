import sys

from pytest_clarity.diff import build_split_diff, build_unified_diff
from pytest_clarity.hints import hints_for
from pytest_clarity.output import Colour, deleted_text, diff_intro_text, inserted_text
from pytest_clarity.util import display_op_for, pformat_no_color, utf8_replace


def pytest_load_initial_conftests(args):
    # Force verbose logging to prevent pytest truncating output
    if "pytest_clarity" in sys.modules:
        args[:] = ["-vv"] + args


def pytest_addoption(parser):
    parser.addoption(
        "--no-hints",
        action="store_true",
        default=False,
        help="pytest-clarity: disable hints (boolean)",
    )

    parser.addoption(
        "--diff-width",
        action="store",
        default="80",
        help="pytest-clarity: configure output width",
    )

    parser.addoption(
        "--diff-type",
        action="store",
        default="auto",
        help="pytest-clarity: default auto. one of [auto, unified, split]",
    )


def pytest_assertrepr_compare(config, op, left, right):
    op = display_op_for(op)

    width = int(config.getoption("--diff-width"))
    diff_type = config.getoption("--diff-type")

    lhs_repr = pformat_no_color(utf8_replace(left), width)
    rhs_repr = pformat_no_color(utf8_replace(right), width)

    if diff_type == "split":
        output = build_full_splitdiff_output(lhs_repr, rhs_repr, op)
    elif diff_type == "unified":
        output = build_full_unidiff_output(lhs_repr, rhs_repr, op)
    else:  # assume diff_type == "auto" so decide based on newlines
        if "\n" in lhs_repr and "\n" in rhs_repr:
            output = build_full_unidiff_output(lhs_repr, rhs_repr, op)
        else:
            output = build_full_splitdiff_output(lhs_repr, rhs_repr, op)

    if not config.getoption("--no-hints"):
        output += hints_for(op, left, right)

    return [utf8_replace(line) for line in output]


def build_full_unidiff_output(lhs_repr, rhs_repr, op):
    left_key = inserted_text("L=left")
    right_key = deleted_text("R=right")
    return [
        "left {} right failed. ".format(op),
        "{}Showing unified diff ({}, {}):".format(Colour.stop, left_key, right_key),
        "",
    ] + build_unified_diff(lhs_repr, rhs_repr)


def build_full_splitdiff_output(lhs_repr, rhs_repr, op):
    lhs_diff, rhs_diff = build_split_diff(lhs_repr, rhs_repr)
    output = [
        "left {} right failed.".format(op),
        "{}Showing split diff:".format(Colour.stop),
        "",
    ]
    if lhs_diff and rhs_diff:
        lhs_diff[0] = Colour.stop + diff_intro_text("left:  ") + lhs_diff[0]
        rhs_diff[0] = Colour.stop + diff_intro_text("right: ") + rhs_diff[0]
    output += lhs_diff + rhs_diff
    return output
