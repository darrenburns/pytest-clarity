import json

import pytest

pytest_plugins = ["pytester"]


@pytest.mark.parametrize("color, environment, colored", [
    ("no", {}, False),
    ("yes", {}, True),
    ("auto", {"PY_COLORS": "0"}, False),
    ("auto", {"PY_COLORS": "1"}, True),
    ("auto", {"NO_COLOR": "1"}, False),
])
def test_diff_follows_pytest_color_policy(pytester, monkeypatch, color, environment, colored):
    for name in ("PY_COLORS", "NO_COLOR", "FORCE_COLOR"):
        monkeypatch.delenv(name, raising=False)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)
    pytester.makeconftest('''
        import json
        from pathlib import Path
        import pytest

        @pytest.hookimpl(hookwrapper=True, tryfirst=True)
        def pytest_assertrepr_compare():
            outcome = yield
            Path("diff.json").write_text(json.dumps(outcome.get_result()))
    ''')
    pytester.makepyfile("def test_difference():\n    assert 'one' == 'two'\n")
    result = pytester.runpytest_subprocess("-vv", "--color=" + color)
    result.assert_outcomes(failed=1)
    output = result.stdout.str()
    assert "pytest-clarity diff shown" in output
    assert "LHS" in output and "RHS" in output
    reports = json.loads((pytester.path / "diff.json").read_text())
    rendered_diff = "\n".join(next(lines for lines in reports
                                    if "pytest-clarity" in lines[0]))
    assert ("\x1b[" in rendered_diff) is colored
