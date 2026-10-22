import services.authenticate_service as s
import services.userProfile_service as se

def profile_is_complete(user_id):
    """
    check if the profile and users are completed
    arg : user_id
    return : True or False
    """
    user = s.get_user_by_id(user_id)
    profile = se.get_user_profile_by_id_with_pictures(user_id)

    if not user and profile:
        return False

    required_user_field = [
        "email",
        "username",
        "last_name",
        "first_name"
    ]
    required_profile_field = [
            "age",
            "gender",
            "gender_ref",
            "bio",
            "picture_profile_index",
            "localisation",
            "tags"
    ]

    for field in required_user_field:
        value = field.value
        if not value:
            return False

    for field in required_profile_field:
        value = field.value
        if not value:
            return False

    return True