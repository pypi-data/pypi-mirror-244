"""
End-to-End Tests for the Unit Grader CLI App
------------------------------------------------------------------
This module contains end-to-end tests for the unit_grader CLI app.
------------------------------------------------------------------
The following commands are tested:
        * unit-grader
"""
import pytest
from typer.testing import CliRunner

from unit_grader.cli import app
from unit_grader.config.enums import Answer
from unit_grader.config.enums import TemperatureUnits as T
from unit_grader.config.enums import VolumeUnits as V

# Create a CliRunner for testing the CLI app
runner = CliRunner()

# Test the grade_conversion CLI command with valid input and correct response
test_case_valid_input_correct_response = [
    ("100", T.CELSIUS.value, T.KELVIN.value, "373.15"),
    ("100", T.CELSIUS.value, T.FAHRENHEIT.value, "212"),
    ("100", T.CELSIUS.value, T.RANKINE.value, "671.67"),
    ("100", T.FAHRENHEIT.value, T.CELSIUS.value, "37.78"),
    ("100", T.FAHRENHEIT.value, T.KELVIN.value, "310.93"),
    ("100", T.FAHRENHEIT.value, T.RANKINE.value, "559.67"),
    ("100", T.KELVIN.value, T.CELSIUS.value, "-173.15"),
    ("100", T.KELVIN.value, T.FAHRENHEIT.value, "-279.67"),
    ("100", T.KELVIN.value, T.RANKINE.value, "180"),
    ("100", T.RANKINE.value, T.CELSIUS.value, "-217.59"),
    ("100", T.RANKINE.value, T.FAHRENHEIT.value, "-359.67"),
    ("100", T.RANKINE.value, T.KELVIN.value, "55.56"),
    ("100", V.GALLONS.value, V.LITERS.value, "378.54"),
    ("100", V.GALLONS.value, V.CUBIC_FEET.value, "13.37"),
    ("100", V.GALLONS.value, V.CUBIC_INCHES.value, "23100"),
    ("100", V.GALLONS.value, V.CUPS.value, "1577.25"),
    ("100", V.GALLONS.value, V.TABLESPOONS.value, "25600"),
    ("100", V.CUBIC_FEET.value, V.GALLONS.value, "748.05"),
    ("100", V.CUBIC_FEET.value, V.LITERS.value, "2831.68"),
    ("100", V.CUBIC_FEET.value, V.CUBIC_INCHES.value, "172800"),
    ("100", V.CUBIC_FEET.value, V.CUPS.value, "11798.7"),
    ("100", V.CUBIC_FEET.value, V.TABLESPOONS.value, "191501"),
    ("100", V.CUBIC_INCHES.value, V.GALLONS.value, "0.43"),
    ("100", V.CUBIC_INCHES.value, V.LITERS.value, "1.64"),
    ("100", V.CUBIC_INCHES.value, V.CUBIC_FEET.value, "0.06"),
    ("100", V.CUBIC_INCHES.value, V.CUPS.value, "6.83"),
    ("100", V.CUBIC_INCHES.value, V.TABLESPOONS.value, "110.823"),
    ("100", V.LITERS.value, V.GALLONS.value, "26.42"),
    ("100", V.LITERS.value, V.CUBIC_FEET.value, "3.53"),
    ("100", V.LITERS.value, V.CUBIC_INCHES.value, "6102.37"),
    ("100", V.LITERS.value, V.CUPS.value, "416.667"),
    ("100", V.LITERS.value, V.TABLESPOONS.value, "6762.8"),
    ("100", V.CUPS.value, V.GALLONS.value, "6.25"),
    ("100", V.CUPS.value, V.CUBIC_FEET.value, "0.01"),
    ("100", V.CUPS.value, V.CUBIC_INCHES.value, "144.3"),
    ("100", V.CUPS.value, V.LITERS.value, "23.66"),
    ("100", V.CUPS.value, V.TABLESPOONS.value, "1600"),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, student_response",
    test_case_valid_input_correct_response,
)
def test_grade_conversion_valid_input_correct_response(
    input_value: str, from_unit: str, to_unit: str, student_response: str
) -> None:
    """
    Test the grade_conversion CLI command with valid input and correct response.

    Expected Behavior:
    -------------------
    Ensure that the function returns correct.
    """
    result = runner.invoke(
        app,
        [
            "--input-value",
            input_value,
            "--from-unit",
            from_unit,
            "--to-unit",
            to_unit,
            "--student-response",
            student_response,
        ],
    )
    assert result.exit_code == 0
    assert Answer.CORRECT.value in result.output


# Test the grade_conversion CLI command with valid input and incorrect response

test_case_valid_input_incorrect_response = [
    ("100", T.CELSIUS.value, T.KELVIN.value, "dog"),
    ("100", T.CELSIUS.value, T.KELVIN.value, "373.15dog"),
    ("100", T.CELSIUS.value, T.KELVIN.value, "373.5"),
    ("100", T.CELSIUS.value, T.KELVIN.value, "373"),
    ("100", T.CELSIUS.value, T.KELVIN.value, "373.001"),
    ("100", T.CELSIUS.value, T.KELVIN.value, ".001"),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, student_response",
    test_case_valid_input_incorrect_response,
)
def test_grade_conversion_valid_input_incorrect_response(
    input_value: str, from_unit: str, to_unit: str, student_response: str
) -> None:
    """
    Test the grade_conversion CLI command with valid input and correct response.

    Expected Behavior:
    -------------------
    Ensure that the function returns incorrect.
    """
    result = runner.invoke(
        app,
        [
            "--input-value",
            input_value,
            "--from-unit",
            from_unit,
            "--to-unit",
            to_unit,
            "--student-response",
            student_response,
        ],
    )
    assert result.exit_code == 0
    assert Answer.INCORRECT.value in result.output


# Test the grade_conversion CLI command with invalid input
test_case_invalid_input = [
    ("dog", T.CELSIUS.value, T.KELVIN.value, "373.15"),
    ("dog100", T.CELSIUS.value, T.KELVIN.value, "373.15"),
    ("dog100", T.CELSIUS.value, T.KELVIN.value, "dog"),
    ("100", "CELSISUS", T.KELVIN.value, "373.15"),
    ("100", "celsius", T.KELVIN.value, "373.15"),
    ("100", "CelsiuS", T.KELVIN.value, "373.15"),
    ("100", "Dummy", T.KELVIN.value, "373.15"),
    ("100", "Dummy", T.KELVIN.value, "dog"),
    ("100", T.CELSIUS.value, V.LITERS.value, "373.15"),
    ("100", V.CUBIC_FEET.value, T.FAHRENHEIT, "373.15"),
    ("100", T.CELSIUS.value, "KELVIN", "373.15"),
    ("100", T.CELSIUS.value, "kelvin", "373.15"),
    ("100", T.CELSIUS.value, "KelviN", "373.15"),
    ("100", T.CELSIUS.value, "Dummy", "373.15"),
    ("100", T.CELSIUS.value, "Dummy", "dog"),
    ("100", T.CELSIUS.value, "Dummy", "373.2"),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, student_response",
    test_case_invalid_input,
)
def test_grade_conversion_invalid_input(
    input_value: str, from_unit: str, to_unit: str, student_response: str
) -> None:
    """
    Test the grade_conversion CLI command with invalid input.

    Expected Behavior:
    -------------------
    Ensure that the function returns invalid.
    """
    result = runner.invoke(
        app,
        [
            "--input-value",
            input_value,
            "--from-unit",
            from_unit,
            "--to-unit",
            to_unit,
            "--student-response",
            student_response,
        ],
    )
    assert result.exit_code == 0
    print(result.output)
    assert Answer.INVALID.value in result.output
