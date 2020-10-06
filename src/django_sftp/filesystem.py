import logging
from typing import Any, Dict, List

import asyncssh
from django.conf import settings
from django.core.files.storage import get_storage_class as _get_storage_class
from six import text_type

logger = logging.getLogger(__name__)


class StoragePatch:
    """Base class for patches to StorageFS."""

    patch_methods: List[str] = []

    @classmethod
    def apply(cls, fs: Any) -> None:
        """replace bound methods of fs."""
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


class StorageFS(asyncssh.SFTPServer):
    """FileSystem for bridge to Django storage."""

    _cwd = None
    storage_class = None
    patches: Dict[str, Any] = {"FileSystemStorage": FileSystemStoragePatch}

    def apply_patch(self):
        """apply adjustment patch for storage"""
        patch = self.patches.get(self.storage.__class__.__name__)
        if patch:
            patch.apply(self)

    def __init__(self, chan):
        if not self._cwd:
            self._cwd = settings.MEDIA_ROOT
        self.storage = self.get_storage()
        self.apply_patch()
        super().__init__(chan, chroot=self._cwd)

    def get_storage_class(self):
        if self.storage_class is None:
            return _get_storage_class()
        return self.storage_class

    def get_storage(self):
        storage_class = self.get_storage_class()
        return storage_class()
