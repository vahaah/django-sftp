import sys
import typing

import asyncssh
from django.contrib.auth import authenticate

from .mixins import UserAccountMixin


class StubServer(UserAccountMixin, asyncssh.SSHServer):
    """SFTP server interface based on asyncssh.SSHServer."""

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
