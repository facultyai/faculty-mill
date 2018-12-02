from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

from faculty_mill.execute import run


@pytest.fixture
def tempdir(tmpdir):
    """Fixture that wraps pytest fixture to return Path object"""
    return Path(str(tmpdir))


@pytest.fixture
def tmpnotebook():
    test_notebook = StringIO()
    test_notebook.write("test notebook content")
    test_notebook.seek(0)
    return test_notebook


@pytest.fixture
def mock_click_context():
    click_context = Mock()
    click_context.args = ["arg 1", "arg 2"]
    return click_context


def test_that_run_copies_content(tempdir, tmpnotebook, mock_click_context):
    output_notebook = run(
        tmpnotebook, tempdir, execute=False, click_context=mock_click_context
    )
    assert output_notebook.parent == tempdir
    assert output_notebook.read_text() == "test notebook content"


def test_that_run_calls_papermill(tempdir, tmpnotebook, mock_click_context):
    with patch("faculty_mill.execute.papermill") as mock_papermill:
        output_notebook = run(
            tmpnotebook,
            tempdir,
            execute=True,
            click_context=mock_click_context,
        )
        assert output_notebook.parent == tempdir
        mock_papermill.make_context.assert_called_once_with(
            "The papermill execution command.",
            [str(tempdir / "input.ipynb"), str(tempdir / "output.ipynb")]
            + mock_click_context.args,
            parent=mock_click_context,
        )
        mock_papermill.invoke.assert_called_once_with(
            mock_papermill.make_context.return_value
        )
