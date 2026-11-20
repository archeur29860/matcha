from uuid import UUID
from pathlib import Path
import re
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





WORDS_FILE = Path(__file__).resolve().parent.parent / "common_english_words.txt"
with WORDS_FILE.open("r", encoding="utf-8") as f:
    COMMON_WORDS = {line.strip().lower() for line in f if line.strip()}

def validate_password(value: str, username: str, first_name: str, last_name: str) -> None:
    if not value:
        raise ValidationError("password is required", {"field": "password"})
    checks = [
        (len(value) >= 12, "the password must be at least 12 characters"),
        (bool(re.search(r"[a-z]", value)), "the password must have at least 1 lowercase"),
        (bool(re.search(r"[A-Z]", value)), "the password must have at least 1 uppercase"),
        (bool(re.search(r"\d", value)), "the password must have at least 1 number"),
        (bool(re.search(r"[^A-Za-z0-9]", value)), "the password must have at least 1 special char"),
    ]
    for ok, message in checks:
        if not ok:
            raise ValidationError(message, {"field": "password"})

    lower = value.lower()
    if lower in COMMON_WORDS:
        raise ValidationError("the password must not be a common english word", {"field": "password"})

    for label, name in (("username", username), ("first name", first_name), ("last name", last_name)):
        if name and name.strip().lower() in lower:
            raise ValidationError(
                f"the password must not contain your {label}",
                {"field": "password"},
            )
