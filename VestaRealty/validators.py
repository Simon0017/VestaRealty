from enum import Enum

from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number

# from .error_codes import PaymentErrorCode

# to validate the phone number
def validate_possible_number(phone, country=None):
    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.",
        )
    return phone_number

# to validate the amount
def validate_amount(amount):
    """this methods validates the amount"""
    if not amount or float(amount) <= 0:
        raise ValidationError(
            {"error": "Amount must be greater than Zero"}
        )
    return amount


# to validate the reference
def validate_reference(reference):
        """Write your validation logic here"""
        if reference:
            return reference
        return "Test"

# to validate the reference
def validate_description(description):
    """Write your validation logic here"""
    if description:
        return description
    return "Test"

