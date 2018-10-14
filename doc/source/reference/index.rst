The :mod:`freezerclient` Python API

.. module:: freezerclient
   :synopsis: A client for the OpenStack Freezer API.

.. currentmodule:: freezerclient

Basic Usage
-----------

First create a client instance using a keystoneauth Session. For more
information on this keystoneauth API, see `Using Sessions`_.

.. _Using Sessions: https://docs.openstack.org/keystoneauth/latest/using-sessions.html

.. code-block:: python

    >>> from keystoneauth1 import identity
    >>> from keystoneauth1 import session
    >>> from freezerclient import client
    >>> username='username'
    >>> password='password'
    >>> project_name='demo'
    >>> project_domain_id='default'
    >>> user_domain_id='default'
    >>> auth_url='http://auth.example.com:5000/v3'
    >>> auth = identity.Password(auth_url=auth_url,
    ...                          username=username,
    ...                          password=password,
    ...                          project_name=project_name,
    ...                          project_domain_id=project_domain_id,
    ...                          user_domain_id=user_domain_id)
    >>> sess = session.Session(auth=auth)
    >>> freezer = client.Client(version='2',session=sess)

It is also possible to use an instance as a context manager in which case
there will be a session kept alive for the duration of the with statement::

    >>> from freezerclient import client
    >>> freezer = client.Client('2')
    >>> freezer.jobs.list_all()
