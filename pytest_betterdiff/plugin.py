from pytest_betterdiff.diff import build_split_diff
from pytest_betterdiff.hints import _hints_for
from pytest_betterdiff.terminal import Color, _diff_intro_text
from pytest_betterdiff.util import display_op_for, ecu


def pytest_addoption(parser):
    parser.addoption(
        '--no-hints',
        action='store_true',
        default=False,
        help='disable pytest-betterdiff hints (boolean)',
    )


def pytest_assertrepr_compare(config, op, left, right):
    display_op = display_op_for(op)
    print(left, right)
    lhs_diff, rhs_diff = build_split_diff(left, right)

    output = ['left {} right failed, where: '.format(display_op), '']

    if lhs_diff and rhs_diff:
        lhs_diff[0] = Color.stop + _diff_intro_text('left:  ') + lhs_diff[0]
        rhs_diff[0] = Color.stop + _diff_intro_text('right: ') + rhs_diff[0]

    output += lhs_diff + rhs_diff

    if not config.getoption('--no-hints'):
        output += _hints_for(op, left, right)

    return [ecu(line) for line in output]
