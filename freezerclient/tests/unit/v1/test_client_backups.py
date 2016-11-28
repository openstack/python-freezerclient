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
from freezerclient.v1.managers import backups


class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.mock_client = mock.Mock()
        self.mock_client.endpoint = 'http://testendpoint:9999'
        self.mock_client.auth_token = 'testtoken'
        self.b = backups.BackupsManager(self.mock_client)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_create(self, mock_requests):
        self.assertEqual('http://testendpoint:9999/v1/backups/',
                         self.b.endpoint)
        self.assertEqual({'X-Auth-Token': 'testtoken',
                          'Content-Type': 'application/json',
                          'Accept': 'application/json'},
                         self.b.headers)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_create_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'backup_id': 'qwerqwer'}
        mock_requests.post.return_value = mock_response
        retval = self.b.create(backup_metadata={'backup': 'metadata'})
        self.assertEqual('qwerqwer', retval)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_create_fail_when_api_return_error_code(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_requests.post.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.create,
                          {'backup': 'metadata'})

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_delete_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_requests.delete.return_value = mock_response
        retval = self.b.delete('test_backup_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_delete_fail(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_requests.delete.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.delete,
                          'test_backup_id')

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_get_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'backup_id': 'qwerqwer'}
        mock_requests.get.return_value = mock_response
        retval = self.b.get('test_backup_id')
        self.assertEqual({'backup_id': 'qwerqwer'}, retval)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_get_none(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response
        retval = self.b.get('test_backup_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_get_error(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 403
        mock_requests.get.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.b.get, 'test_backup_id')

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_list_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        backup_list = [{'backup_id_0': 'qwerqwer'},
                       {'backup_id_1': 'asdfasdf'}]
        mock_response.json.return_value = {'backups': backup_list}
        mock_requests.get.return_value = mock_response
        retval = self.b.list()
        self.assertEqual(backup_list, retval)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_list_parameters(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        backup_list = [{'backup_id_0': 'qwerqwer'},
                       {'backup_id_1': 'asdfasdf'}]
        mock_response.json.return_value = {'backups': backup_list}
        mock_requests.get.return_value = mock_response
        retval = self.b.list(limit=5,
                             offset=5,
                             search={"time_before": 1428529956})
        mock_requests.get.assert_called_with(
            'http://testendpoint:9999/v1/backups/',
            params={'limit': 5, 'offset': 5},
            data='{"time_before": 1428529956}',
            headers={'X-Auth-Token': 'testtoken',
                     'Content-Type': 'application/json',
                     'Accept': 'application/json'},
            verify=True)
        self.assertEqual(backup_list, retval)

    @mock.patch('freezerclient.v1.managers.backups.requests')
    def test_list_error(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        backup_list = [{'backup_id_0': 'qwerqwer'},
                       {'backup_id_1': 'asdfasdf'}]
        mock_response.json.return_value = {'backups': backup_list}
        mock_requests.get.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.list)
