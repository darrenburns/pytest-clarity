from io import StringIO

from rich.console import Console

from pytest_clarity.diff import Diff
from pytest_clarity.util import display_op_for


def pytest_addoption(parser):
    parser.addoption(
        "--diff-width",
        action="store",
        default="80",
        help="pytest-clarity: configure output width",
    )
    parser.addoption(
        "--diff-symbols",
        action="store_true",
        default=False,
        help="pytest-clarity: configure whether to display diff symbols",
    )


def pytest_assertrepr_compare(config, op, left, right):
    if config.getoption("-v") < 2:
        return

    op = display_op_for(op)
    width = int(config.getoption("--diff-width"))
    show_symbols = bool(config.getoption("--diff-symbols"))

    diff = Diff(left, right, width, show_symbols)

    output = StringIO()
    console = Console(file=output, record=True)

    console.print("\n[green]LHS[/] vs [red]RHS[/] shown below\n")
    console.print(diff)

    diff_text = console.export_text(styles=True)

    return [
        f"{display_op_for(op)} failed. [pytest-clarity diff shown]",
        *[f"\033[0m{line}" for line in diff_text.split(f"\n")],
    ]
