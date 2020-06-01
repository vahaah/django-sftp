import socket
import threading
import time
from typing import Dict, Any
import paramiko
from django.core.management.base import BaseCommand, CommandParser

from django_sftp.interface import StubServer
from django_sftp.server import StubSFTPServer, StubSFTPServerInterface

BACKLOG = 10


class ConnHandlerThd(threading.Thread):
    def __init__(self, conn: socket.socket, keyfile: str, *args, **kwargs) -> None:
        super(ConnHandlerThd, self).__init__(*args, **kwargs)
        self._conn = conn
        self._keyfile = keyfile

    def run(self) -> None:
        host_key = paramiko.RSAKey.from_private_key_file(self._keyfile)
        transport = paramiko.Transport(self._conn)
        transport.add_server_key(host_key)
        transport.set_subsystem_handler("sftp", StubSFTPServer, StubSFTPServerInterface)

        server = StubServer()
        transport.start_server(server=server)

        _ = transport.accept()
        while transport.is_active():
            time.sleep(1)


def start_server(host: str, port: int, keyfile: str, level: str) -> None:
    paramiko_level = getattr(paramiko.common, level)
    paramiko.common.logging.basicConfig(level=paramiko_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((host, port))
    server_socket.listen(BACKLOG)

    while True:
        conn, _ = server_socket.accept()
        srv_thd = ConnHandlerThd(conn, keyfile)
        srv_thd.setDaemon(True)
        srv_thd.start()


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
        # bind host and port
        host_port = options.get("host_port", "")
        host, _port = host_port.split(":", 1)
        port = int(_port)

        level = options["level"]
        keyfile = options["keyfile"]
        start_server(host, port, keyfile, level)
