import asyncio
import os
import sys

import asyncssh
from django.core.management.base import BaseCommand, CommandParser

from django_sftp.filesystem import StorageFS
from django_sftp.interface import StubServer


def handle_client(process):
    process.stdout.write(
        "Welcome to my SSH server, %s!\n" % process.get_extra_info("username")
    )
    process.exit(0)


async def start_server(host, port, keyfile):
    await asyncssh.create_server(
        StubServer,
        host,
        port,
        server_host_keys=[keyfile],
        process_factory=handle_client,
        sftp_factory=StorageFS,
    )


class Command(BaseCommand):
    help = "Start SFTP server"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("host_port", nargs="?")
        parser.add_argument(
            "-l",
            "--level",
            dest="level",
            default="DEBUG",
            help="Debug level: WARNING, INFO, DEBUG [default: %(default)s]",
        )
        parser.add_argument(
            "-k",
            "--keyfile",
            dest="keyfile",
            metavar="FILE",
            help="Path to private key, for example /tmp/test_rsa.key",
        )

    def handle(self, *args, **options) -> None:
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        # bind host and port
        host_port = options.get("host_port", "")
        host, _port = host_port.split(":", 1)
        port = int(_port)

        level = options["level"]
        keyfile = options["keyfile"]

        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(start_server(host, port, keyfile))
        except (OSError, asyncssh.Error) as exc:
            sys.exit("Error starting server: " + str(exc))

        loop.run_forever()
