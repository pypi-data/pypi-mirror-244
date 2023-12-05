"""
This module contains the enums used in the conversion data.
"""
from enum import Enum


class Answer(Enum):
    """
    This enum contains the grading result to a conversion question.
    """

    CORRECT = "correct"
    INCORRECT = "incorrect"
    INVALID = "invalid"


class UnitCategory(Enum):
    """
    This enum contains the categories of units of measure.
    """

    TEMPERATURE = "temperature"
    VOLUME = "volume"


class TemperatureUnits(Enum):
    """
    This enum contains the units of measure for temperature.
    """

    KELVIN = "Kelvin"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"
    RANKINE = "Rankine"


class VolumeUnits(Enum):
    """
    This enum contains the units of measure for volume.
    """

    LITERS = "liters"
    TABLESPOONS = "tablespoons"
    CUBIC_INCHES = "cubic-inches"
    CUPS = "cups"
    CUBIC_FEET = "cubic-feet"
    GALLONS = "gallons"
