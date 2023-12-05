"""
    ----------------------------------------------------------------------------
    This module contains the unit tests for the functions in the common.py file.
    ----------------------------------------------------------------------------
    The following functions are tested:
        * is_valid_numeric_string
        * convert_units

"""
import pytest

from unit_grader.config.data import CONVERSION_DATA
from unit_grader.config.enums import TemperatureUnits, UnitCategory, VolumeUnits
from unit_grader.utils.common import (
    convert_units,
    is_valid_numeric_string,
)

# is_valid_numeric_string
test_is_valid_numeric_string_valid = [
    ("25.0", True),
    ("-25.0", True),
    ("0.0", True),
]


@pytest.mark.parametrize(
    "input_value, expected",
    test_is_valid_numeric_string_valid,
)
def test_is_valid_numeric_string_valid(input_value: str, expected: bool) -> None:
    """
    Test the is_valid_numeric_string function with valid input.

    Expected Behavior:
    -------------------
    Ensure that the function returns True.
    """
    result = is_valid_numeric_string(input_value)
    assert result == expected


# is_valid_numeric_string
test_is_valid_numeric_string_invalid = [
    ("25.0+", False),
    ("-25.0+", False),
    ("hello", False),
    ("234hello", False),
    (None, False),
]


@pytest.mark.parametrize(
    "input_value, expected",
    test_is_valid_numeric_string_invalid,
)
def test_is_valid_numeric_string_invalid(input_value: str, expected: bool) -> None:
    """
    Test the is_valid_numeric_string function with invalid input.

    Expected Behavior:
    -------------------
    Ensure that the function returns False
    """
    result = is_valid_numeric_string(input_value)
    assert result == expected


# invalid category
test_convert_units_invalid_category = [
    (
        25.0,
        "celsius",
        "fahrenheit",
        "invalid_category",
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        "Weight",
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        "TemperaturE",
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        "Volume",
        CONVERSION_DATA,
        None,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_invalid_category,
)
def test_convert_units_invalid_category(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    """
    Test the convert_units function with invalid category.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected


# invalid from_unit or to_unit
test_convert_units_invalid_from_unit_to_unit = [
    (
        25.0,
        VolumeUnits.LITERS.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        VolumeUnits.LITERS.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        "from_unit",
        "to_unit",
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        None,
    ),
    (
        25.0,
        "from_unit",
        "to_unit",
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        None,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_invalid_from_unit_to_unit,
)
def test_convert_units_invalid_from_unit_to_unit(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected


# invalid conversion factor
mock_data_invalid_conversion_factor = {
    UnitCategory.TEMPERATURE.value: {},
    UnitCategory.VOLUME.value: {},
}

test_convert_units_invalid_conversion_factor = [
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.TEMPERATURE.value,
        mock_data_invalid_conversion_factor,
        None,
    ),
    (
        25.0,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        mock_data_invalid_conversion_factor,
        None,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_invalid_conversion_factor,
)
def test_convert_units_invalid_conversion_factor(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    """
    Test the convert_units function with invalid conversion factor.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected


# same valid from_unit to_unit
test_convert_units_same_valid_from_unit_to_unit = [
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        25.0,
    ),
    (
        25.0,
        VolumeUnits.LITERS.value,
        VolumeUnits.LITERS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        25.0,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_same_valid_from_unit_to_unit,
)
def test_convert_units_same_valid_from_unit_to_unit(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    """
    Test the convert_units function with same valid from_unit to_unit.

    Expected Behavior:
    -------------------
    Ensure that the function returns the input value.
    """
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected


# invalid conversion function
mock_data_invalid_conversion_data = {
    UnitCategory.TEMPERATURE.value: {
        (
            TemperatureUnits.CELSIUS.value,
            TemperatureUnits.FAHRENHEIT.value,
        ): 1
    },
    UnitCategory.VOLUME.value: {
        (VolumeUnits.LITERS.value, VolumeUnits.TABLESPOONS.value): 2
    },
}
test_convert_units_invalid_conversion_data = [
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.FAHRENHEIT.value,
        UnitCategory.TEMPERATURE.value,
        mock_data_invalid_conversion_data,
        None,
    ),
    (
        25.0,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        mock_data_invalid_conversion_data,
        None,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_invalid_conversion_data,
)
def test_convert_units_invalid_conversion_data(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    """
    Test the convert_units function when the conversion function is None.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected


# conversion function leads to unexpected error
mock_data_invalid_conversion_fuction = {
    UnitCategory.TEMPERATURE.value: {
        (
            TemperatureUnits.CELSIUS.value,
            TemperatureUnits.KELVIN.value,
        ): lambda x: x / 0,
    },
    UnitCategory.VOLUME.value: {
        (
            VolumeUnits.LITERS.value,
            VolumeUnits.CUBIC_INCHES.value,
        ): lambda x: x / 0,
    },
}
test_convert_units_invalid_conversion_function = [
    (
        25.0,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.TEMPERATURE.value,
        mock_data_invalid_conversion_fuction,
        None,
    ),
    (
        25.0,
        VolumeUnits.LITERS.value,
        VolumeUnits.CUBIC_INCHES.value,
        UnitCategory.VOLUME.value,
        mock_data_invalid_conversion_fuction,
        None,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_invalid_conversion_function,
)
def test_convert_units_invalid_conversion_function(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    """
    Test the convert_units function when the conversion function is invalid.

    Expected Behavior:
    -------------------
    Ensure that the function returns None.
    """
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected


# different valid from_unit to_unit
test_convert_units_different_valid_from_unit_to_unit = [
    # Test different number with or without decimal places
    (
        50,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        10.0,
    ),
    (
        60,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        15.6,
    ),
    (
        50.223,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        10.1,
    ),
    (
        -50.223,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -45.7,
    ),
    (
        0,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -17.8,
    ),
    (
        0.0,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -17.8,
    ),
    # Fahrenheit to Kelvin
    (
        50,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        283.2,
    ),
    # Fahrenheit to Rankine
    (
        50,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.RANKINE.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        509.7,
    ),
    # Celsius to Fahrenheit
    (
        50,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.FAHRENHEIT.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        122.0,
    ),
    # Celsius to Kelvin
    (
        50,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        323.2,
    ),
    # Celsius to Rankine
    (
        50,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.RANKINE.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        581.7,
    ),
    # Kelvin to Fahrenheit
    (
        50,
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.FAHRENHEIT.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -369.7,
    ),
    # Kelvin to Celsius
    (
        50,
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -223.2,
    ),
    # Kelvin to Rankine
    (
        50,
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.RANKINE.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        90.0,
    ),
    # Rankine to Fahrenheit
    (
        50,
        TemperatureUnits.RANKINE.value,
        TemperatureUnits.FAHRENHEIT.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -409.7,
    ),
    # Rankine to Celsius
    (
        50,
        TemperatureUnits.RANKINE.value,
        TemperatureUnits.CELSIUS.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        -245.4,
    ),
    # Rankine to Kelvin
    (
        50,
        TemperatureUnits.RANKINE.value,
        TemperatureUnits.KELVIN.value,
        UnitCategory.TEMPERATURE.value,
        CONVERSION_DATA,
        27.8,
    ),
    # Test different number from Liters to Tablespoons
    (
        50,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        3381.4,
    ),
    (
        60,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        4057.7,
    ),
    (
        50.223,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        3396.5,
    ),
    (
        -50.223,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        -3396.5,
    ),
    (
        0,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.0,
    ),
    (
        0.000,
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.0,
    ),
    # Liters to Cubic Inches
    (
        50,
        VolumeUnits.LITERS.value,
        VolumeUnits.CUBIC_INCHES.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        3051.2,
    ),
    # Liters to Cups
    (
        50,
        VolumeUnits.LITERS.value,
        VolumeUnits.CUPS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        211.4,
    ),
    # Liters to Cubic Feet
    (
        50,
        VolumeUnits.LITERS.value,
        VolumeUnits.CUBIC_FEET.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        1.8,
    ),
    # Liters to Gallons
    (
        50,
        VolumeUnits.LITERS.value,
        VolumeUnits.GALLONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        13.2,
    ),
    # Tablespoons to Liters
    (
        50,
        VolumeUnits.TABLESPOONS.value,
        VolumeUnits.LITERS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.7,
    ),
    # Tablespoons to Cubic Inches
    (
        50,
        VolumeUnits.TABLESPOONS.value,
        VolumeUnits.CUBIC_INCHES.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        45.1,
    ),
    # Tablespoons to Cups
    (
        50,
        VolumeUnits.TABLESPOONS.value,
        VolumeUnits.CUPS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        3.1,
    ),
    # Tablespoons to Cubic Feet
    (
        50,
        VolumeUnits.TABLESPOONS.value,
        VolumeUnits.CUBIC_FEET.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.0,
    ),
    # Tablespoons to Gallons
    (
        50,
        VolumeUnits.TABLESPOONS.value,
        VolumeUnits.GALLONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.2,
    ),
    # Cubic Inches to Liters
    (
        50,
        VolumeUnits.CUBIC_INCHES.value,
        VolumeUnits.LITERS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.8,
    ),
    # Cubic Inches to Tablespoons
    (
        50,
        VolumeUnits.CUBIC_INCHES.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        55.4,
    ),
    # Cubic Inches to Cups
    (
        50,
        VolumeUnits.CUBIC_INCHES.value,
        VolumeUnits.CUPS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        3.5,
    ),
    # Cubic Inches to Cubic Feet
    (
        100,
        VolumeUnits.CUBIC_INCHES.value,
        VolumeUnits.CUBIC_FEET.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.1,
    ),
    # Cubic Inches to Gallons
    (
        100,
        VolumeUnits.CUBIC_INCHES.value,
        VolumeUnits.GALLONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.4,
    ),
    # Cups to Liters
    (
        50,
        VolumeUnits.CUPS.value,
        VolumeUnits.LITERS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        11.8,
    ),
    # Cups to Tablespoons
    (
        50,
        VolumeUnits.CUPS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        800,
    ),
    # Cups to Cubic Inches
    (
        50,
        VolumeUnits.CUPS.value,
        VolumeUnits.CUBIC_INCHES.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        721.9,
    ),
    # Cups to Cubic Feet
    (
        50,
        VolumeUnits.CUPS.value,
        VolumeUnits.CUBIC_FEET.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        0.4,
    ),
    # Cups to Gallons
    (
        50,
        VolumeUnits.CUPS.value,
        VolumeUnits.GALLONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        3.1,
    ),
    # Cubic Feet to Liters
    (
        50,
        VolumeUnits.CUBIC_FEET.value,
        VolumeUnits.LITERS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        1415.8,
    ),
    # Cubic Feet to Tablespoons
    (
        50,
        VolumeUnits.CUBIC_FEET.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        95750.0,
    ),
    # Cubic Feet to Cubic Inches
    (
        50,
        VolumeUnits.CUBIC_FEET.value,
        VolumeUnits.CUBIC_INCHES.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        86400.0,
    ),
    # Cubic Feet to Cups
    (
        50,
        VolumeUnits.CUBIC_FEET.value,
        VolumeUnits.CUPS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        5985.0,
    ),
    # Cubic Feet to Gallons
    (
        50,
        VolumeUnits.CUBIC_FEET.value,
        VolumeUnits.GALLONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        374.0,
    ),
    # Gallons to Liters
    (
        100,
        VolumeUnits.GALLONS.value,
        VolumeUnits.LITERS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        378.5,
    ),
    # Gallons to Tablespoons
    (
        50,
        VolumeUnits.GALLONS.value,
        VolumeUnits.TABLESPOONS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        12800.0,
    ),
    # Gallons to Cubic Inches
    (
        50,
        VolumeUnits.GALLONS.value,
        VolumeUnits.CUBIC_INCHES.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        11550.0,
    ),
    # Gallons to Cups
    (
        50,
        VolumeUnits.GALLONS.value,
        VolumeUnits.CUPS.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        800.0,
    ),
    # Gallons to Cubic Feet
    (
        50,
        VolumeUnits.GALLONS.value,
        VolumeUnits.CUBIC_FEET.value,
        UnitCategory.VOLUME.value,
        CONVERSION_DATA,
        6.7,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, category, conversion_data, expected",
    test_convert_units_different_valid_from_unit_to_unit,
)
def test_convert_units_different_valid_from_unit_to_unit(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
    expected: bool,
) -> None:
    """
    Test the convert_units function with different valid from_unit to_unit.

    Expected Behavior:
    -------------------
    Ensure that the function returns the correct value.
    """
    result = convert_units(input_value, from_unit, to_unit, category, conversion_data)
    assert result == expected
