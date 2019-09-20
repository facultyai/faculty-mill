import shutil
from pathlib import Path
from io import TextIOWrapper

import click
from papermill.cli import papermill


def run_notebook(
    notebook: TextIOWrapper,
    directory: Path,
    execute: bool,
    click_context: click.Context,
) -> Path:
    input_path = directory / "input.ipynb"
    output_path = directory / "output.ipynb"
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
        shutil.copy(str(input_path), str(output_path))

    return output_path
