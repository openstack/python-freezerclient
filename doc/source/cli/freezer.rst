================================
:program:`freezer` CLI man page
================================

.. program:: freezer
.. highlight:: bash

SYNOPSIS
========

:program:`freezer` [options] <command> [command-options]

:program:`freezer help`

:program:`freezer help` <command>


DESCRIPTION
===========

The :program:`freezer` command line utility interacts with OpenStack Backup, Restore, and DR service (Freezer).

In order to use the CLI, you must provide your OpenStack username, password,
project (historically called tenant), and auth endpoint. You can use
configuration options ``--os-username``, ``--os-password``, ``--os-project-id``,
and ``--os-auth-url`` or set corresponding environment variables::

    export OS_USERNAME=user
    export OS_PASSWORD=pass
    export OS_PROJECT_ID=c373706f891f48019483f8bd6503c54b
    export OS_AUTH_URL=http://auth.example.com:5000/v2.0

The command line tool will attempt to reauthenticate using provided credentials
for every request. You can override this behavior by manually supplying an auth
token using ``--os-backup-url`` and ``--os-auth-token`` or by setting
corresponding environment variables::

    export OS_IMAGE_URL=http://freezer.example.org:9090/
    export OS_AUTH_TOKEN=3bdc4d3a03f44e3d8377fa247b0ad155

You can select an API version to use by ``--os-backup-api-version`` option or by
setting corresponding environment variable::

    export OS_BACKUP_API_VERSION=1

Default Freezer API used is v2.

OPTIONS
=======

To get a list of available commands and options run::

    freezer help

To get usage and options of a command::

    freezer help <command>


EXAMPLES
========

Get information about job-create command::

    freezer help job-create

See available actions::

    freezer job-list

Create new job::

    freezer job-create  --file /root/action-local-nova-with-vol.json --client
    ubuntu_c89bd80e25da4407a12bfc73daa47052

Describe a specific image::

    freezer job-show <Job-ID>

BUGS
====

Use the master OpenStack bug tracker,available at:
https://storyboard.openstack.org/#!/project/openstack/freezer.
