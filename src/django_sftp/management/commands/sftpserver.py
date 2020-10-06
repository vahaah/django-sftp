import asyncio
import os
import sys

import asyncssh
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser

from django_sftp.filesystem import StorageFS
from django_sftp.interface import StubServer


async def start_server(host: str, port: str, keyfile: str) -> None:
    """Start SFTP server.

    Args:
        host (str): host, eg. 0.0.0.0
        port (str): port, eg. 21
        keyfile (str): RSA key path.
    """
    await asyncssh.create_server(
        StubServer, host, port, server_host_keys=[keyfile], sftp_factory=StorageFS,
    )


class Command(BaseCommand):
    """Django Command to start SFTP server. Runs as ./manage.py sftpserver."""

    help = "Start SFTP server"

    def add_arguments(self, parser: CommandParser) -> None:
        """Parse django command arguments.

        Args:
            parser (CommandParser): CommandParser instance
        """
        parser.add_argument("host_port", nargs="?")
        parser.add_argument(
            "-k",
            "--keyfile",
            dest="keyfile",
            metavar="FILE",
            help="Path to private key, for example /tmp/test_rsa.key",
        )

    def handle(self, *args, **options) -> None:
        """Django command handler."""
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        # bind host and port
        host_port = options.get("host_port", "")
        host, _port = host_port.split(":", 1)
        port = int(_port)

        keyfile = options["keyfile"]

        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(start_server(host, port, keyfile))
        except (OSError, asyncssh.Error) as exc:
            sys.exit("Error starting server: " + str(exc))

        loop.run_forever()
