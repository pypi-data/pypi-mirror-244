"""
    -----------------------------------------------------------------
    This module contains unit tests for the conversion_grader.py file
    in the unit_grader/commands directory.
    -----------------------------------------------------------------
    The following functions are tested:
        * check_unit_existence
        * validate_input
        * grade_response

"""
import pytest
import pytest_mock

from unit_grader.commands.conversion_grader import (
    check_unit_existence,
    grade_response,
    validate_input,
)
from unit_grader.config.data import UNITS
from unit_grader.config.enums import Answer, TemperatureUnits, UnitCategory, VolumeUnits

# Define the function names for patching
check_unit_existence_function_name = (
    "unit_grader.commands." "conversion_grader.check_unit_existence"
)

is_valid_numeric_string_function_name = (
    "unit_grader.utils." "common.is_valid_numeric_string"
)

validate_input_function_name = (
    "unit_grader.commands." "conversion_grader.validate_input"
)

convert_units_function_name = "unit_grader.utils.common.convert_units"

# Test check_unit_existence

# Test check_unit_existence on temperature units
test_cases_check_unit_existence_temperature = [
    (UNITS, TemperatureUnits.KELVIN.value, UnitCategory.TEMPERATURE.value),
    (UNITS, TemperatureUnits.CELSIUS.value, UnitCategory.TEMPERATURE.value),
    (
        UNITS,
        TemperatureUnits.FAHRENHEIT.value,
        UnitCategory.TEMPERATURE.value,
    ),
    (UNITS, TemperatureUnits.RANKINE.value, UnitCategory.TEMPERATURE.value),
]


@pytest.mark.parametrize(
    "dictionary, unit_to_check, expected",
    test_cases_check_unit_existence_temperature,
)
def test_check_unit_existence_temperature(
    dictionary: dict, unit_to_check: str, expected: bool
) -> None:
    """
    Test the check_unit_existence function on temperature units.

    Expected Behavior:
    -------------------
    Ensure that the function returns "temperature".
    """
    result = check_unit_existence(dictionary, unit_to_check)
    assert result == expected


# Test check_unit_existence on volume units
test_cases_check_unit_existence_volume = [
    (UNITS, VolumeUnits.LITERS.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.TABLESPOONS.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.CUBIC_INCHES.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.CUPS.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.CUBIC_FEET.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.GALLONS.value, UnitCategory.VOLUME.value),
]


@pytest.mark.parametrize(
    "dictionary, unit_to_check, expected",
    test_cases_check_unit_existence_volume,
)
def test_check_unit_existence_volume(
    dictionary: dict, unit_to_check: str, expected: bool
) -> None:
    """
    Test the check_unit_existence function on volume units.

    Expected Behavior:
    -------------------
    Ensure that the function returns "volume".
    """
    result = check_unit_existence(dictionary, unit_to_check)
    assert result == expected


# Test check_unit_existence on nonexistent units
test_cases_check_unit_existence_nonexistent = [
    (UNITS, "KELvin", None),
    (UNITS, "NoneExist", None),
    (UNITS, "", None),
    (UNITS, None, None),
]


@pytest.mark.parametrize(
    "dictionary, unit_to_check, expected",
    test_cases_check_unit_existence_nonexistent,
)
def test_check_unit_existence_nonexistent(
    dictionary: dict, unit_to_check: str, expected: bool
) -> None:
    """
    Test the check_unit_existence function on nonexistent units.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = check_unit_existence(dictionary, unit_to_check)
    assert result == expected


# Test validate_input


# Test validate_input when from_unit is invalid
def test_validate_input_invalid_from_unit(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the validate_input function when from_unit is invalid.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[UnitCategory.TEMPERATURE.value, None],
    )
    result = validate_input("Dummy_Unit", TemperatureUnits.FAHRENHEIT.value, "25")
    assert result is None


# Test validate_input when to_unit is invalid
def test_validate_input_invalid_to_unit(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[UnitCategory.TEMPERATURE.value, None],
    )
    """
    Test the validate_input function when to_unit is invalid.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = validate_input(TemperatureUnits.CELSIUS.value, "Dummy_Unit", "25")
    assert result is None


# Test validate_input when from_unit and to_unit are invalid
def test_validate_input_invalid_from_and_to_unit(
    mocker: pytest_mock.MockFixture,
) -> None:
    """
    Test the validate_input function when from_unit and to_unit are invalid.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[None, None],
    )
    result = validate_input("Dummy_Unit", "Dummy_Unit", "25")
    assert result is None


# Test validate_input when from_unit and to_unit are valid but different categories
def test_validate_input_different_unit_categories(
    mocker: pytest_mock.MockFixture,
) -> None:
    """
    Test the validate_input function
     when from_unit and to_unit are in different categories

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[
            UnitCategory.TEMPERATURE.value,
            UnitCategory.VOLUME.value,
        ],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value, VolumeUnits.CUPS.value, "25"
    )
    assert result is None


# Test validate_input when input_value is not a number string
def test_validate_input_invalid_input_value(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the validate_input function when input_value is not a number string.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[
            UnitCategory.TEMPERATURE.value,
            UnitCategory.TEMPERATURE.value,
        ],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.FAHRENHEIT.value,
        "dog",
    )
    assert result is None


# Test validate_input when input_value is None
def test_validate_input_invalid_input_wrong_type(
    mocker: pytest_mock.MockFixture,
) -> None:
    """
    Test the validate_input function when input_value is None.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[
            UnitCategory.TEMPERATURE.value,
            UnitCategory.TEMPERATURE.value,
        ],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.FAHRENHEIT.value,
        None,
    )
    assert result is None


# Test validate_input when input_value is valid for temperature conversion
def test_validate_input_valid_temperature(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the validate_input function
      when input_value is valid for temperature conversion.

    Expected Behavior:
    -------------------
    Ensure that the function returns "temperature".
    """
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[
            UnitCategory.TEMPERATURE.value,
            UnitCategory.TEMPERATURE.value,
        ],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.FAHRENHEIT.value,
        "25",
    )
    assert result == UnitCategory.TEMPERATURE.value


# Test validate_input when input_value is valid for volume conversion
def test_validate_input_valid_volume(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=[UnitCategory.VOLUME.value, UnitCategory.VOLUME.value],
    )
    """
    Test the validate_input function
      when input_value is valid for volume conversion.

    Expected Behavior:
    -------------------
    Ensure that the function returns "volume".
    """
    result = validate_input(VolumeUnits.LITERS.value, VolumeUnits.TABLESPOONS, "25")
    assert result == UnitCategory.VOLUME.value


# Test validate_input when check_unit_existence raises an exception
def test_validate_input_unexpected_exception(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch(
        check_unit_existence_function_name,
        side_effect=Exception("This is a deliberate exception"),
    )
    """
    Test the validate_input function when check_unit_existence raises an exception.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = validate_input(VolumeUnits.LITERS.value, VolumeUnits.TABLESPOONS, "25")
    assert result is None


# Test grade_response


# Test grade_response when user response is not a number
def test_grade_response_non_numeric_user_response(
    mocker: pytest_mock.MockFixture,
) -> None:
    """
    Test the grade_response function when user response is not a number.

    Expected Behavior:
    -------------------
    Ensure that the function returns Answer.INCORRECT.
    """
    mocker.patch(
        is_valid_numeric_string_function_name,
        return_value=False,
    )
    mocker.patch(
        validate_input_function_name,
        return_value=UnitCategory.TEMPERATURE.value,
    )
    result = grade_response(
        "30",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        "dog",
    )
    assert result == Answer.INCORRECT


# Test grade_response when user response is incorrect
def test_grade_response_incorrect_response(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the grade_response function when user response is incorrect.

    Expected Behavior:
    -------------------
    Ensure that the function returns Answer.INCORRECT.
    """
    mocker.patch(
        is_valid_numeric_string_function_name,
        return_value=True,
    )
    mocker.patch(
        validate_input_function_name,
        return_value=UnitCategory.TEMPERATURE.value,
    )
    mocker.patch(
        convert_units_function_name,
        return_value=-241.1,
    )
    result = grade_response(
        "32",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        "-241.01",
    )
    assert result == Answer.INCORRECT


# Test grade_response when from_unit/to_unit/input_value is invalid
def test_grade_response_invalid_input(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the grade_response function when from_unit/to_unit/input_value is invalid.

    Expected Behavior:
    -------------------
    Ensure that the function returns Answer.INVALID.
    """
    mocker.patch(
        is_valid_numeric_string_function_name,
        return_value=True,
    )
    mocker.patch(
        validate_input_function_name,
        return_value=None,
    )
    result = grade_response(
        "dog",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        "-241.1",
    )
    assert result == Answer.INVALID


def test_grade_response_same_unit_incorrect_user_response(
    mocker: pytest_mock.MockFixture,
) -> None:
    """
    Test the grade_response function
        when from_unit and to_unit are the same but user response is incorrect.

    Expected Behavior:
    -------------------
    Ensure that the function returns Answer.INCORRECT.
    """
    mocker.patch(
        is_valid_numeric_string_function_name,
        return_value=True,
    )
    mocker.patch(
        validate_input_function_name,
        return_value=UnitCategory.TEMPERATURE.value,
    )
    result = grade_response(
        "32",
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.CELSIUS.value,
        "31",
    )
    assert result == Answer.INCORRECT


# Test grade_response when convert_units returns None
def test_grade_response_failed_convert_units(mocker: pytest_mock.MockFixture) -> None:
    """
    Test the grade_response function when convert_units returns None.

    Expected Behavior:
    -------------------
    Ensure that the function returns Answer.INVALID.
    """
    mocker.patch(
        is_valid_numeric_string_function_name,
        return_value=True,
    )
    mocker.patch(
        validate_input_function_name,
        return_value=UnitCategory.TEMPERATURE.value,
    )
    mocker.patch(convert_units_function_name, return_value=None)

    result = grade_response(
        "32",
        TemperatureUnits.CELSIUS.value,
        VolumeUnits.LITERS.value,
        "305.2",
    )
    assert result == Answer.INVALID


test_grade_response_correct_answer = [
    (
        "32.0",
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        "0",
        Answer.CORRECT,
    ),
    (
        "32.0",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        "-241.15",
        Answer.CORRECT,
    ),
    (
        "32.0",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.KELVIN.value,
        "32.0",
        Answer.CORRECT,
    ),
    (
        "32.01",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.KELVIN.value,
        "32.013",
        Answer.CORRECT,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, user_response, expected",
    test_grade_response_correct_answer,
)
def test_grade_response_correct_response(
    input_value: str,
    from_unit: str,
    to_unit: str,
    user_response: str,
    expected: Answer,
    mocker: pytest_mock.MockFixture,
) -> None:
    """
    Test the grade_response function when user response is correct.

    Expected Behavior:
    -------------------
    Ensure that the function returns Answer.CORRECT.
    """
    mocker.patch(
        is_valid_numeric_string_function_name,
        return_value=True,
    )
    mocker.patch(
        validate_input_function_name,
        return_value=UnitCategory.TEMPERATURE.value,
    )
    mocker.patch(
        convert_units_function_name,
        return_value=user_response,
    )
    # Test correct response
    result = grade_response(input_value, from_unit, to_unit, user_response)
    assert result == expected
