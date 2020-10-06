import sys

from django.core.management.base import BaseCommand, CommandError

from django_sftp.models import SFTPUserGroup


class Command(BaseCommand):
    help = "Create SFTP user group"

    def add_arguments(self, parser):
        parser.add_argument("name")
        parser.add_argument("home_dir", nargs="?")

    def handle(self, *args, **options):
        name = options.get("name")
        home_dir = options.get("home_dir")

        if SFTPUserGroup.objects.filter(name=name).exists():
            raise CommandError(f"SFTP user group {name} is already exists.")

        group = SFTPUserGroup(name=name, home_dir=home_dir)
        group.save()

        sys.stdout.write(f"FTP user group pk={group.pk}, {name} was created.\n")
