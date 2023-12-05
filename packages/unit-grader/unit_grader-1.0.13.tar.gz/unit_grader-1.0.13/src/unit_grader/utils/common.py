from typing import Optional

import numpy as np  # Import numpy for rounding
from rich import print

from ..config.data import UNITS


def is_valid_numeric_string(numeric_string: str) -> bool:
    """
    Check if a string is a valid numeric string.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a valid numeric string, False otherwise.
    """
    try:
        float(numeric_string)  # Try to convert the string to a float
        return True  # If successful, it's a valid numeric string
    except TypeError:
        return False
    except ValueError:
        return False


def convert_units(
    input_value: str,
    from_unit: str,
    to_unit: str,
    category: str,
    conversion_data: dict,
) -> Optional[float]:
    """
    Convert an input value from one unit to another.

    Args:
        input_value (float): The input value to be converted.
        from_unit (str): The unit to convert from.
        to_unit (str): The unit to convert to.
        category (str): The unit category ('temperature' or 'volume').
        conversion_data (dict): The conversion data.

    Returns:
        float: The converted value.
        None: If the conversion cannot be performed.
    """
    # Perform the conversion
    try:
        # Validate the input parameters
        if category not in UNITS:
            raise ValueError(f"category {category} is not a valid category.")

        if (from_unit not in UNITS[category]) or (to_unit not in UNITS[category]):
            raise ValueError(
                (
                    f"from_unit {from_unit} is not a "
                    f"valid unit or to_unit {to_unit} is not a valid unit."
                )
            )

        # if from_unit == to_unit return the output
        if from_unit == to_unit:
            return np.round(input_value, 1)

        # Define conversion factors for temperatures and volumes
        if (from_unit, to_unit) not in conversion_data[category]:
            raise ValueError(
                (f"Conversion factor for {from_unit}" f"to {to_unit} does not exist.")
            )

        conversion_func = conversion_data[category][(from_unit, to_unit)]
        if not callable(conversion_func):
            raise ValueError(
                (
                    f"Conversion function {conversion_func} "
                    f"for {from_unit} to {to_unit} is not callable."
                )
            )
        """
        Perform the conversion and avoid the
        floating point precision issue using numpy for rounding
        checkout https://docs.python.org/3/
        library/functions.html#round for rounding issue in python3
        """

        converted_value = np.round((conversion_func(input_value)), 3)
        return np.round(converted_value, 1)
    except ValueError as e:
        print(f"[bold red]Error: {e}.[/bold red]")
        return None
    except Exception as e:
        print(f"[bold red]Error: {e}.[/bold red]")
        return None  # Cannot convert for any reason
