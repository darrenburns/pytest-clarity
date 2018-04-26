# -*- coding: utf-8 -*-

import pytest

from pytest_betterdiff.util import auto_repr, display_op_for, has_overriden_repr, has_differing_len, ecu


class SingleArg(object):
    def __init__(self, x):
        self.x = x


class BiArg(object):
    def __init__(self, y, z):
        self.y = y
        self.z = z

    def __repr__(self):
        return 'BiArg[[{}]]'.format(self.y)


@pytest.mark.parametrize('arg, expected_repr',
                         [
                             ('word', 'SingleArg(x=\'word\')'),
                             ('wørd', 'SingleArg(x=\'wørd\')'),
                             (123, 'SingleArg(x=123)'),
                             (123.0, 'SingleArg(x=123.0)'),
                             ([1, '2'], 'SingleArg(x=[1, \'2\'])'),
                             (BiArg(1, 2), 'SingleArg(x=BiArg[[1]])'),
                             (SingleArg('hello'), 'SingleArg(x=SingleArg(x=\'hello\'))'),
                         ]
                         )
def test_auto_repr(arg, expected_repr):
    assert auto_repr(SingleArg(arg)) == ecu(expected_repr)


def test_auto_repr_root_has_own_repr_impl():
    assert auto_repr(BiArg(1, 2)) == 'BiArg[[1]]'


@pytest.mark.parametrize('arg, result', [('equal', '=='), ('not in', 'not in')])
def test_display_op_for(arg, result):
    assert display_op_for(arg) == result


@pytest.mark.parametrize('arg, result', [(SingleArg(1), False), (BiArg(1, 2), True)])
def test_has_overriden_repr(arg, result):
    assert has_overriden_repr(arg) == result


@pytest.mark.parametrize('lhs, rhs, is_diff_len',
                         [
                             ([1, 2], [4, 5], False),
                             ([1, 2, 3], [4, 5], True),
                             ('abc', 'def', False),
                             ('ab', 'abc', True),
                             (set((1, 2, 3)), set((4, 5)), True),
                             ({'x': 'y'}, {'x': 'y', 'a': 'b'}, True),
                             ([], [], False),
                             ({}, {}, False),
                             ('', '', False),
                             (SingleArg(1), BiArg(1, 1), False),
                         ]
                         )
def test_has_differing_len(lhs, rhs, is_diff_len):
    assert has_differing_len(lhs, rhs) == is_diff_len
