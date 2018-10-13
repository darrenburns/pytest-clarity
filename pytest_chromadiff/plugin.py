from pytest_chromadiff.diff import build_split_diff, build_split_line_centric_diff
from pytest_chromadiff.hints import hints_for
from pytest_chromadiff.output import Colour, diff_intro_text
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
    display_op = display_op_for(op)

    width = int(config.getoption("--diff-width"))
    show_bg = config.getoption("--diff-bg")
    diff_type = config.getoption("--diff-type")

    lhs_repr = pformat_no_color(utf8_replace(left), width)
    rhs_repr = pformat_no_color(utf8_replace(right), width)

    output = []

    # Determine whether to show a split or unified diff
    if diff_type == "auto":
        if "\n" in lhs_repr and "\n" in rhs_repr:
            # In the case where both reprs are mutliple lines, we'll
            # use a line based diff rather than a character based one,
            # and present it as a unified diff.
            output += ["left {} right failed, showing unified diff:".format(display_op), ""]
            output += build_split_line_centric_diff(lhs_repr, rhs_repr)

    elif diff_type == "split":
        lhs_diff, rhs_diff = build_split_diff(lhs_repr, rhs_repr, show_bg)

        output += ["left {} right failed, where:".format(display_op), ""]

        if lhs_diff and rhs_diff:
            lhs_diff[0] = Colour.stop + diff_intro_text("left:  ") + lhs_diff[0]
            rhs_diff[0] = Colour.stop + diff_intro_text("right: ") + rhs_diff[0]

        output += lhs_diff + rhs_diff

    if not config.getoption("--no-hints"):
        output += hints_for(op, left, right)

    return [utf8_replace(line) for line in output]
