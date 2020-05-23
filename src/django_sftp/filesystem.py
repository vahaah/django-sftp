import logging
import os
import time
from collections import namedtuple

from django.core.files.storage import (
    get_storage_class as _get_storage_class
)
from paramiko import SFTP_OK, SFTPServer, SFTPAttributes, SFTP_OP_UNSUPPORTED
from six import text_type

from django_sftp.handler import StubSFTPHandle

logger = logging.getLogger(__name__)

PseudoStat = namedtuple(
    'PseudoStat',
    [
        'st_size', 'st_mtime', 'st_nlink', 'st_mode', 'st_uid', 'st_gid',
        'st_dev', 'st_ino', 'st_atime'
    ])


class StoragePatch:
    """Base class for patches to StorageFS.
    """
    patch_methods = ()
    
    @classmethod
    def apply(cls, fs):
        """replace bound methods of fs.
        """
        logger.debug(
            'Patching %s with %s.', fs.__class__.__name__, cls.__name__)
        fs._patch = cls
        for method_name in cls.patch_methods:
            # if fs hasn't method, raise AttributeError.
            origin = getattr(fs, method_name)
            method = getattr(cls, method_name)
            bound_method = method.__get__(fs, fs.__class__)
            setattr(fs, method_name, bound_method)
            setattr(fs, '_origin_' + method_name, origin)


class FileSystemStoragePatch(StoragePatch):
    """StoragePatch for Django's FileSystemStorage.
    """
    patch_methods = (
        'mkdir', 'rmdir',
    )
    
    def mkdir(self, path):
        os.mkdir(self.storage.path(path))
    
    def rmdir(self, path):
        os.rmdir(self.storage.path(path))


class S3Boto3StoragePatch(StoragePatch):
    """StoragePatch for S3Boto3Storage(provided by django-storages).
    """
    patch_methods = (
        '_exists', 'isdir', 'getmtime', 'remove', 'rename', 'readlink', 'symlink', 'mkdir',
        'rmdir', 'chattr'
    )
    
    def _exists(self, path):
        if path.endswith('/'):
            return True
        return self.storage.exists(path)
    
    def isdir(self, path):
        return not self.isfile(path)
    
    def getmtime(self, path):
        if self.isdir(path):
            return 0
        return self._origin_getmtime(path)
    
    def remove(self, path):
        path = self.realpath(path)
        try:
            self.storage.delete(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK
    
    def rename(self, oldpath, newpath):
        return SFTP_OP_UNSUPPORTED
    
    def readlink(self, path):
        return SFTP_OP_UNSUPPORTED
    
    def symlink(self, target_path, path):
        return SFTP_OP_UNSUPPORTED
    
    def mkdir(self, path, attr):
        return SFTP_OP_UNSUPPORTED
    
    def rmdir(self, path):
        return SFTP_OP_UNSUPPORTED
    
    def chattr(self, path, attr):
        return SFTP_OP_UNSUPPORTED


class StorageFS(object):
    """FileSystem for bridge to Django storage.
    """
    _cwd = None
    storage_class = None
    patches = {
        'FileSystemStorage': FileSystemStoragePatch,
        'S3Boto3Storage': S3Boto3StoragePatch
    }
    
    def apply_patch(self):
        """apply adjustment patch for storage
        """
        patch = self.patches.get(self.storage.__class__.__name__)
        if patch:
            patch.apply(self)
    
    def __init__(self, *args, **kwargs):
        if not self._cwd:
            self._cwd = os.getcwd()
        self.storage = self.get_storage()
        self.apply_patch()
    
    def get_storage_class(self):
        if self.storage_class is None:
            return _get_storage_class()
        return self.storage_class
    
    def get_storage(self):
        storage_class = self.get_storage_class()
        return storage_class()
    
    def open(self, path, flags, attr):
        path = self.realpath(path)
        if flags:
            f = self.storage.open(path, 'wb')
        else:
            f = self.storage.open(path, 'rb')
        fobj = StubSFTPHandle(flags)
        fobj.filename = path
        fobj.readfile = f
        fobj.writefile = f
        return fobj
    
    def list_folder(self, path):
        path = self.realpath(path)
        directories, files = self.storage.listdir(path)
        return [SFTPAttributes.from_stat(self.stat(os.path.join(path, name + '/'))) for name in directories if name] + [
            SFTPAttributes.from_stat(self.stat(os.path.join(path, name))) for name in files if name]
    
    def rmdir(self, path):
        raise NotImplementedError
    
    def remove(self, path):
        assert isinstance(path, text_type), path
        self.storage.delete(path)
    
    def stat(self, path):
        if self.isfile(path):
            st_mode = 0o0100770
        else:
            # directory
            st_mode = 0o0040770
        st_time = int(self.getmtime(path))
        return PseudoStat(
            st_size=self.getsize(path),
            st_mtime=st_time,
            st_atime=st_time,
            st_nlink=1,
            st_mode=st_mode,
            st_uid=1000,
            st_gid=1000,
            st_dev=0,
            st_ino=0,
        )
    
    lstat = stat
    
    def _exists(self, path):
        if path == '/':
            return self.storage.exists("")
        return self.storage.exists(path)
    
    def isfile(self, path):
        return self._exists(path) and not path.endswith('/')
    
    def readdir(self, path):
        return False
    
    
    def islink(self, path):
        return False
    
    def isdir(self, path):
        if path == '':
            return True
        elif path.endswith('/'):
            return self._exists(path)
        return self._exists(path + '/')
    
    def getsize(self, path):
        if self.isdir(path):
            return 0
        return self.storage.size(path)
    
    def getmtime(self, path):
        return time.mktime(self.storage.get_modified_time(path).timetuple())
    
    def realpath(self, path):
        _cwd = self._cwd
        if self._cwd.endswith('/'):
            _cwd = self._cwd[:-1]
        return _cwd + self.canonicalize(path)
    
    def lexists(self, path):
        return self._exists(path)
