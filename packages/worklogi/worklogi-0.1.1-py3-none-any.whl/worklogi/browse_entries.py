from rich.style import Style
from worklogi.entry import Entry
from rich.console import Console
from rich.table import Table
from .database import WorkLogDatabase


def browse_entries(_):
    table = Table(title="worklogi")
    for column in Entry.get_header():
        table.add_column(column)
    for entry in WorkLogDatabase.get_entries():
        is_checkout = entry.title == "checkout"
        is_rebase = entry.branch == "HEAD"
        row_style = Style(dim=is_rebase, bold=is_checkout)
        table.add_row(*entry.get_data(), style=row_style)

    console = Console()
    console.print(table)
