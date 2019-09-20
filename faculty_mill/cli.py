from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

import click

from .publish import publish
from .version import version
from .execute import run_notebook


@contextmanager
def tmpdir() -> Path:
    if Path("/project").is_dir():
        with TemporaryDirectory(prefix=".", dir="/project") as tmpdir:
            yield Path(tmpdir)
    else:
        with TemporaryDirectory(prefix=".") as tmpdir:
            yield Path(tmpdir)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    pass


@cli.command(name="version")
def echo_version():
    "Print the faculty-mill version number."
    click.echo(version)


@cli.command(
    context_settings=dict(
        help_option_names=["-h", "--help"],
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.argument("notebook", type=click.File())
@click.argument("report_name")
@click.option(
    "--description", default=None, help="The description of the report."
)
@click.option(
    "--code/--no-code",
    default=False,
    help="Whether or not the code cells should be shown.",
)
@click.option(
    "--execute/--as-is",
    default=True,
    help="Whether the notebook should be executed before publishing or not.",
)
@click.pass_context
def run(
    click_context,
    notebook,
    report_name,
    description=None,
    show_code=False,
    execute=True,
):
    """Run a notebook and publish it as a report.

    All additional flags and options to the ones specified below will be passed
    onto papermill
    """

    with tmpdir() as directory:

        output_path = run_notebook(notebook, directory, execute, click_context)

        publish(report_name, output_path, show_code=show_code)


@cli.command()
def create_job():
    """
    Create a Faculty Platform job that will run a notebook.
    """
    raise NotImplementedError
