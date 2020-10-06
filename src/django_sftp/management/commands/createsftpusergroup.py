import sys

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser

from django_sftp.models import SFTPUserGroup


class Command(BaseCommand):
    """Django Command to creare SFTP group. Runs as ./manage.py createsftpusergroup."""

    help = "Create SFTP user group"

    def add_arguments(self, parser: CommandParser) -> None:
        """Parse django command arguments.

        Args:
            parser (CommandParser): CommandParser instance
        """
        parser.add_argument("name")
        parser.add_argument("home_dir", nargs="?")

    def handle(self, *args, **options) -> None:
        """Django command handler."""
        name = options.get("name")
        home_dir = options.get("home_dir")

        if SFTPUserGroup.objects.filter(name=name).exists():
            raise CommandError(f"SFTP user group {name} is already exists.")

        group = SFTPUserGroup(name=name, home_dir=home_dir)
        group.save()

        sys.stdout.write(f"FTP user group pk={group.pk}, {name} was created.\n")
