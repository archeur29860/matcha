from uuid import UUID

from utils.exceptions import ValidationError


def validate_uuid(value, field_name):

    try:
        return UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        raise ValidationError(
            f"{field_name} must be a valid UUID",
            {
                "field": field_name,
                "value": value
            }
        )

def validate_len_string(value, field_name, limit):
    if(len(value) < limit):
        return value
    raise ValidationError(
        f"{field_name} must be less than {limit}",
        {
            "field": field_name,
            "value": value
        }
    )

def validate_enum(value, field_name, enum_value):
    if value in enum_value:
        return value
    raise ValidationError(
        f"{field_name} must be in {enum_value}",
        {
            "field": field_name,
            "value": value
        }
    )