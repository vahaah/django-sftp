from unittest import mock
from django.test import TestCase
from django.core.files.storage import Storage
from django_sftp.filesystem import StorageFS
from asyncssh import SFTPAttrs


class FileSystemStorageTest(TestCase):
    @mock.patch("asyncssh.SSHServerChannel")
    def test_fs_initialisation(self, channel):
        fs = StorageFS(channel)
        self.assertEqual("", fs._cwd)
        self.assertTrue(isinstance(fs.storage, Storage))
        self.assertEqual(fs.storage.__class__.__name__, "FileSystemStorage")

    @mock.patch("asyncssh.SSHServerChannel")
    def test_file_system_storage(self, channel):
        fs = StorageFS(channel)

        fs.rmdir("user1".encode())
        fs.mkdir("user1".encode(), SFTPAttrs())
        self.assertEqual(
            fs.listdir("".encode()), [b".", b"..", b"user1", b".gitkeep"]
        )

