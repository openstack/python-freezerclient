# (c) Copyright 2026 Cleura AB
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

import unittest
from unittest import mock

from freezerclient.v2.managers import base


class FakeManager(base.BaseManager):
    resource_name = 'fake_resource'


class TestBaseManager(unittest.TestCase):

    def setUp(self):
        self.mock_client = mock.MagicMock()
        self.mock_client.endpoint = 'http://freezer.api:8989'
        self.mock_client.project_id = 'test_project'
        self.mock_client.auth_token = 'test_token'
        self.manager = FakeManager(self.mock_client, verify=True)

    def test_endpoint_construction_without_v2(self):
        # Should append /v2/{project_id}/{resource}/
        self.assertEqual(
            'http://freezer.api:8989/v2/test_project/fake_resource/',
            self.manager.endpoint
        )

    def test_endpoint_construction_with_v2(self):
        # Should append /{resource}/ and avoid double v2
        self.mock_client.endpoint = 'http://freezer.api:8989/v2'
        self.assertEqual(
            'http://freezer.api:8989/v2/fake_resource/',
            self.manager.endpoint
        )

    def test_headers(self):
        expected = {
            'X-Auth-Token': 'test_token',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.assertEqual(expected, self.manager.headers)

    def test_methods_raise_not_implemented(self):
        self.assertRaises(NotImplementedError, self.manager.create)
        self.assertRaises(NotImplementedError, self.manager.delete)
        self.assertRaises(NotImplementedError, self.manager.list)
        self.assertRaises(NotImplementedError, self.manager.get)
        self.assertRaises(NotImplementedError, self.manager.update)
