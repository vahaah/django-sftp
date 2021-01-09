import typing

from . import models
from .compat import get_username_field


class UserAccountMixin:
    """Mixin contains methods to works with SFTP Account."""

    username = ""
    model = models.SFTPUserAccount
    username_field = get_username_field()

    def get_account(self, username: str) -> typing.Union[None, models.SFTPUserAccount]:
        """Return SFTP User by username.

        Args:
            username (str): username as string.

        Returns:
            typing.Union[None, models.SFTPUserAccount]: None or SFTP User instance.
        """
        try:
            account = self.model.objects.get(**self._filter_user_by(username))
        except self.model.DoesNotExist:
            return None
        return account

    def get_home_dir(self, username: str = "") -> str:
        """Get user home dir.

        Args:
            username (str): username as string.

        Returns:
            str: user home directory.
        """
        if not username:
            username = self.username
        account = self.get_account(username)
        if not account:
            return ""
        return account.get_home_dir()

    def _filter_user_by(self, username: str) -> dict:
        """Generate arguments for django filter.

        Args:
            username (str): username as string.

        Returns:
            dict: django filter arguments.
        """
        return {"user__%s" % self.username_field: username}
