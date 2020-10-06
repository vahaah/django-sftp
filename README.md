
Django SFTP [WIP]
===========


[![Tests](https://github.com/vahaah/django-sftp/workflows/Tests/badge.svg)](https://github.com/vahaah/django-sftp/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/vahaah/django-sftp/branch/master/graph/badge.svg)](https://codecov.io/gh/vahaah/django-sftp)
[![PyPI](https://img.shields.io/pypi/v/django-sftp.svg)](https://pypi.org/project/django-sftp/)
[![Python Version](https://img.shields.io/pypi/pyversions/django-sftp)](https://pypi.org/project/django-sftp/)
[![Read the Docs](https://readthedocs.org/projects/django-sftp/badge/)](https://django-sftp.readthedocs.io/)
[![License](https://img.shields.io/pypi/l/django-sftp)](https://opensource.org/licenses/MIT)
[![License](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Dependabot](https://api.dependabot.com/badges/status?host=github&repo=vahaah/django-sftp)](https://dependabot.com)


Features
--------

* TODO


Requirements
------------

* TODO


Getting Started
---------------

1.  Install django-sftp by pip.
```bash
$ pip install django-sftp
```

2. Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
   ...
   'django_sftp',
   ...
)
```

3. Migrate app.
```bash
$ ./manage.py migrate
```

4. Create user account.
```bash
$ ./manage.py createsuperuser --username user
```

5. Create SFTP user group.
```bash
$ ./manage.py createsftpusergroup test
```

6. Create SFTP account.
```bash
$ ./manage.py createftpuseraccount user test
```

7. Generate RSA key
```bash
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -m PEM
```

8. Run SFTP server
```bash
$ ./manage.py sftpserver :11121 -k rsa
```

Usage
-----

* TODO


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`.


License
-------

Distributed under the terms of the MIT_ license,
*Django SFTP* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue` along with a detailed description.


Credits
-------

* MIT: http://opensource.org/licenses/MIT
* file an issue: https://github.com/vahaah/django-sftp/issues
* pip: https://pip.pypa.io/
* Contributor Guide: CONTRIBUTING.rst
