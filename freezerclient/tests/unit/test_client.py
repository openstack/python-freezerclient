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

import mock
import unittest

from freezerclient import client
from freezerclient import v1
from freezerclient import v2


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.session = mock.Mock()

    def test_client_v1_endpoint(self):
        gc = client.Client(version='1', endpoint='http://freezer.org',
                           session=self.session)
        self.assertEqual("http://freezer.org", gc.opts.os_backup_url)
        self.assertIsInstance(gc, v1.client.Client)

    def test_client_v1_auth_url(self):
        gc = client.Client(version='1', auth_url='http://example.com',
                           endpoint='http://freezer.org',
                           session=self.session)
        self.assertEqual("http://freezer.org", gc.opts.os_backup_url)
        self.assertIsInstance(gc, v1.client.Client)

    def test_client_v1_username(self):
        gc = client.Client('1', endpoint='http://freezer.org',
                           username='caihui', session=self.session)
        self.assertEqual("caihui", gc.opts.os_username)
        self.assertIsInstance(gc, v1.client.Client)

    def test_client_v1_password(self):
        gc = client.Client('1', password='password',
                           endpoint='http://freezer.org',
                           session=self.session)
        self.assertEqual("password", gc.opts.os_password)
        self.assertIsInstance(gc, v1.client.Client)

    def test_client_v2_auth_url(self):
        gc = client.Client(version='2', auth_url='http://example.com',
                           session=self.session)
        self.assertEqual("http://example.com", gc.opts.os_auth_url)
        self.assertIsInstance(gc, v2.client.Client)

    def test_client_v2_endpoint(self):
        gc = client.Client(version='2', endpoint='http://freezer.org',
                           session=self.session)
        self.assertEqual("http://freezer.org", gc.opts.os_backup_url)
        self.assertIsInstance(gc, v2.client.Client)

    def test_client_v2_username(self):
        gc = client.Client('2', username='caihui', session=self.session)
        self.assertEqual("caihui", gc.opts.os_username)
        self.assertIsInstance(gc, v2.client.Client)

    def test_client_v2_password(self):
        gc = client.Client('2', password='password', session=self.session)
        self.assertEqual("password", gc.opts.os_password)
        self.assertIsInstance(gc, v2.client.Client)

    def test_client_v2_porject_name(self):
        gc = client.Client('2', project_name='tecs', session=self.session)
        self.assertEqual("tecs", gc.opts.os_project_name)
        self.assertIsInstance(gc, v2.client.Client)

    def test_client_default_version(self):
        gc = client.Client(session=self.session)
        self.assertIsInstance(gc, v2.client.Client)
