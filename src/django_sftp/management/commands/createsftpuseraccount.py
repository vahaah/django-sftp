import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser

from django_sftp.compat import get_username_field
from django_sftp.models import SFTPUserAccount
from django_sftp.models import SFTPUserGroup


class Command(BaseCommand):
    """Django Command to creare SFTP account.

    Runs as ./manage.py createsftpuseraccount.
    """

    help = "Create SFTP user account"

    def add_arguments(self, parser: CommandParser) -> None:
        """Parse django command arguments.

        Args:
            parser (CommandParser): CommandParser instance
        """
        parser.add_argument("username")
        parser.add_argument("group")
        parser.add_argument("home_dir", nargs="?")

    def handle(self, *args, **options) -> None:
        """Django command handler."""
        username = options.get("username")
        group_name = options.get("group")
        home_dir = options.get("home_dir")

        if SFTPUserAccount.objects.filter(user__username=username).exists():
            raise CommandError(f'FTP user account "{username}" is already exists.')

        user_model = get_user_model()
        try:
            user = user_model.objects.get(**{get_username_field(): username})
        except user_model.DoesNotExist:
            raise CommandError(f'User "{username}" is not exists.')

        try:
            group = SFTPUserGroup.objects.get(name=group_name)
        except SFTPUserGroup.DoesNotExist:
            raise CommandError(f'FTP user group "{group_name}" is not exists.')

        account = SFTPUserAccount.objects.create(
            user=user, group=group, home_dir=home_dir
        )

        sys.stdout.write(
            f'FTP user account pk={account.pk}, "{username}" was created.\n',
        )
