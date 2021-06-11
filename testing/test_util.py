from ward import test

from pytest_clarity.util import display_op_for

for arg, result in [
    ("equal", "=="),
    ("not in", "not in"),
]:

    @test(f"display_op_for(`{arg}`) returns `{result}`")
    def _(arg=arg, result=result):
        assert display_op_for(arg) == result
