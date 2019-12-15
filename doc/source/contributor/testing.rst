Testing

The preferred way to run the unit tests is using ``tox``. There are multiple
test targets that can be run to validate the code.

``tox -e pep8``
  Style guidelines enforcement.

``tox -e py37``
  Traditional unit testing (Python 3.7).

``tox -e cover``
  Generate a coverage report on unit testing.

Functional testing assumes the existence of a `clouds.yaml` file as supported
by `os-client-config <https://docs.openstack.org/os-client-config/latest>`__
It assumes the existence of a cloud named `devstack` that behaves like a normal
DevStack installation with a demo and an admin user/tenant - or clouds named
`functional_admin` and `functional_nonadmin`.

Refer to  `Consistent Testing Interface`__ for more details.

__ https://opendev.org/openstack/governance/src/branch/master/reference/project-testing-interface.rst

Refer to  `Tester Use`__ for more details.

__ https://wiki.openstack.org/wiki/Testr
