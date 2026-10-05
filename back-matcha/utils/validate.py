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
    try:
        if(len(value) > limit):
            return value
    except (ValueError, TypeError, AttributeError):
        raise ValidationError(
            f"{field_name} must be less than {limit}",
            {
                "field": field_name,
                "value": value
            }
        )