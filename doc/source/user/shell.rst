The :program:`freezer` Shell Utility

.. program:: freezer
.. highlight:: bash

The :program:`freezer` shell utility interacts with OpenStack Freezer API from the
command line. It supports the entirety of the OpenStack Freezer API.

You'll need to provide :program:`freezer` with your OpenStack Keystone user
information. You can do this with the `--os-username`, `--os-password`,
`--os-project-name` (`--os-project-id`), `--os-project-domain-name`
(`--os-project-domain-id`) and `--os-user-domain-name` (`--os-user-domain-id`)
options, but it's easier to just set them as environment variables by setting
some environment variables:

.. envvar:: OS_USERNAME

    Your OpenStack Keystone user name.

.. envvar:: OS_PASSWORD

    Your password.

.. envvar:: OS_PROJECT_NAME

    The name of project for work.

.. envvar:: OS_PROJECT_ID

    The ID of project for work.

.. envvar:: OS_PROJECT_DOMAIN_NAME

    The name of domain containing the project.

.. envvar:: OS_PROJECT_DOMAIN_ID

    The ID of domain containing the project.

.. envvar:: OS_USER_DOMAIN_NAME

    The user's domain name.

.. envvar:: OS_USER_DOMAIN_ID

    The user's domain ID.

.. envvar:: OS_AUTH_URL

    The OpenStack Keystone endpoint URL.

.. envvar:: OS_BACKUP_API_VERSION

    The OpenStack freezer API version.

.. envvar:: OS_REGION_NAME

    The Keystone region name. Defaults to the first region if multiple regions
    are available.

For example, in Bash you'd use::

    export OS_USERNAME=yourname
    export OS_PASSWORD=yadayadayada
    export OS_PROJECT_NAME=myproject
    export OS_PROJECT_DOMAIN_NAME=default
    export OS_USER_DOMAIN_NAME=default
    export OS_AUTH_URL=http://<url-to-openstack-keystone>/identity
    export OS_BACKUP_API_VERSION=2

From there, all shell commands take the form::

    freezer <command> [arguments...]

Run :program:`freezer help` to get a full list of all possible commands, and run
:program:`freezer help <command>` to get detailed help for that command.

Reference
---------

For more information, see the reference:

.. toctree::
   :maxdepth: 2

   /cli/freezer
