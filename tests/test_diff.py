# coding=utf-8
from pytest_betterdiff.diff import build_split_diff
from pytest_betterdiff.util import ecu


def test_build_split_diff():
    lhs_diff, rhs_diff = build_split_diff(ecu('abcde'), ecu('abbde'))

    # Remove the 'c' from the left (thus colour it red)
    assert lhs_diff == ['\x1b[0m"ab\x1b[1m\x1b[31m' + 'c' + '\x1b[0m\x1b[0mde"']
    # Add the 'b' to the right (colour it green)
    assert rhs_diff == ['\x1b[0m"ab\x1b[1m\x1b[32m' + 'b' + '\x1b[0m\x1b[0mde"']
