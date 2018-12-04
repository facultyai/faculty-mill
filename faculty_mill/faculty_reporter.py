import shutil
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

import click
from papermill.cli import papermill
from publish import publish

from .version import print_version


@contextmanager
def tmpdir() -> Path:
    if Path("/project").is_dir():
        with TemporaryDirectory(prefix=".", dir="/project") as tmpdir:
            yield Path(tmpdir)
    else:
        with TemporaryDirectory(prefix=".") as tmpdir:
            yield Path(tmpdir)


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
    show_code=False,
    execute=True,
):
    """
    Publish a report from NOTEBOOK under the name REPORT_NAME in the
    current project.

    Pass '-' as NOTEBOOK in order to parse file content from stdin.

    This command supports all flags and options that papermill supports.
    """

    with tmpdir() as directory:
        input_path = directory / "input.ipynb"
        output_path = directory / "output.ipynb"

        # write the input file to the new, temporary input file
        # this is to allow processing of stdin
        with input_path.open("w") as input_file:
            shutil.copyfileobj(notebook, input_file)

        if execute:
            papermill_click_context = papermill.make_context(
                "The papermill execution command.",
                [str(input_path), str(output_path)] + click_context.args,
                parent=click_context,
            )
            papermill.invoke(papermill_click_context)
        else:
            shutil.copy(input_path, output_path)

        publish(report_name, output_path, show_code=show_code)


if __name__ == "__main__":
    main()
