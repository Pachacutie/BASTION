"""CLI entry point for bastion-contract-scan."""

from __future__ import annotations

import sys
from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .extractor import extract
from .readability import compute_readability
from .report import render
from .scanner import scan

app = typer.Typer(add_completion=False)
err_console = Console(stderr=True)


def version_callback(value: bool):
    if value:
        print(f"bastion-contract-scan {__version__}")
        raise typer.Exit()


@app.command()
def main(
    file: Optional[str] = typer.Argument(  # noqa: UP007
        None,
        help="Path to PDF or text file. Omit to read from stdin.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    md_output: bool = typer.Option(False, "--md", help="Output as Markdown"),
    verbose: bool = typer.Option(False, "--verbose", help="Show matched trigger phrases and evidence"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output"),
    web: bool = typer.Option(False, "--web", help="Launch web interface in browser"),
    version: bool = typer.Option(False, "--version", callback=version_callback, is_eager=True, help="Show version"),
):
    """BASTION Contract Scan — detect predatory clauses in any contract."""
    if web:
        import webbrowser
        from .web import create_app
        flask_app = create_app()
        print(f"BASTION Contract Scan v{__version__} — web UI at http://127.0.0.1:5000")
        webbrowser.open("http://127.0.0.1:5000")
        flask_app.run(host="127.0.0.1", port=5000, debug=False)
        raise typer.Exit()

    fmt = "terminal"
    if json_output:
        fmt = "json"
    elif md_output:
        fmt = "md"

    try:
        extraction = extract(file)
    except (FileNotFoundError, ValueError) as e:
        err_console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    result = scan(extraction.text)
    readability = compute_readability(extraction.text)
    output = render(extraction, result, readability=readability, fmt=fmt, verbose=verbose, no_color=no_color)
    print(output)


if __name__ == "__main__":
    app()
