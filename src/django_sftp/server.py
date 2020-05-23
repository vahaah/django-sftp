from paramiko import SFTPServerInterface, SFTPServer
from paramiko.common import DEBUG
from paramiko.sftp import Message, SFTP_OK

from django_sftp.filesystem import StorageFS


class StubSFTPServer(SFTPServer):
    def start_subsystem(self, name, transport, channel):
        self.sock = channel
        self._log(DEBUG, "Started sftp server on channel %s" % repr(channel))
        self._send_server_version()
        self.server.session_started()
        while True:
            try:
                t, data = self._read_packet()
            except EOFError:
                return
            except Exception:
                return
            msg = Message(data)
            request_number = msg.get_int()
            try:
                self._process(t, request_number, msg)
            except Exception:
                # send some kind of failure message, at least
                try:
                    self._send_status(request_number, SFTP_OK)
                except:
                    pass


class StubSFTPServerInterface(StorageFS, SFTPServerInterface):
    # assume current folder is a fine root
    # (the tests always create and eventualy delete a subfolder, so there shouldn't be any mess)

    def __init__(self, server, *largs, **kwargs) -> None:
        """
        Create a new SFTPServerInterface object.  This method does nothing by
        default and is meant to be overridden by subclasses.

        :param .ServerInterface server:
            the server object associated with this channel and SFTP subsystem
        """

        self.server_interface = server
        self._cwd = self.server_interface.get_home_dir()
        super(StubSFTPServerInterface, self).__init__(server, *largs, **kwargs)

    def session_started(self) -> None:
        """
        The SFTP server session has just started.  This method is meant to be
        overridden to perform any necessary setup before handling callbacks
        from SFTP operations.
        """
        pass

    def session_ended(self) -> None:
        """
        The SFTP server session has just ended, either cleanly or via an
        exception.  This method is meant to be overridden to perform any
        necessary cleanup before this `.SFTPServerInterface` object is
        destroyed.
        """
        pass
