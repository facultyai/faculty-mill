import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
from uuid import UUID

import click
import sherlockml
import sml.auth

from .version import print_version
from .execute import run


@contextmanager
def tmpdir():
    if Path("/project").is_dir():
        with TemporaryDirectory(prefix=".", dir="/project") as tmpdir:
            yield tmpdir
    else:
        with TemporaryDirectory(prefix=".") as tmpdir:
            yield tmpdir


@click.command(
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
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Display the version of this library.",
)
@click.pass_context
def main(
    click_context,
    notebook,
    report_name,
    description=None,
    code=False,
    execute=True,
):
    """
    Publish a report from NOTEBOOK under the name REPORT_NAME in the
    current project.

    This command supports all flags and options that papermill supports.
    """

    PROJECT_ID = UUID(os.getenv("SHERLOCKML_PROJECT_ID"))
    USER_ID = sml.auth.user_id()
    report_client = sherlockml.client("report")

    with tmpdir() as directory:
        directory = Path(directory)

        output_path = run(notebook, directory, execute, click_context)

        reports = {
            report.name: report for report in report_client.list(PROJECT_ID)
        }

        if report_name in reports:
            report_client.create_version(
                reports[report_name].id,
                str(output_path.relative_to("/project/")),
                USER_ID,
                show_code=code,
            )
            click.echo("Publishing report version...")
        else:
            report_client.create(
                PROJECT_ID,
                report_name,
                str(output_path.relative_to("/project/")),
                USER_ID,
                show_code=code,
            )
            click.echo("Publishing report...")

        sleep(5)
        click.echo("Done!")


if __name__ == "__main__":
    main()
