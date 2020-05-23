
Django SFTP [WIP]
===========

|Tests| |Codecov| |PyPI| |Python Version| |Read the Docs| |License| |Black| |pre-commit| |Dependabot|

.. |Tests| image:: https://github.com/vahaah/django-sftp/workflows/Tests/badge.svg
   :target: https://github.com/vahaah/django-sftp/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/vahaah/django-sftp/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/vahaah/django-sftp
   :alt: Codecov
.. |PyPI| image:: https://img.shields.io/pypi/v/django-sftp.svg
   :target: https://pypi.org/project/django-sftp/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/django-sftp
   :target: https://pypi.org/project/django-sftp
   :alt: Python Version
.. |Read the Docs| image:: https://readthedocs.org/projects/django-sftp/badge/
   :target: https://django-sftp.readthedocs.io/
   :alt: Read the Docs
.. |License| image:: https://img.shields.io/pypi/l/django-sftp
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=vahaah/django-sftp
   :target: https://dependabot.com
   :alt: Dependabot


Features
--------

* TODO


Requirements
------------

* TODO


Installation
------------

You can install *Django SFTP* via pip_ from PyPI_:

.. code:: console

   $ pip install django-sftp

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_sftp',
        ...
    )

Generate RSA key

.. code:: console

    $ ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -m PEM

Run SFTP server

.. code:: bash

    $ ./manage.py sftpserver :11121 -k /tmp/rsa


Usage
-----

* TODO


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT_ license,
*Django SFTP* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

.. _MIT: http://opensource.org/licenses/MIT
.. _file an issue: https://github.com/vahaah/django-sftp/issues
.. _pip: https://pip.pypa.io/
.. _Contributor Guide: CONTRIBUTING.rst
