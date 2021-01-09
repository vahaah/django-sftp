# -*- coding: utf-8 -*-
import typing
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SFTPUserGroup(models.Model):
    """SFTP Group DB model."""

    name = models.CharField(
        _("Group name"), max_length=30, null=False, blank=False, unique=True
    )
    home_dir = models.CharField(
        _("Home directory"), max_length=1024, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("SFTP user group")
        verbose_name_plural = _("SFTP user groups")


class SFTPUserAccount(models.Model):
    """SFTP Account DB model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        SFTPUserGroup,
        verbose_name=_("SFTP user group"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    last_login = models.DateTimeField(_("Last login"), editable=False, null=True)
    home_dir = models.CharField(
        _("Home directory"), max_length=1024, null=True, blank=True
    )

    def __str__(self) -> str:
        try:
            user = self.user
        except ObjectDoesNotExist:
            user = ""
        return f"{user}"

    def get_username(self) -> str:
        """Get username or empty string."""
        try:
            user = self.user
        except ObjectDoesNotExist:
            user = ""
        return user and user.username or ""

    def update_last_login(self, value: typing.Union[datetime, None] = None) -> None:
        """Update last login datetime.

        Args:
            value (typing.Union[datetime, None], optional): Custom datetime.
        """
        self.last_login = value or timezone.now()

    def get_home_dir(self) -> str:
        """Get user home directory."""
        if self.home_dir:
            directory = self.home_dir
        elif self.group and self.group.home_dir:
            directory = self.group.home_dir
        else:
            directory = settings.MEDIA_ROOT
        return directory

    class Meta:
        verbose_name = _("SFTP user account")
        verbose_name_plural = _("SFTP user accounts")
