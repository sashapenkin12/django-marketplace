"""
A module contains validators for users app models.
"""

from django.core.exceptions import ValidationError

def validate_even(value):
    """
    Validate whether the given number is even or not.

    Args:
        value: Validation number

    Raises:
        ValidationError: if value is not even
    """
    if value % 2 != 0:
        raise ValidationError(
            "%(value)s is not an even number",
            params={"value": value},
        )

def validate_length(value):
    """
    Validate whether the given value is shorter than 8 symbols.

    Args:
        value: Validation value

    Raises:
        ValidationError: if value is shorter than 8 symbols
    """
    if len(str(value)) > 8:
        raise ValidationError(
            '%(value)s does not have the required length'
        )
