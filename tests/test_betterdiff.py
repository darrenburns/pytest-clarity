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
    assert Foo(2) == Foo(1)
    assert {'key': 'first value'} == {'key': 'second value'}
    assert [1, 2, 3] == [2, 3, 1]
    assert [202, 4202, 2202] == [2202, 3202, 5202, 4202]
    assert [Foo(1), Foo(2), Foo(3)] == [Foo(1), Foo(2), Foo(4), Bar(5)]
    assert set([1, 2, 3]) == set([2, 1])
    assert list(range(4, 30)) == list(range(1, 7))
    assert 0 in [1, 2, 3, 4]
    assert 'tr' in 'tomato'
    assert [1, 2, 3] != [1, 2, 3]
    assert 1 not in [1, 2, 3, 4]
