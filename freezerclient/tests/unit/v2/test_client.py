# Copyright (c) 2018 ZTE Corporation.
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

from keystoneauth1 import loading as kaloading

from freezerclient.v2 import client


class TestClientMock(unittest.TestCase):

    @mock.patch.object(kaloading.session, 'Session', autospec=True)
    @mock.patch.object(kaloading, 'get_plugin_loader', autospec=True)
    def test_client_new(self, mock_ks_loader, mock_ks_session):
        session = mock_ks_session.return_value.load_from_options.return_value
        mock_ks_loader.return_value.load_from_options.return_value = 'auth'
        c = client.Client(endpoint='blabla', auth_url='blabla')
        self.assertIsInstance(c, client.Client)
        self.assertEqual(session, c.session)

    @mock.patch.object(kaloading.session, 'Session', autospec=True)
    @mock.patch.object(kaloading, 'get_plugin_loader', autospec=True)
    def test_client_new_with_kwargs_session(self, mock_ks_loader,
                                            mock_ks_session):
        mock_ks_loader.return_value.load_from_options.return_value = 'auth'
        mock_session = mock.Mock()
        kwargs = {'token': 'alpha',
                  'username': 'bravo',
                  'password': 'charlie',
                  'tenant_name': 'delta',
                  'auth_url': 'echo',
                  'endpoint': 'golf',
                  'session': mock_session}
        c = client.Client(**kwargs)
        self.assertIsInstance(c, client.Client)
        self.assertEqual('alpha', c.opts.os_token)
        self.assertEqual('bravo', c.opts.os_username)
        self.assertEqual('charlie', c.opts.os_password)
        self.assertEqual('delta', c.opts.os_tenant_name)
        self.assertEqual('echo', c.opts.os_auth_url)
        self.assertEqual(mock_session, c._session)
        self.assertEqual(mock_session, c.session)
        self.assertEqual('golf', c.endpoint)

    @mock.patch.object(kaloading.session, 'Session', autospec=True)
    @mock.patch.object(kaloading, 'get_plugin_loader', autospec=True)
    def test_client_new_with_kwargs_usename_password(self, mock_ks_loader,
                                                     mock_ks_session):
        session = mock_ks_session.return_value.load_from_options.return_value
        mock_ks_loader.return_value.load_from_options.return_value = 'auth'
        kwargs = {'auth_url': 'one',
                  'project_id': 'two',
                  'tenant_name': 'three',
                  'project_name': 'four',
                  'user_domain_id': 'five',
                  'user_domain_name': 'six',
                  'project_domain_id': 'senven',
                  'project_domain_name': 'eight',
                  'username': 'nine',
                  'password': 'ten'}

        c = client.Client(**kwargs)
        self.assertIsInstance(c, client.Client)
        self.assertEqual('one', c.opts.os_auth_url)
        self.assertEqual('two', c.opts.os_project_id)
        self.assertEqual('three', c.opts.os_tenant_name)
        self.assertEqual('four', c.opts.os_project_name)
        self.assertEqual('five', c.opts.os_user_domain_id)
        self.assertEqual('six', c.opts.os_user_domain_name)
        self.assertEqual('senven', c.opts.os_project_domain_id)
        self.assertEqual('eight', c.opts.os_project_domain_name)
        self.assertEqual('nine', c.opts.os_username)
        self.assertEqual('ten', c.opts.os_password)
        self.assertEqual(session, c.session)

    @mock.patch.object(kaloading.session, 'Session', autospec=True)
    @mock.patch.object(kaloading, 'get_plugin_loader', autospec=True)
    def test_client_new_with_kwargs_token(self, mock_ks_loader,
                                          mock_ks_session):
        session = mock_ks_session.return_value.load_from_options.return_value
        mock_ks_loader.return_value.load_from_options.return_value = 'auth'
        kwargs = {'auth_url': 'one',
                  'project_id': 'two',
                  'tenant_name': 'three',
                  'project_name': 'four',
                  'user_domain_id': 'five',
                  'user_domain_name': 'six',
                  'project_domain_id': 'senven',
                  'project_domain_name': 'eight',
                  'token': 'nine'}

        c = client.Client(**kwargs)
        self.assertIsInstance(c, client.Client)
        self.assertEqual('one', c.opts.os_auth_url)
        self.assertEqual('two', c.opts.os_project_id)
        self.assertEqual('three', c.opts.os_tenant_name)
        self.assertEqual('four', c.opts.os_project_name)
        self.assertEqual('five', c.opts.os_user_domain_id)
        self.assertEqual('six', c.opts.os_user_domain_name)
        self.assertEqual('senven', c.opts.os_project_domain_id)
        self.assertEqual('eight', c.opts.os_project_domain_name)
        self.assertEqual('nine', c.opts.os_token)
        self.assertEqual(session, c.session)

    @mock.patch.object(kaloading.session, 'Session', autospec=True)
    @mock.patch.object(kaloading, 'get_plugin_loader', autospec=True)
    def test_get_token(self, mock_ks_loader, mock_ks_session):
        mock_ks_loader.return_value.load_from_options.return_value = 'auth'
        mock_session = mock.Mock()
        mock_session.get_token.return_value = 'antaniX2'
        c = client.Client(session=mock_session, endpoint='justtest',
                          auth_url='blabla')
        self.assertIsInstance(c, client.Client)
        self.assertEqual(c.auth_token, 'antaniX2')

    @mock.patch('freezerclient.v2.client.socket')
    @mock.patch.object(kaloading.session, 'Session', autospec=True)
    @mock.patch.object(kaloading, 'get_plugin_loader', autospec=True)
    def test_get_client_id(self, mock_ks_loader, mock_ks_session,
                           mock_socket):
        mock_ks_loader.return_value.load_from_options.return_value = 'auth'
        mock_socket.gethostname.return_value = 'parmenide'
        mock_session = mock.Mock()
        mock_session.get_project_id.return_value = 'H2O'
        c = client.Client(session=mock_session, endpoint='justtest',
                          auth_url='blabla')
        self.assertIsInstance(c, client.Client)
        self.assertEqual(c.client_id, 'H2O_parmenide')
