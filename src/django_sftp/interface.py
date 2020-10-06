import sys

import asyncssh
from django.contrib.auth import authenticate

from . import models
from .compat import get_username_field


class StubServer(asyncssh.SSHServer):
    model = models.SFTPUserAccount
    username_field = get_username_field()

    def connection_made(self, conn):
        print("SSH connection received from %s." % conn.get_extra_info("peername")[0])

    def connection_lost(self, exc):
        if exc:
            print("SSH connection error: " + str(exc), file=sys.stderr)
        else:
            print("SSH connection closed.")

    def begin_auth(self, username):
        return True

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        user = authenticate(**{self.username_field: username, "password": password})
        account = self.get_account(username)
        if not (user and account):
            return False
        return True

    def get_account(self, username):
        """return user by username."""
        try:
            account = self.model.objects.get(**self._filter_user_by(username))
        except self.model.DoesNotExist:
            return None
        return account

    def get_home_dir(self, username=None):
        if not username:
            username = self.username
        account = self.get_account(username)
        if not account:
            return ""
        return account.get_home_dir()

    def _filter_user_by(self, username: str) -> dict:
        return {"user__%s" % self.username_field: username}
