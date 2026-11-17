<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: string
    placeholder?: string
    disabled?: boolean
  }>(),
  {
    type: 'text',
    placeholder: '',
    disabled: false,
  }
)

const model = defineModel<string>({ default: '' })
</script>

<template>
  <div class="input-wrapper">
    <input
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      class="input"
    />
  </div>
</template>

<style scoped>
.input-wrapper {
  width: 100%;
}

.input {
  width: 100%;
  height: 48px;
  padding: 0 16px;

  box-sizing: border-box;

  border: 1px solid #f1e5e5;
  border-radius: 14px;

  background: #ffffff;
  color: #3c2830;

  font-family: inherit;
  font-size: 15px;
  font-weight: 500;

  outline: none;

  box-shadow: 0 6px 18px rgba(60, 30, 40, 0.05);

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.input::placeholder {
  color: #b9a9af;
  font-weight: 400;
}

.input:hover:not(:disabled) {
  border-color: #ead5da;
}

.input:focus {
  border-color: #ed6284;
  box-shadow:
    0 0 0 3px rgba(237, 98, 132, 0.1),
    0 6px 18px rgba(60, 30, 40, 0.06);
}

.input:disabled {
  background: #f8f1f3;
  color: #a99aa0;
  cursor: not-allowed;
  box-shadow: none;
}

@media (max-width: 600px) {
  .input {
    height: 46px;
    font-size: 14px;
    padding: 0 14px;
  }
}
</style>


from flask import Blueprint, request
import services.users_services as u

from utils.validate import validate_len_string, validate_uuid
from utils.response import success


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


def validate_user_fields(data):
    if not isinstance(data, dict):
        return None, ({"error": "JSON body required"}, 400)

    required_fields = [
        "email",
        "username",
        "last_name",
        "first_name",
        "password"
    ]

    all_field_content = {}

    for field in required_fields:
        if field not in data:
            return None, (
                {"error": f"The field '{field}' is required"},
                400
            )

        field_content = data[field]

        if not isinstance(field_content, str):
            return None, (
                {"error": f"{field} must be a string"},
                400
            )

        field_content = field_content.strip()

        if not field_content:
            return None, (
                {"error": f"{field} cannot be empty"},
                400
            )

        if field in ("email", "password"):
            validate_len_string(field_content, field, 256)
        else:
            validate_len_string(field_content, field, 51)

        all_field_content[field] = field_content

    return all_field_content, None


@users_bp.route("/", methods=["POST"])
def create_user():

    data = request.get_json(silent=True)

    all_field_content, error = validate_user_fields(data)

    if error:
        return error

    result = u.add_user(all_field_content)

    return success(result, 201)


@users_bp.route("/", methods=["PUT"])
def modify_user():

    data = request.get_json(silent=True)

    all_field_content, error = validate_user_fields(data)

    if error:
        return error

    if "user_id" not in data:
        return {"error": "user_id is required"}, 400

    all_field_content["user_id"] = validate_uuid(
        data["user_id"], "id"
    )

    result = u.modify_user(all_field_content)

    return success(result, 200)


    