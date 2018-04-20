from six import u

from diff import build_split_diff
from hints import _hints_for
from terminal import Color, _diff_intro_text
from util import _display_op_for


def pytest_addoption(parser):
    parser.addoption(
        '--no-hints',
        action='store_true',
        default=False,
        help='disable pytest-betterdiff hints (boolean)',
    )


def pytest_assertrepr_compare(config, op, left, right):
    display_op = _display_op_for(op)

    lhs_diff, rhs_diff = build_split_diff(left, right)

    output = [u('left {} right failed, where: ').format(display_op), '']

    if lhs_diff and rhs_diff:
        lhs_diff[0] = Color.stop + _diff_intro_text('left:  ') + lhs_diff[0]
        rhs_diff[0] = Color.stop + _diff_intro_text('right: ') + rhs_diff[0]

    output += lhs_diff + rhs_diff

    if not config.getoption('--no-hints'):
        output += _hints_for(op, left, right)

    return output
