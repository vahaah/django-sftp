import logging
import typing
from typing import Any
from typing import Dict
from typing import List

import asyncssh
from django.core.files.storage import get_storage_class as _get_storage_class
from django.core.files.storage import Storage

from .mixins import UserAccountMixin

logger = logging.getLogger(__name__)


class StoragePatch:
    """Base class for patches to StorageFS."""

    patch_methods: List[str] = []

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

    patch_methods = []


class StorageFS(UserAccountMixin, asyncssh.SFTPServer):
    """FileSystem for bridge to Django storage."""

    _cwd: str = ""
    storage_class: typing.Union[None, Storage] = None
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

    def get_storage_class(self) -> Storage:
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
