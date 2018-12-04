from pathlib import Path
from unittest.mock import Mock, patch
from uuid import uuid4

from faculty_mill import publish


def test_that_get_report_by_name_calls_the_right_endpoint():

    mock_report = Mock()
    mock_report.id = "test id"
    mock_report.name = "test name"
    mock_client = Mock()
    mock_client.list.return_value = [mock_report]

    with patch(
        "sherlockml.client", return_value=mock_client
    ) as mock_client_creator:

        result = publish.get_report_id_by_name("test name", "project id")
        mock_client_creator.assert_called_once_with("report")
        mock_client.list.assert_called_once_with("project id")
        assert result == mock_report.id


@patch("sherlockml.client")
def test_that_publish_calls_client_method_correctly_with_all_ids_set(
    mock_client_factory
):

    mock_client = Mock()
    mock_client_factory.return_value = mock_client
    test_report_id = uuid4()
    test_project_id = uuid4()
    test_user_id = uuid4()
    publish.publish(
        report_name="report name",
        path=Path("/project/test.ipynb"),
        show_code=False,
        report_id=test_report_id,
        project_id=test_project_id,
        user_id=test_user_id,
    )
