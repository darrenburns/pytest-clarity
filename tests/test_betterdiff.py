# -*- coding: utf-8 -*-

class Foo(object):
    def __init__(self, x):
        self.x = x


class Bar(object):
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return 'Bar({})'.format(self.x)

def test_something():
    assert True
