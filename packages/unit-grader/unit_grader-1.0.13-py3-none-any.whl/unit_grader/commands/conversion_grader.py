from typing import Optional

import numpy as np  # Import numpy for rounding
import typer
from rich import print

from ..config.data import (
    CONVERSION_DATA,
    HELP_INSTRUCTION,
    UNIT_CONVERSION_INSTRUCTIONS,
    UNITS,
)
from ..config.enums import Answer
from ..utils.common import convert_units, is_valid_numeric_string


def check_unit_existence(
    dictionary: dict[str, list[str]], unit_to_check: str
) -> Optional[str]:
    """
    Check if a unit exists in a dictionary.

    Args:
        dictionary (dict): The dictionary to check.
        unit_to_check (str): The unit to check.

    Returns:
        str: The category of the unit (e.g., 'temperature' or 'volume').
        None: If the unit does not exist.
    """
    for key, units in dictionary.items():
        if unit_to_check in units:
            return key
    return None


def validate_input(from_unit: str, to_unit: str, input_value: str) -> Optional[str]:
    """
    Validate the input values

    Args:
        from_unit (str): The unit to convert from.
        to_unit (str): The unit to convert to.
        input_value (str): The input value to be converted.

    Returns:
        str: The category of the units (e.g., 'temperature' or 'volume').
        None: If the input is invalid.
    """

    try:
        if not is_valid_numeric_string(input_value):
            raise TypeError(
                (
                    f"{input_value} as input_value"
                    f" needs to be a number. {HELP_INSTRUCTION}"
                )
            )
        from_unit_category = check_unit_existence(UNITS, from_unit)
        to_unit_category = check_unit_existence(UNITS, to_unit)

        if from_unit_category is None:
            raise ValueError(
                (
                    f"{from_unit} as from_unit"
                    f" is not supported. {UNIT_CONVERSION_INSTRUCTIONS}"
                )
            )

        if to_unit_category is None:
            raise ValueError(
                (
                    f"{to_unit} as to_unit"
                    f" is not supported. {UNIT_CONVERSION_INSTRUCTIONS}"
                )
            )

        if from_unit_category != to_unit_category:
            raise ValueError(
                (
                    f"Ensure the selected conversion units"
                    " match their respective categories"
                    f" for a valid conversion. {UNIT_CONVERSION_INSTRUCTIONS}"
                )
            )
    except TypeError as e:
        print(f"[bold red]Input Error: {e}[/bold red]")
        return None
    except ValueError as e:
        print(f"[bold red]Input Error: {e}[/bold red]")
        return None
    except Exception as e:
        print(f"[bold red]Error: {e}.[/bold red]")
        return None
    return from_unit_category


def grade_response(
    input_value: str, from_unit: str, to_unit: str, student_response: str
) -> Answer:
    """
    Grade a student's response to a conversion question.
    The student's response is correct if it matches the correct answer after both values are rounded to the tenths place. The rounding strategy follows round half to even (Banker's rounding).
    For example round(4.65, 1) == 4.6 and round(4.75, 1) == 4.8.

    Args:
        input_value (str): The input value provided in the question.
        from_unit (str): The unit mentioned in the question.
        to_unit (str): The target unit mentioned in the question.
        student_response (str): The student's response.
    Returns:
        Answer: The result of the grading.
        Possible values are: Answer.CORRECT, Answer.INCORRECT, Answer.INVALID
    """
    # unit name validation
    category: Optional[str] = validate_input(from_unit, to_unit, input_value)
    if category is None:  # invalid input
        return Answer.INVALID

    if not is_valid_numeric_string(student_response):
        typer.echo(f"\n{student_response} is not a valid numeric string.")
        return Answer.INCORRECT

    if from_unit == to_unit:
        correct_answer: float = np.round(float(input_value), 1)
        student_response: float = np.round(float(student_response), 1)
        if correct_answer == student_response:
            return Answer.CORRECT
        else:
            typer.echo(
                f"\n{student_response} is not the correct answer. The correct answer is {correct_answer}."
            )
            return Answer.INCORRECT

    student_response: float = np.round(float(student_response), 1)
    input_numeric_value: float = float(input_value)
    convert_value: Optional(float) = convert_units(
        input_numeric_value, from_unit, to_unit, category, CONVERSION_DATA
    )
    if convert_value is None:
        return Answer.INVALID
    elif convert_value == student_response:
        return Answer.CORRECT
    else:
        typer.echo(
            f"\n{student_response} is not the correct answer. The correct answer is {convert_value}."
        )
        return Answer.INCORRECT
