# (c) Copyright 2018 ZTE Corporation
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

from freezerclient import exceptions
from freezerclient.v2 import backups as backups_cli
from freezerclient.v2.managers import backups


class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.mock_client = mock.Mock()
        self.mock_client.endpoint = 'http://testendpoint:9999'
        self.mock_client.project_id = 'tecs'
        self.mock_client.auth_token = 'testtoken'
        self.b = backups.BackupsManager(self.mock_client)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_create(self, mock_requests):
        self.assertEqual('http://testendpoint:9999/v2/tecs/backups/',
                         self.b.endpoint)
        self.assertEqual({'X-Auth-Token': 'testtoken',
                          'Content-Type': 'application/json',
                          'Accept': 'application/json'},
                         self.b.headers)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_create_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'backup_id': 'qwerqwer'}
        mock_requests.post.return_value = mock_response
        retval = self.b.create(backup_metadata={'backup': 'metadata'})
        self.assertEqual('qwerqwer', retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_create_fail_when_api_return_error_code(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_requests.post.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.create,
                          {'backup': 'metadata'})

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_delete_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_requests.delete.return_value = mock_response
        retval = self.b.delete('test_backup_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_delete_fail(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_requests.delete.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.delete,
                          'test_backup_id')

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_get_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'backup_id': 'qwerqwer'}
        mock_requests.get.return_value = mock_response
        retval = self.b.get('test_backup_id')
        self.assertEqual({'backup_id': 'qwerqwer'}, retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_get_none(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response
        retval = self.b.get('test_backup_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_get_error(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 403
        mock_requests.get.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.b.get, 'test_backup_id')

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_list_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        backup_list = [{'backup_id_0': 'qwerqwer'},
                       {'backup_id_1': 'asdfasdf'}]
        mock_response.json.return_value = {'backups': backup_list}
        mock_requests.get.return_value = mock_response
        retval = self.b.list()
        self.assertEqual(backup_list, retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
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
            'http://testendpoint:9999/v2/tecs/backups/',
            params={'limit': 5, 'offset': 5},
            data='{"time_before": 1428529956}',
            headers={'X-Auth-Token': 'testtoken',
                     'Content-Type': 'application/json',
                     'Accept': 'application/json'},
            verify=True)
        self.assertEqual(backup_list, retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_list_error(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        backup_list = [{'backup_id_0': 'qwerqwer'},
                       {'backup_id_1': 'asdfasdf'}]
        mock_response.json.return_value = {'backups': backup_list}
        mock_requests.get.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.list)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_update_ok(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        expected_doc = {'backup_id': 'test_backup_id', 'status': 'available'}
        mock_response.json.return_value = expected_doc
        mock_requests.patch.return_value = mock_response
        retval = self.b.update('test_backup_id', {'status': 'available'})
        self.assertEqual(expected_doc, retval)

    @mock.patch('freezerclient.v2.managers.backups.requests')
    def test_update_error(self, mock_requests):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_requests.patch.return_value = mock_response
        self.assertRaises(exceptions.ApiClientException, self.b.update,
                          'test_backup_id', {'status': 'completed'})


class TestBackupList(unittest.TestCase):
    def setUp(self):
        self.app = mock.Mock()
        self.cmd = backups_cli.BackupList(self.app, mock.Mock())

    def test_take_action_includes_status_column(self):
        self.app.client.backups.list.return_value = [{
            'backup_id': 'b1',
            'status': 'available',
            'backup_metadata': {
                'hostname': 'host1',
                'path_to_backup': '/tmp',
                'time_stamp': '1600000000',
                'curr_backup_level': 0
            }
        }]

        parsed_args = mock.Mock()
        parsed_args.limit = 10
        parsed_args.offset = 0
        parsed_args.search = ''

        columns, data = self.cmd.take_action(parsed_args)
        self.assertIn('Status', columns)
        self.assertNotIn('Backup UUID', columns)
        data_list = list(data)
        self.assertEqual('available', data_list[0][columns.index('Status')])
        self.assertEqual('b1', data_list[0][columns.index('Backup ID')])


class TestFormatBackup(unittest.TestCase):

    def test_format_backup_with_backup_id(self):
        backup = {
            'backup_id': 'b1',
            'project_id': 'p1',
            'user_id': 'u1',
            'status': 'available',
            'backup_metadata': {'hostname': 'host1'}
        }
        columns, data = backups_cli.format_backup(backup)
        self.assertEqual('Backup ID', columns[0])
        self.assertEqual('b1', data[0])

    def test_format_backup_with_backup_uuid_fallback(self):
        backup = {
            'backup_uuid': 'uuid1',
            'project_id': 'p1',
            'user_id': 'u1',
            'status': 'available',
            'backup_metadata': {'hostname': 'host1'}
        }
        columns, data = backups_cli.format_backup(backup)
        self.assertEqual('Backup ID', columns[0])
        self.assertEqual('uuid1', data[0])


class TestBackupShow(unittest.TestCase):

    def setUp(self):
        self.app = mock.Mock()
        self.app.client = mock.Mock()
        self.cmd = backups_cli.BackupShow(self.app, mock.Mock())

    def test_take_action(self):
        parsed_args = mock.Mock()
        parsed_args.backup_id = 'b1'
        self.app.client.backups.get.return_value = {
            'backup_id': 'b1',
            'project_id': 'p1',
            'user_id': 'u1',
            'status': 'available',
            'backup_metadata': {'hostname': 'host1'}
        }
        columns, data = self.cmd.take_action(parsed_args)
        self.app.client.backups.get.assert_called_once_with('b1')
        self.assertEqual('b1', data[0])

    def test_take_action_not_found(self):
        parsed_args = mock.Mock()
        parsed_args.backup_id = 'b1'
        self.app.client.backups.get.return_value = None
        self.assertRaises(exceptions.ApiClientException,
                          self.cmd.take_action, parsed_args)


class TestBackupDelete(unittest.TestCase):

    def setUp(self):
        self.app = mock.Mock()
        self.app.client = mock.Mock()
        self.cmd = backups_cli.BackupDelete(self.app, mock.Mock())

    def test_take_action(self):
        parsed_args = mock.Mock()
        parsed_args.backup_id = 'b1'
        self.cmd.take_action(parsed_args)
        self.app.client.backups.delete.assert_called_once_with('b1')
