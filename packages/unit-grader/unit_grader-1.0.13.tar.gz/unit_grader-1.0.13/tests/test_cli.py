"""
    ------------------------------------------------
    This module contains the tests for the CLI app.
    ------------------------------------------------
    The following functions are tested:
        * grade_conversion
        * version_callback
        * enable_verbose

"""
import pytest
import pytest_mock
from typer import Exit
from typer.testing import CliRunner

from unit_grader.cli import (
    app,
    handle_feedback,
    version_callback,
    enableLogging,
    app_name,
)
from unit_grader.config.enums import Answer
import logging

LOGGER = logging.getLogger(__name__)
# Create a CliRunner for testing the CLI app
runner = CliRunner()

grad_response_function_name = "unit_grader.commands.conversion_grader.grade_response"


# Test the grade_conversion CLI command
def test_grade_conversion_without_verbose(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the grade_conversion CLI command
      with correct arguments but without verbose mode

    Expected Behavior:
    -------------------
    Ensure that correct answer is returned
      and verbose messages are not printed.
    """
    mocker.patch(
        grad_response_function_name,
        return_value=Answer.CORRECT,
    )
    result = runner.invoke(
        app,
        [
            "--input-value",
            "32",
            "--from-unit",
            "Celsius",
            "--to-unit",
            "Kelvin",
            "--student-response",
            "305.2",
        ],
    )
    assert "Verbose mode is enabled." not in result.output
    assert "input_value: 32" not in result.output
    assert "from_unit: Celsius" not in result.output
    assert "to_unit: Kelvin" not in result.output
    assert "student_response: 305.2" not in result.output
    assert result.exit_code == 0
    assert Answer.CORRECT.value in result.output


@pytest.fixture
def setup_logging():
    logging.basicConfig(level=logging.NOTSET)


def test_enable_verbose(
    capfd: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture
) -> None:
    """
    Test the enable_verbose function
     when verbose is True

    Expected Behavior:
    -------------------
    Ensure that verbose mode is enabled
    """
    mock_logger_basicConfig = mocker.patch("logging.basicConfig")
    enableLogging(verbose=True)
    mock_logger_basicConfig.assert_called_once_with(
        level=logging.DEBUG, format="[%(levelname)s] %(message)s"
    )
    captured = capfd.readouterr()
    assert "Verbose mode is enabled." in captured.out


def test_enableLogging_non_verbose(
    capfd: pytest.CaptureFixture, mocker: pytest_mock.MockerFixture
) -> None:
    mock_logger_basicConfig = mocker.patch("logging.basicConfig")
    enableLogging(verbose=False)
    mock_logger_basicConfig.assert_called_once_with(
        level=logging.INFO, format="[%(levelname)s] %(message)s"
    )
    captured = capfd.readouterr()
    assert "Verbose mode is enabled." not in captured.out


def test_grade_conversion_verbose(
    mocker: pytest_mock.MockFixture, caplog: pytest.CaptureFixture
) -> None:
    """
    Test the grade_conversion CLI command with correct arguments and verbose mode

    Expected Behavior:
    -------------------
    Ensure that correct answer is returned and verbose messages are printed.

    """
    mocker.patch(
        grad_response_function_name,
        return_value=Answer.CORRECT,
    )
    caplog.set_level(logging.DEBUG)
    result = runner.invoke(
        app,
        [
            "--input-value",
            "32",
            "--from-unit",
            "Celsius",
            "--to-unit",
            "Kelvin",
            "--student-response",
            "305.2",
            "--verbose",
        ],
    )
    assert result.exit_code == 0
    assert "Verbose mode is enabled." in result.output
    assert "input_value: 32" in caplog.text
    assert "from_unit: Celsius" in caplog.text
    assert "to_unit: Kelvin" in caplog.text
    assert "student_response: 305.2" in caplog.text
    assert Answer.CORRECT.value in result.output


@pytest.fixture
def mock_app_version(mocker: pytest_mock.MockerFixture) -> None:
    """
    Mock the global_config function
    """
    mocker.patch("unit_grader.cli.app_version", new="1.0.1", autospec=False)


def test_version_callback(
    capsys: pytest_mock.MockerFixture, mock_app_version: pytest_mock.MockerFixture
) -> None:
    """
    Test the version_callback function
    Expected Behavior:
    -------------------
    Ensure that the function returns version information.

    """
    with pytest.raises(Exit):
        version_callback(True)  # Call the function
    # Capture the output using capsys
    captured = capsys.readouterr()
    output = captured.out.strip()
    assert output == f"{app_name}: 1.0.1"


@pytest.fixture
def mock_feedback_url(mocker: pytest_mock.MockerFixture) -> None:
    """
    Mock the global_config function
    """
    mocker.patch("unit_grader.cli.feedback_url", new="www.google.com", autospec=False)


def test_handle_feedback_valid_feedback_url(
    capsys: pytest_mock.MockerFixture, mock_feedback_url
) -> None:
    """
    Test the handle_feedback function

    Expected Behavior:
    -------------------
    Ensure that the function returns message including the feedback url.

    """

    handle_feedback()  # Call the function
    # Capture the output using capsys
    captured = capsys.readouterr()
    output = captured.out.strip()
    assert (
        "We would like your feedback! Please visit www.google.com to provide feedback."
        in output
    )
