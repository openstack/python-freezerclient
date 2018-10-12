# (c) Copyright 2018 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import sys

import fixtures
import six
import testtools
from testtools import matchers

from freezerclient import shell as openstack_shell


DEFAULT_USERNAME = 'username'
DEFAULT_PASSWORD = 'password'
DEFAULT_PROJECT_ID = 'tenant_id'
DEFAULT_PROJECT_NAME = 'tenant_name'
DEFAULT_AUTH_URL = 'http://127.0.0.1:5000/v2.0/'


class ShellTest(testtools.TestCase):

    FAKE_ENV = {
        'OS_USERNAME': DEFAULT_USERNAME,
        'OS_PASSWORD': DEFAULT_PASSWORD,
        'OS_TENANT_ID': DEFAULT_PROJECT_ID,
        'OS_TENANT_NAME': DEFAULT_PROJECT_NAME,
        'OS_PROJECT_ID': DEFAULT_PROJECT_ID,
        'OS_PROJECT_NAME': DEFAULT_PROJECT_NAME,
        'OS_AUTH_URL': DEFAULT_AUTH_URL,
    }

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        super(ShellTest, self).setUp()
        for var in self.FAKE_ENV:
            self.useFixture(
                fixtures.EnvironmentVariable(
                    var, self.FAKE_ENV[var]))

    def shell(self, argstr, check=False, expected_val=0):
        # expected_val is the expected return value after executing
        # the command in FreezerShell
        orig = (sys.stdout, sys.stderr)
        clean_env = {}
        _old_env, os.environ = os.environ, clean_env.copy()
        try:
            sys.stdout = six.moves.cStringIO()
            sys.stderr = six.moves.cStringIO()
            _shell = openstack_shell.FreezerShell()
            _shell.run(argstr.split())
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertEqual(expected_val, exc_value.code)
        finally:
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout, sys.stderr = orig
            os.environ = _old_env
        return stdout, stderr, _shell.options

    def test_help(self):
        required = 'usage:'
        help_text, stderr, _ = self.shell('help')
        self.assertThat(
            help_text,
            matchers.MatchesRegex(required))

    def test_help_on_subcommand(self):
        required = [
            '.*?^usage: .* job-list']
        stdout, stderr, _ = self.shell('help job-list')
        for r in required:
            self.assertThat(
                stdout,
                matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))

    def test_help_command(self):
        required = 'usage:'
        help_text, stderr, _ = self.shell('help action-create')
        self.assertThat(
            help_text,
            matchers.MatchesRegex(required))

    def test_run_incomplete_command(self):
        cmd = 'job-create'
        stdout, stderr, _ = self.shell(cmd, check=True, expected_val=2)
        search_str = "run job-create: error"
        self.assertTrue(any(search_str in string for string
                            in stderr.split('\n')))

    def test_set_os_backup_api_version(self):
        cmd = (
            '--os-backup-api-version 1 job-list')
        stdout, stderr, options = self.shell(cmd)
        self.assertEqual("1", options.os_backup_api_version)

    def test_default_os_backup_api_version(self):
        cmd = 'help job-list'
        stdout, stderr, options = self.shell(cmd)
        self.assertEqual("2", options.os_backup_api_version)

    def test_set_os_username_password(self):
        cmd = (
            '--os-username caihui --os-password stack  job-list')
        stdout, stderr, options = self.shell(cmd)
        self.assertEqual("caihui", options.os_username)
        self.assertEqual("stack", options.os_password)

    def test_set_os_project_name_id(self):
        cmd = (
            '--os-project-id tecs0000000001 \
             --os-project-name tecs   job-list')
        stdout, stderr, options = self.shell(cmd)
        self.assertEqual("tecs0000000001", options.os_project_id)
        self.assertEqual("tecs", options.os_project_name)

    def test_set_os_auth_url(self):
        cmd = (
            '--os-auth-url http://127.0.0.1:5001 job-list')
        stdout, stderr, options = self.shell(cmd)
        self.assertEqual("http://127.0.0.1:5001", options.os_auth_url)
