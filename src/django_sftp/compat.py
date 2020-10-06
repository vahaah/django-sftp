from django.conf import settings


def get_user_model_path() -> str:
    """Get custom User model path.

    Returns:
        str: model path.
    """
    return getattr(settings, "AUTH_USER_MODEL", "auth.User")


def get_username_field() -> str:
    """Get custom username field.

    Returns:
        str: username field.
    """
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    return getattr(user_model, "USERNAME_FIELD", "username")
