import os
from pathlib import Path
from time import sleep
from typing import Optional
from uuid import UUID

import click
import sherlockml
import sml.auth


def publish(
    report_name: str,
    path: Path,
    show_code: bool = False,
    report_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
):
    """Publish a notebook as a report.

    Parameters
    ----------
    report_name : str
        The name of the report
    path : Path
        The path of the notebook.
    report_id : Optional[UUID], optional
        The report ID, if you want to publish it as a version of an existing
        report (the default is None, in which case we search for an existing
        report with the provided name)
    project_id : Optional[UUID], optional
        The project ID. Only needed if not invoking from within a project.
    user_id : Optional[UUID], optional
        The user ID. Only needed if not invoking from within a project.
    show_code : bool, optional
        Whether the code should be shown in the report or not (default False)
    """

    if project_id is None:
        project_id = UUID(os.getenv("SHERLOCKML_PROJECT_ID"))

    if user_id is None:
        user_id = sml.auth.user_id()

    report_client = sherlockml.client("report")

    if report_id is None:
        report_id = get_report_id_by_name(report_name, project_id)

    if report_id is not None:
        report_client.create_version(
            report_id,
            str(path.relative_to("/project/")),
            user_id,
            show_code=show_code,
        )
        click.echo("Publishing report version...")
    else:
        report_client.create(
            project_id,
            report_name,
            str(path.relative_to("/project/")),
            user_id,
            show_code=show_code,
        )
        click.echo("Publishing report...")
    # this is to allow farah to process the notebook before deleting it
    sleep(5)
    click.echo("Done!")


def get_report_id_by_name(
    report_name: str, project_id: UUID
) -> Optional[UUID]:
    """Get a report id if the name exists in a project

    Parameters
    ----------
    report_name : str
        The name of the report.
    project_id : UUID
        The ID of the project in which to check for the report name.

    Returns
    -------
    Optional[UUID]
        The report ID if a report with that name exists, else None
    """

    report_client = sherlockml.client("report")
    reports = {
        report.name: report.id for report in report_client.list(project_id)
    }
    return reports.get(report_name)
