from pytest_chromadiff.diff import build_split_diff, build_unified_diff
from pytest_chromadiff.hints import hints_for
from pytest_chromadiff.output import Colour, diff_intro_text, header_text
from pytest_chromadiff.util import display_op_for, pformat_no_color, utf8_replace


def pytest_addoption(parser):
    parser.addoption(
        "--no-hints",
        action="store_true",
        default=False,
        help="pytest-chromadiff: disable hints (boolean)",
    )

    parser.addoption(
        "--diff-width",
        action="store",
        default="80",
        help="pytest-chromadiff: configure output width",
    )

    parser.addoption(
        "--diff-bg",
        action="store_true",
        default=False,
        help="pytest-chromadiff: use background colours on diff output",
    )

    parser.addoption(
        "--diff-type",
        action="store",
        default="auto",
        help="pytest-chromadiff: default auto. one of [auto, unified, split]",
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
    return [
               "left {} right failed, showing unified diff:".format(op),
               "",
               header_text("Unified Diff (L=left, R=right)"),
               "",
           ] + build_unified_diff(lhs_repr, rhs_repr)


def build_full_splitdiff_output(lhs_repr, rhs_repr, op):
    output = []
    lhs_diff, rhs_diff = build_split_diff(lhs_repr, rhs_repr)
    output += ["left {} right failed, showing split diff:".format(op),
               "",
               header_text("Split Diff"),
               "",
               ]
    if lhs_diff and rhs_diff:
        lhs_diff[0] = Colour.stop + diff_intro_text("left:  ") + lhs_diff[0]
        rhs_diff[0] = Colour.stop + diff_intro_text("right: ") + rhs_diff[0]
    output += lhs_diff + [""] + rhs_diff
    return output
