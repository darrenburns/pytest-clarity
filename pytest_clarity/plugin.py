from io import StringIO

from rich.console import Console
from _pytest.config import create_terminal_writer

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

    reporter = config.pluginmanager.getplugin("terminalreporter")
    writer = reporter._tw if reporter is not None else create_terminal_writer(config)
    use_color = writer.hasmarkup
    diff_text = console.export_text(styles=use_color)
    reset = "\033[0m" if use_color else ""

    return [
        f"{display_op_for(op)} failed. [pytest-clarity diff shown]",
        *[f"{reset}{line}" for line in diff_text.split(f"\n")],
    ]
