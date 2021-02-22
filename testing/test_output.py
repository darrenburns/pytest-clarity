from pytest_clarity.output import (_colored, Colour, Attr)


def test_colored(monkeypatch):
    monkeypatch.delenv('NO_COLOR', raising=False)
    assert '\x1b[1m\x1b[31m' in _colored('foo', color=Colour.red, attrs=[Attr.bold])


def test_no_color(monkeypatch):
    monkeypatch.setenv('NO_COLOR', 1)
    assert '\x1b[1m\x1b[31m' not in _colored('foo', color=Colour.red, attrs=[Attr.bold])
