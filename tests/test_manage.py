import random

import pytest
from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase


class TestManage(TestCase):
    def _createUserWithUsername(self, username):
        from django.contrib.auth import models

        return models.User.objects.create(username=username)

    def _createSftpUserGroupWithName(self, name):
        from django_sftp import models

        return models.SFTPUserGroup.objects.create(name=name)

    def _createSftpUserAccountWithUser(self, user):
        from django_sftp import models

        return models.SFTPUserAccount.objects.create(user=user)

    def test_run_sftpserver(self):
        with pytest.raises(CommandError):
            # Test that management commands work - but without actually running one
            management.call_command("sftpserver", "--passive-ports=fake")

    @pytest.mark.django_db
    def test_createsftpusergroup(self):
        random_name = "".join(random.choice("abcde") for _ in range(10))
        management.call_command("createsftpusergroup", random_name)

    def test_createsftpuseraccount(self):
        user = self._createUserWithUsername("test")
        group = self._createSftpUserGroupWithName("test")
        management.call_command("createsftpuseraccount", user.username, group.name)
