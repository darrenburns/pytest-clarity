# -*- coding: utf-8 -*-

import pytest

from pytest_betterdiff.util import auto_repr


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
                             (123, 'SingleArg(x=123)'),
                             (123.0, 'SingleArg(x=123.0)'),
                             ([1, '2'], 'SingleArg(x=[1, \'2\'])'),
                             (BiArg(1, 2), 'SingleArg(x=BiArg[[1]])'),
                             (SingleArg('hello'), 'SingleArg(x=SingleArg(x=\'hello\'))'),
                         ]
                         )
def test_auto_repr(arg, expected_repr):
    assert auto_repr(SingleArg(arg)) == expected_repr


def test_auto_repr_root_has_own_repr_impl():
    assert auto_repr(BiArg(1, 2)) == 'BiArg[[1]]'
