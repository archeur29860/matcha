import re
from uuid import UUID

from utils.exceptions import ValidationError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def require_field(data, field_name):
    if field_name not in data:
        raise ValidationError(
            f"The field '{field_name}' is required",
            {"field": field_name},
        )
    return data[field_name]


def validate_max_len(value, field_name, limit):
    if len(value) <= limit:
        return value
    raise ValidationError(
        f"{field_name} must be {limit} characters or less",
        {"field": field_name, "value": value},
    )

def validate_email(value):
    if not value:
        raise ValidationError(
            "email cannot be empty",
            {"field": "email"},
        )

    validate_max_len(value, "email", 255)

    if not EMAIL_RE.fullmatch(value):
        raise ValidationError(
            "email must contain exactly one @ and at least one .",
            {"field": "email", "value": value},
        )

    return value

def 