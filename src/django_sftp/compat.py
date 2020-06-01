"""
The `compat` module provides support for backwards compatibility
with older versions of django
"""

from django.conf import settings


def get_user_model_path() -> str:
    return getattr(settings, "AUTH_USER_MODEL", None) or "auth.User"


def get_username_field() -> str:
    from django.contrib.auth import get_user_model

    UserModel = get_user_model()
    return getattr(UserModel, "USERNAME_FIELD", "username")
