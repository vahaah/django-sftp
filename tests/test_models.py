from django.test import TestCase
from django.utils import timezone


class UserAccountTest(TestCase):
    def _getOne(self):
        from django_sftp import models

        return models.SFTPUserAccount()

    def _getUser(self):
        from django.contrib.auth import models

        return models.User.objects.create()

    def test_update_last_login(self):
        account = self._getOne()
        value = timezone.now()
        account.update_last_login(value)
        self.assertEqual(account.last_login, value)

    def test_get_home_dir_from_account(self):
        account = self._getOne()
        account.home_dir = "/test/for/account/"
        self.assertEqual(account.get_home_dir(), account.home_dir)

    def test_get_username_no_user(self):
        account = self._getOne()
        self.assertEqual(account.get_username(), "")

    def test_get_username(self):
        user = self._getUser()
        user.username = "spam"
        account = self._getOne()
        account.user = user
        self.assertEqual(account.get_username(), "spam")


class UserAccountWithGroupTest(TestCase):
    def _getGroup(self):
        from django_sftp import models

        return models.SFTPUserGroup.objects.create()

    def _getOne(self):
        from django_sftp import models

        return models.SFTPUserAccount()

    def test_get_home_dir_from_group(self):
        group = self._getGroup()
        group.home_dir = "/test/for/group/"
        account = self._getOne()
        account.group = group
        self.assertEqual(account.get_home_dir(), group.home_dir)
