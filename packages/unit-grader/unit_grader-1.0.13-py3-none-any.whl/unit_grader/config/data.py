"""
This module contains the conversion data
for the conversion calculator.
"""
from ..config.enums import TemperatureUnits, UnitCategory, VolumeUnits

# Ask for unexpected exit
UNEXPECTED_EXIT: str = "Unexpected exit. Please contact the maintainer."

# Help instructions
HELP_INSTRUCTION: str = "Please use --help to see valid options."

# Conversion instructions
UNIT_CONVERSION_INSTRUCTIONS: str = (
    "Select a conversion unit (Kelvin, Celsius, "
    "Fahrenheit, Rankine for temperature; liters,"
    " tablespoons, cubic-inches, cups, cubic-feet,"
    " gallons for volume). Please note that the"
    " unit is case-sensitive."
)

# Units in each category
UNITS: dict = {
    UnitCategory.TEMPERATURE.value: [
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.RANKINE.value,
    ],
    UnitCategory.VOLUME.value: [
        VolumeUnits.LITERS.value,
        VolumeUnits.TABLESPOONS.value,
        VolumeUnits.CUBIC_INCHES.value,
        VolumeUnits.CUPS.value,
        VolumeUnits.CUBIC_FEET.value,
        VolumeUnits.GALLONS.value,
    ],
}

# Conversion data between units
CONVERSION_DATA: dict = {
    UnitCategory.TEMPERATURE.value: {
        (
            TemperatureUnits.CELSIUS.value,
            TemperatureUnits.FAHRENHEIT.value,
        ): lambda x: x * (9 / 5) + 32,
        (
            TemperatureUnits.CELSIUS.value,
            TemperatureUnits.KELVIN.value,
        ): lambda x: x + 273.15,
        (
            TemperatureUnits.CELSIUS.value,
            TemperatureUnits.RANKINE.value,
        ): lambda x: (x + 273.15) * (9 / 5),
        (
            TemperatureUnits.FAHRENHEIT.value,
            TemperatureUnits.CELSIUS.value,
        ): lambda x: (x - 32) * (5 / 9),
        (
            TemperatureUnits.FAHRENHEIT.value,
            TemperatureUnits.KELVIN.value,
        ): lambda x: (x + 459.67) * (5 / 9),
        (
            TemperatureUnits.FAHRENHEIT.value,
            TemperatureUnits.RANKINE.value,
        ): lambda x: x + 459.67,
        (
            TemperatureUnits.KELVIN.value,
            TemperatureUnits.CELSIUS.value,
        ): lambda x: x - 273.15,
        (
            TemperatureUnits.KELVIN.value,
            TemperatureUnits.FAHRENHEIT.value,
        ): lambda x: x * (9 / 5) - 459.67,
        (
            TemperatureUnits.KELVIN.value,
            TemperatureUnits.RANKINE.value,
        ): lambda x: x * (9 / 5),
        (
            TemperatureUnits.RANKINE.value,
            TemperatureUnits.CELSIUS.value,
        ): lambda x: (x - 491.67) * (5 / 9),
        (
            TemperatureUnits.RANKINE.value,
            TemperatureUnits.FAHRENHEIT.value,
        ): lambda x: x - 459.67,
        (
            TemperatureUnits.RANKINE.value,
            TemperatureUnits.KELVIN.value,
        ): lambda x: x * (5 / 9),
    },
    UnitCategory.VOLUME.value: {
        (VolumeUnits.LITERS.value, VolumeUnits.TABLESPOONS.value): lambda x: x * 67.628,
        (
            VolumeUnits.LITERS.value,
            VolumeUnits.CUBIC_INCHES.value,
        ): lambda x: x * 61.024,
        (VolumeUnits.LITERS.value, VolumeUnits.CUPS.value): lambda x: x * 4.227,
        (VolumeUnits.LITERS.value, VolumeUnits.CUBIC_FEET.value): lambda x: x / 28.317,
        (VolumeUnits.LITERS.value, VolumeUnits.GALLONS.value): lambda x: x / 3.785,
        (VolumeUnits.TABLESPOONS.value, VolumeUnits.LITERS.value): lambda x: x / 67.628,
        (
            VolumeUnits.TABLESPOONS.value,
            VolumeUnits.CUBIC_INCHES.value,
        ): lambda x: x / 1.108,
        (VolumeUnits.TABLESPOONS.value, VolumeUnits.CUPS.value): lambda x: x / 16,
        (
            VolumeUnits.TABLESPOONS.value,
            VolumeUnits.CUBIC_FEET.value,
        ): lambda x: x / 1915,
        (
            VolumeUnits.TABLESPOONS.value,
            VolumeUnits.GALLONS.value,
        ): lambda x: x / 256,
        (
            VolumeUnits.CUBIC_INCHES.value,
            VolumeUnits.LITERS.value,
        ): lambda x: x / 61.024,
        (
            VolumeUnits.CUBIC_INCHES.value,
            VolumeUnits.TABLESPOONS.value,
        ): lambda x: x * 1.108,
        (VolumeUnits.CUBIC_INCHES.value, VolumeUnits.CUPS.value): lambda x: x / 14.438,
        (
            VolumeUnits.CUBIC_INCHES.value,
            VolumeUnits.CUBIC_FEET.value,
        ): lambda x: x / 1728,
        (
            VolumeUnits.CUBIC_INCHES.value,
            VolumeUnits.GALLONS.value,
        ): lambda x: x / 231,
        (VolumeUnits.CUPS.value, VolumeUnits.LITERS.value): lambda x: x / 4.227,
        (VolumeUnits.CUPS.value, VolumeUnits.CUBIC_INCHES.value): lambda x: x * 14.438,
        (VolumeUnits.CUPS.value, VolumeUnits.TABLESPOONS.value): lambda x: x * 16,
        (VolumeUnits.CUPS.value, VolumeUnits.CUBIC_FEET.value): lambda x: x / 119.7,
        (VolumeUnits.CUPS.value, VolumeUnits.GALLONS.value): lambda x: x / 16,
        (VolumeUnits.CUBIC_FEET.value, VolumeUnits.LITERS.value): lambda x: x * 28.317,
        (
            VolumeUnits.CUBIC_FEET.value,
            VolumeUnits.CUBIC_INCHES.value,
        ): lambda x: x * 1728,
        (
            VolumeUnits.CUBIC_FEET.value,
            VolumeUnits.TABLESPOONS.value,
        ): lambda x: x * 1915,
        (VolumeUnits.CUBIC_FEET.value, VolumeUnits.CUPS.value): lambda x: x * 119.7,
        (VolumeUnits.CUBIC_FEET.value, VolumeUnits.GALLONS.value): lambda x: x * 7.481,
        (VolumeUnits.GALLONS.value, VolumeUnits.LITERS.value): lambda x: x * 3.785,
        (
            VolumeUnits.GALLONS.value,
            VolumeUnits.CUBIC_INCHES.value,
        ): lambda x: x * 231,
        (VolumeUnits.GALLONS.value, VolumeUnits.CUBIC_FEET.value): lambda x: x / 7.48,
        (
            VolumeUnits.GALLONS.value,
            VolumeUnits.TABLESPOONS.value,
        ): lambda x: x * 256,
        (VolumeUnits.GALLONS.value, VolumeUnits.CUPS.value): lambda x: x * 16,
    },
}
