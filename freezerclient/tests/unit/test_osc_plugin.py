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

from osc_lib import utils

from freezerclient.osc import plugin


class TestOscPlugin(unittest.TestCase):

    def test_plugin_variables(self):
        self.assertEqual('backup', plugin.API_NAME)
        self.assertEqual('os_backup_api_version', plugin.API_VERSION_OPTION)
        self.assertEqual('2', plugin.DEFAULT_API_VERSION)
        self.assertEqual(
            {'2': 'freezerclient.v2.client.Client'},
            plugin.API_VERSIONS
        )

    @mock.patch('freezerclient.v2.client.Client', autospec=True)
    def test_make_client(self, mock_client):
        mock_instance = mock.Mock()
        mock_instance.session = mock.Mock()
        mock_instance.session.verify = True
        mock_instance.interface = 'public'
        mock_instance.region_name = 'RegionOne'
        mock_instance.get_endpoint_for_service_type.return_value = (
            'fake_endpoint'
        )

        plugin.make_client(mock_instance)

        mock_instance.get_endpoint_for_service_type.assert_called_once_with(
            'backup',
            interface='public',
            region_name='RegionOne'
        )
        mock_client.assert_called_once_with(
            session=mock_instance.session,
            endpoint='fake_endpoint',
            insecure=False,
            cacert=None
        )

    @mock.patch('freezerclient.v2.client.Client', autospec=True)
    def test_make_client_insecure(self, mock_client):
        mock_instance = mock.Mock()
        mock_instance.session = mock.Mock()
        mock_instance.session.verify = False
        mock_instance.interface = 'public'
        mock_instance.region_name = 'RegionOne'
        mock_instance.get_endpoint_for_service_type.return_value = (
            'fake_endpoint'
        )

        plugin.make_client(mock_instance)

        mock_client.assert_called_once_with(
            session=mock_instance.session,
            endpoint='fake_endpoint',
            insecure=True,
            cacert=None
        )

    @mock.patch('freezerclient.v2.client.Client', autospec=True)
    def test_make_client_cacert(self, mock_client):
        mock_instance = mock.Mock()
        mock_instance.session = mock.Mock()
        mock_instance.session.verify = '/path/to/ca'
        mock_instance.interface = 'public'
        mock_instance.region_name = 'RegionOne'
        mock_instance.get_endpoint_for_service_type.return_value = (
            'fake_endpoint'
        )

        plugin.make_client(mock_instance)

        mock_client.assert_called_once_with(
            session=mock_instance.session,
            endpoint='fake_endpoint',
            insecure=False,
            cacert='/path/to/ca'
        )

    @mock.patch('freezerclient.v2.client.Client', autospec=True)
    def test_make_client_endpoint_not_found(self, mock_client):
        mock_instance = mock.Mock()
        mock_instance.session = mock.Mock()
        mock_instance.session.verify = True
        mock_instance.interface = 'public'
        mock_instance.region_name = 'RegionOne'
        mock_instance.get_endpoint_for_service_type.side_effect = (
            Exception('EndpointNotFound')
        )

        self.assertRaises(
            Exception,
            plugin.make_client,
            mock_instance
        )
        mock_client.assert_not_called()

    def test_build_option_parser(self):
        parser = mock.Mock()
        plugin.build_option_parser(parser)
        parser.add_argument.assert_called_once_with(
            '--os-backup-api-version',
            metavar='<backup-api-version>',
            default=utils.env('OS_BACKUP_API_VERSION', default='2'),
            help='Backup API version, default=2 (Env: OS_BACKUP_API_VERSION)'
        )

    def test_base_classes_client_standalone(self):
        from freezerclient.base import FreezerCommand

        class DummyCommand(FreezerCommand):
            def take_action(self, parsed_args):
                pass

        mock_app = mock.Mock(spec=['client'])
        mock_app.client = 'fake_client_standalone'

        cmd = DummyCommand(mock_app, None)
        self.assertEqual('fake_client_standalone', cmd.client)

    def test_base_classes_client_osc(self):
        from freezerclient.base import FreezerCommand

        class DummyCommand(FreezerCommand):
            def take_action(self, parsed_args):
                pass

        mock_app = mock.Mock(spec=['client_manager'])
        mock_app.client_manager = mock.Mock()
        mock_app.client_manager.backup = 'fake_client_osc'

        cmd = DummyCommand(mock_app, None)
        self.assertEqual('fake_client_osc', cmd.client)
