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


from freezerclient.v1 import client


class TestSupportFunctions(unittest.TestCase):

    def test_guess_auth_version_returns_none(self):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = ''
        mock_opts.os_auth_url = ''
        self.assertRaises(Exception, client.guess_auth_version, mock_opts)

    def test_guess_auth_version_explicit_3(self):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '3'
        self.assertEqual(client.guess_auth_version(mock_opts), '3')

    def test_guess_auth_version_explicit_2(self):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '2.0'
        self.assertEqual(client.guess_auth_version(mock_opts), '2.0')

    def test_guess_auth_version_implicit_3(self):
        mock_opts = mock.Mock()
        mock_opts.os_auth_url = 'http://whatever/v3'
        self.assertEqual(client.guess_auth_version(mock_opts), '3')

    def test_guess_auth_version_implicit_2(self):
        mock_opts = mock.Mock()
        mock_opts.os_auth_url = 'http://whatever/v2.0'
        self.assertEqual(client.guess_auth_version(mock_opts), '2.0')

    @mock.patch('freezerclient.v1.client.v3')
    @mock.patch('freezerclient.v1.client.v2')
    def test_get_auth_plugin_v3_Password(self, mock_v2, mock_v3):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '3'
        mock_opts.os_user_name = 'myuser'
        mock_opts.os_token = ''
        client.get_auth_plugin(mock_opts)
        self.assertTrue(mock_v3.Password.called)

    @mock.patch('freezerclient.v1.client.v3')
    @mock.patch('freezerclient.v1.client.v2')
    def test_get_auth_plugin_v3_Token(self, mock_v2, mock_v3):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '3'
        mock_opts.os_username = ''
        mock_opts.os_token = 'mytoken'
        client.get_auth_plugin(mock_opts)
        self.assertTrue(mock_v3.Token.called)

    @mock.patch('freezerclient.v1.client.v3')
    @mock.patch('freezerclient.v1.client.v2')
    def test_get_auth_plugin_v2_Password(self, mock_v2, mock_v3):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '2.0'
        mock_opts.os_user_name = 'myuser'
        mock_opts.os_token = ''
        client.get_auth_plugin(mock_opts)
        self.assertTrue(mock_v2.Password.called)

    @mock.patch('freezerclient.v1.client.v3')
    @mock.patch('freezerclient.v1.client.v2')
    def test_get_auth_plugin_v2_Token(self, mock_v2, mock_v3):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '2.0'
        mock_opts.os_username = ''
        mock_opts.os_token = 'mytoken'
        client.get_auth_plugin(mock_opts)
        self.assertTrue(mock_v2.Token.called)

    @mock.patch('freezerclient.v1.client.v3')
    @mock.patch('freezerclient.v1.client.v2')
    def test_get_auth_plugin_raises_when_no_username_token(self, mock_v2,
                                                           mock_v3):
        mock_opts = mock.Mock()
        mock_opts.os_identity_api_version = '2.0'
        mock_opts.os_username = ''
        mock_opts.os_token = ''
        self.assertRaises(Exception, client.get_auth_plugin, mock_opts)


class TestClientMock(unittest.TestCase):

    @mock.patch('freezerclient.v1.client.ksa_session')
    @mock.patch('freezerclient.v1.client.get_auth_plugin')
    def test_client_new(self, mock_get_auth_plugin, mock_ksa_session):
        c = client.Client(endpoint='blabla', auth_url='blabla')
        self.assertIsInstance(c, client.Client)

    @mock.patch('freezerclient.v1.client.ksa_session')
    @mock.patch('freezerclient.v1.client.get_auth_plugin')
    def test_client_new_with_kwargs(self, mock_get_auth_plugin,
                                    mock_ksa_session):
        kwargs = {'token': 'alpha',
                  'username': 'bravo',
                  'password': 'charlie',
                  'tenant_name': 'delta',
                  'auth_url': 'echo',
                  'session': 'foxtrot',
                  'endpoint': 'golf',
                  'version': 'hotel'}
        c = client.Client(**kwargs)
        self.assertIsInstance(c, client.Client)
        self.assertEqual('alpha', c.opts.os_token)
        self.assertEqual('bravo', c.opts.os_username)
        self.assertEqual('charlie', c.opts.os_password)
        self.assertEqual('delta', c.opts.os_tenant_name)
        self.assertEqual('echo', c.opts.os_auth_url)
        self.assertEqual('foxtrot', c._session)
        self.assertEqual('foxtrot', c.session)
        self.assertEqual('golf', c.endpoint)

    @mock.patch('freezerclient.v1.client.ksa_session')
    @mock.patch('freezerclient.v1.client.get_auth_plugin')
    def test_get_token(self, mock_get_auth_plugin, mock_ksa_session):
        mock_session = mock.Mock()
        mock_session.get_token.return_value = 'antaniX2'
        c = client.Client(session=mock_session, endpoint='justtest',
                          auth_url='blabla')
        self.assertIsInstance(c, client.Client)
        self.assertEqual(c.auth_token, 'antaniX2')

    @mock.patch('freezerclient.v1.client.socket')
    @mock.patch('freezerclient.v1.client.ksa_session')
    @mock.patch('freezerclient.v1.client.get_auth_plugin')
    def test_get_client_id(self, mock_get_auth_plugin, mock_ksa_session,
                           mock_socket):
        mock_socket.gethostname.return_value = 'parmenide'
        mock_session = mock.Mock()
        mock_session.get_project_id.return_value = 'H2O'
        c = client.Client(session=mock_session, endpoint='justtest',
                          auth_url='blabla')
        self.assertIsInstance(c, client.Client)
        self.assertEqual(c.client_id, 'H2O_parmenide')
