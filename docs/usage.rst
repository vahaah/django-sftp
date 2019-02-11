=====
Usage
=====

To use Django SFTP Server in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_sftp',
        ...
    )

Add Django SFTP Server's URL patterns:

.. code-block:: python

    from django_sftp import urls as django_sftp_urls


    urlpatterns = [
        ...
        url(r'^', include(django_sftp_urls)),
        ...
    ]
