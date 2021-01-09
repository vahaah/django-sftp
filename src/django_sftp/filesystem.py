import logging
import os
from typing import Any, Dict, List, NoReturn, Optional, Type

import asyncssh
from django.core.files.storage import Storage
from django.core.files.storage import get_storage_class as _get_storage_class

from .mixins import UserAccountMixin

logger = logging.getLogger(__name__)


class StoragePatch:
    """Base class for patches to StorageFS."""

    patch_methods: List[str] = []

    storage: Storage

    @classmethod
    def apply(cls, fs: Any) -> None:
        """Replace bound methods of fs."""
        logger.debug("Patching %s with %s.", fs.__class__.__name__, cls.__name__)
        fs._patch = cls
        for method_name in cls.patch_methods:
            # if fs hasn't method, raise AttributeError.
            origin = getattr(fs, method_name)
            method = getattr(cls, method_name)
            bound_method = method.__get__(fs, fs.__class__)
            setattr(fs, method_name, bound_method)
            setattr(fs, "_origin_" + method_name, origin)


class FileSystemStoragePatch(StoragePatch):
    """StoragePatch for Django's FileSystemStorage."""

    patch_methods = ["mkdir", "rmdir", "stat"]

    def mkdir(self, path: bytes, attrs: asyncssh.SFTPAttrs) -> None:
        """The `mkdir` for `FileSystemStorage` implements method with `os.mkdir`.

        Args:
            path (bytes): path as bytes
            attrs (asyncssh.SFTPAttrs): SFTP attrs
        """
        mode = 0o777 if attrs.permissions is None else attrs.permissions
        os.mkdir(self.storage.path(path.decode()), mode)

    def rmdir(self, path: bytes) -> None:
        """The `rmdir` for `FileSystemStorage` implements method with `os.rmdir`.

        Args:
            path (bytes): path as bytes
        """
        os.rmdir(self.storage.path(path.decode()))

    def stat(self, path: bytes) -> Any:
        """The `stat` for `FileSystemStorage` implements method with `os.stat`.

        Args:
            path (bytes): path as bytes

        Returns:
            return os.stat object
        """
        return os.stat(self.storage.path(path.decode()))


class StorageFS(UserAccountMixin, asyncssh.SFTPServer):
    """FileSystem for bridge to Django storage."""

    _cwd: str = ""
    storage_class: Optional[Type[Storage]] = None
    patches: Dict[str, Any] = {"FileSystemStorage": FileSystemStoragePatch}

    def apply_patch(self) -> None:
        """Apply adjustment patch for storage."""
        patch = self.patches.get(self.storage.__class__.__name__)
        if patch:
            patch.apply(self)

    def __init__(self, chan: asyncssh.SSHServerChannel) -> None:
        """File System for bridge to Django storage."""
        if not self._cwd:
            self._cwd = self.get_home_dir(chan._conn._username)
        self.storage = self.get_storage()
        self.apply_patch()
        super().__init__(chan, chroot=self._cwd)

    def get_storage_class(self) -> Type[Storage]:
        """Get storage class from django settings.

        Returns:
            Storage: Storage class.
        """
        if self.storage_class is None:
            return _get_storage_class()
        return self.storage_class

    def get_storage(self) -> Storage:
        """Get storage instance.

        Returns:
            Storage: Storage instance.
        """
        storage_class = self.get_storage_class()
        return storage_class()

    def listdir(self, path: bytes) -> List[bytes]:
        """The `listdir` for `StorageFS` implements method with `storage.listdir`.

        Args:
            path (bytes): path as bytes

        Returns:
            return List[bytes]
        """
        directories, files = self.storage.listdir(path.decode())
        return (
            [b".", b".."]
            + [name.encode() for name in directories if name]
            + [name.encode() for name in files if name]
        )

    def mkdir(self, path: bytes, attrs: asyncssh.SFTPAttrs) -> NoReturn:
        """The `mkdir` for StorageFS should be implemented in storage level."""
        raise NotImplementedError

    def rmdir(self, path: bytes) -> NoReturn:
        """The `rmdir` for StorageFS should be implemented in storage level."""
        raise NotImplementedError

    def stat(self, path: bytes) -> Any:
        """The `stat` for StorageFS should be implemented in storage level."""
        raise NotImplementedError
