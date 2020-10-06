import sys
import typing

import asyncssh
from django.contrib.auth import authenticate

from . import models
from .compat import get_username_field


class StubServer(asyncssh.SSHServer):
    """SFTP server interface based on asyncssh.SSHServer."""

    model = models.SFTPUserAccount
    username_field = get_username_field()

    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        """Connection made event handler.

        Args:
            conn (asyncssh.SSHServerConnection): SSHServerConnection instance.
        """
        print("SSH connection received from %s." % conn.get_extra_info("peername")[0])

    def connection_lost(self, exc: typing.Union[None, Exception]) -> None:
        """Connection lost event handler.

        Args:
            exc (typing.Union[None, Exception]): Exception if error.
        """
        if exc:
            print("SSH connection error: " + str(exc), file=sys.stderr)
        else:
            print("SSH connection closed.")

    def begin_auth(self, username: str) -> bool:
        """Begin auth event handler.

        Args:
            username (str): username as string.

        Returns:
            bool: True if Ok
        """
        return True

    def password_auth_supported(self) -> bool:
        """Password auth supported event handler.

        Returns:
            bool: True if Ok
        """
        return True

    def validate_password(self, username: str, password: str) -> bool:
        """Validate password event handler.

        Args:
            username (str): username as string.
            password (str): password as string.

        Returns:
            bool: True if Ok
        """
        user = authenticate(**{self.username_field: username, "password": password})
        account = self.get_account(username)
        if not (user and account):
            return False
        return True

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
