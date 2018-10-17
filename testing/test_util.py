# -*- coding: utf-8 -*-

import pytest

from pytest_clarity.util import display_op_for, has_differing_len, pformat_no_color


class SingleArg(object):
    def __init__(self, x):
        self.x = x


class BiArg(object):
    def __init__(self, y, z):
        self.y = y
        self.z = z

    def __repr__(self):
        return "BiArg[[{}]]".format(self.y)


@pytest.mark.parametrize("arg, result", [("equal", "=="), ("not in", "not in")])
def test_display_op_for(arg, result):
    assert display_op_for(arg) == result


@pytest.mark.parametrize(
    "lhs, rhs, is_diff_len",
    [
        ([1, 2], [4, 5], False),
        ([1, 2, 3], [4, 5], True),
        ("abc", "def", False),
        ("ab", "abc", True),
        ({1, 2, 3}, {4, 5}, True),
        ({"x": "y"}, {"x": "y", "a": "b"}, True),
        ([], [], False),
        ({}, {}, False),
        ("", "", False),
        (SingleArg(1), BiArg(1, 1), False),
    ],
)
def test_has_differing_len(lhs, rhs, is_diff_len):
    assert has_differing_len(lhs, rhs) == is_diff_len


@pytest.mark.parametrize("arg, result", [("s", '"s"'), ([1], "[1]"), (["1"], "['1']")])
def test_pformat_no_color(arg, result):
    assert pformat_no_color(arg, 60) == result
