from pytest_chromadiff.diff import build_split_diff
from pytest_chromadiff.hints import _hints_for
from pytest_chromadiff.terminal import Color, diff_intro_text
from pytest_chromadiff.util import display_op_for, ecu


def pytest_addoption(parser):
    parser.addoption(
        '--no-hints',
        action='store_true',
        default=False,
        help='disable pytest-chromadiff hints (boolean)',
    )


def pytest_assertrepr_compare(config, op, left, right):
    display_op = display_op_for(op)
    lhs_diff, rhs_diff = build_split_diff(ecu(left), ecu(right))

    output = ['left {} right failed, where: '.format(display_op), '']

    if lhs_diff and rhs_diff:
        lhs_diff[0] = Color.stop + diff_intro_text('left:  ') + lhs_diff[0]
        rhs_diff[0] = Color.stop + diff_intro_text('right: ') + rhs_diff[0]

    output += lhs_diff + rhs_diff

    if not config.getoption('--no-hints'):
        output += _hints_for(op, left, right)

    return [ecu(line) for line in output]
