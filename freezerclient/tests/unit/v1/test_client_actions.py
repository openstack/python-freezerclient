# (c) Copyright 2014,2015,2016 Hewlett-Packard Development Company, L.P.
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

import mock

from freezerclient import exceptions
from freezerclient.v1.managers import actions


class TestActionManager(unittest.TestCase):
    def setUp(self):
        self.mock_client = mock.Mock()
        self.mock_response = mock.Mock()
        self.mock_client.endpoint = 'http://testendpoint:9999'
        self.mock_client.auth_token = 'testtoken'
        self.mock_client.client_id = 'test_client_id_78900987'
        self.action_manager = actions.ActionManager(self.mock_client)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_create(self, mock_requests):
        self.assertEqual('http://testendpoint:9999/v1/actions/',
                         self.action_manager.endpoint)
        self.assertEqual({'X-Auth-Token': 'testtoken',
                          'Content-Type': 'application/json',
                          'Accept': 'application/json'},
                         self.action_manager.headers)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_create_ok(self, mock_requests):
        self.mock_response.status_code = 201
        self.mock_response.json.return_value = {'action_id': 'qwerqwer'}
        mock_requests.post.return_value = self.mock_response
        retval = self.action_manager.create({'action': 'metadata'})
        self.assertEqual('qwerqwer', retval)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_create_fail_when_api_return_error_code(self, mock_requests):
        self.mock_response.status_code = 500
        mock_requests.post.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.action_manager.create, {'action': 'metadata'})

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_delete_ok(self, mock_requests):
        self.mock_response.status_code = 204
        mock_requests.delete.return_value = self.mock_response
        retval = self.action_manager.delete('test_action_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_delete_fail(self, mock_requests):
        self.mock_response.status_code = 500
        mock_requests.delete.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.action_manager.delete, 'test_action_id')

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_get_ok(self, mock_requests):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {'action_id': 'qwerqwer'}
        mock_requests.get.return_value = self.mock_response
        retval = self.action_manager.get('test_action_id')
        self.assertEqual({'action_id': 'qwerqwer'}, retval)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_get_fails_on_error_different_from_404(self, mock_requests):
        self.mock_response.status_code = 500
        mock_requests.get.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.action_manager.get, 'test_action_id')

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_get_none(self, mock_requests):
        self.mock_response.status_code = 404
        mock_requests.get.return_value = self.mock_response
        retval = self.action_manager.get('test_action_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_list_ok(self, mock_requests):
        self.mock_response.status_code = 200
        action_list = [{'action_id_0': 'bomboloid'},
                       {'action_id_1': 'asdfasdf'}]
        self.mock_response.json.return_value = {'actions': action_list}
        mock_requests.get.return_value = self.mock_response
        retval = self.action_manager.list()
        self.assertEqual(action_list, retval)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_list_error(self, mock_requests):
        self.mock_response.status_code = 404
        action_list = [{'action_id_0': 'bomboloid'},
                       {'action_id_1': 'asdfasdf'}]
        self.mock_response.json.return_value = {'clients': action_list}
        mock_requests.get.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.action_manager.list)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_update_ok(self, mock_requests):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {
            "patch": {"status": "bamboozled"},
            "version": 12,
            "action_id": "d454beec-1f3c-4d11-aa1a-404116a40502"
        }
        mock_requests.patch.return_value = self.mock_response
        retval = self.action_manager.update(
            'd454beec-1f3c-4d11-aa1a-404116a40502', {'status': 'bamboozled'})
        self.assertEqual(12, retval)

    @mock.patch('freezerclient.v1.managers.actions.requests')
    def test_update_raise_MetadataUpdateFailure_when_api_return_error_code(
            self, mock_requests):
        self.mock_response.json.return_value = {
            "patch": {"status": "bamboozled"},
            "version": 12,
            "action_id": "d454beec-1f3c-4d11-aa1a-404116a40502"
        }
        self.mock_response.status_code = 404
        self.mock_response.text = (
            '{"title": "Not Found","description":"No document found with ID '
            'd454beec-1f3c-4d11-aa1a-404116a40502x"}'
        )
        mock_requests.patch.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.action_manager.update,
                          'd454beec-1f3c-4d11-aa1a-404116a40502',
                          {'status': 'bamboozled'})
