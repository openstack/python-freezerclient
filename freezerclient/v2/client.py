# (c) Copyright 2014-2016 Hewlett-Packard Development Company, L.P.
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

import socket

from keystoneauth1.identity import v2
from keystoneauth1.identity import v3
from keystoneauth1 import session as ksa_session

from freezerclient import utils
from freezerclient.v2.managers import actions
from freezerclient.v2.managers import backups
from freezerclient.v2.managers import clients
from freezerclient.v2.managers import jobs
from freezerclient.v2.managers import sessions

FREEZER_SERVICE_TYPE = 'backup'


def guess_auth_version(opts):
    """Guess keystone version to connect to"""
    if opts.os_identity_api_version == '3':
        return '3'
    elif opts.os_identity_api_version == '2.0':
        return '2.0'
    elif opts.os_auth_url.endswith('v3'):
        return '3'
    elif opts.os_auth_url.endswith('v2.0'):
        return '2.0'
    raise Exception('Please provide valid keystone auth url with valid'
                    ' keystone api version to use')


def get_auth_plugin(opts):
    """Create the right keystone connection depending on the version
    for the api, if username/password and token are provided, username and
    password takes precedence.
    """
    auth_version = guess_auth_version(opts)
    if opts.os_username:
        if auth_version == '3':
            return v3.Password(auth_url=opts.os_auth_url,
                               username=opts.os_username,
                               password=opts.os_password,
                               project_name=opts.os_project_name,
                               user_domain_name=opts.os_user_domain_name,
                               user_domain_id=opts.os_user_domain_id,
                               project_domain_name=opts.os_project_domain_name,
                               project_domain_id=opts.os_project_domain_id,
                               project_id=opts.os_project_id)
        elif auth_version == '2.0':
            return v2.Password(auth_url=opts.os_auth_url,
                               username=opts.os_username,
                               password=opts.os_password,
                               tenant_name=opts.os_tenant_name)
    elif opts.os_token:
        if auth_version == '3':
            return v3.Token(auth_url=opts.os_auth_url,
                            token=opts.os_token,
                            project_name=opts.os_project_name,
                            project_domain_name=opts.os_project_domain_name,
                            project_domain_id=opts.os_project_domain_id,
                            project_id=opts.os_project_id)
        elif auth_version == '2.0':
            return v2.Token(auth_url=opts.os_auth_url,
                            token=opts.os_token,
                            tenant_name=opts.os_tenant_name)
    raise Exception('Unable to determine correct auth method, please provide'
                    ' either username or token')


class Client(object):
    """Client for the OpenStack Disaster Recovery v1 API.
    """

    def __init__(self, version='3', token=None, username=None, password=None,
                 tenant_name=None, auth_url=None, session=None, endpoint=None,
                 endpoint_type=None, opts=None, project_name=None,
                 user_domain_name=None, user_domain_id=None,
                 project_domain_name=None, project_domain_id=None,
                 cert=None, cacert=None, insecure=False, project_id=None):
        """
        Initialize a new client for the Disaster Recovery v1 API.
        :param version: keystone version to use
        :param token: keystone token
        :param username: openstack username
        :param password: openstack password
        :param tenant_name: tenant
        :param auth_url: keystone-api endpoint
        :param session: keystone.Session
        :param endpoint: freezer-api endpoint
        :param endpoint_type: type of endpoint
        :param opts: a namespace to store all keystone data
        :param project_name: only for version 3
        :param tenant_id: only for version 2
        :param user_domain_name: only for version 3
        :param user_domain_id: only for version 3
        :param project_domain_name: only for version 3
        :param project_domain_id: only for version 3
        :param insecure: The verification arguments to pass to requests.
                       These are of the same form as requests expects,
                       so True or False to verify (or not) against system
                       certificates or a path to a bundle or CA certs to
                       check against or None for requests to
                       attempt to locate and use certificates. (optional,
                       defaults to True)
        :param cert: Path to cert
        :return: freezerclient.Client
        """

        self.project_id = project_id

        if opts is None:
            self.opts = utils.Namespace({})
            self.opts.os_token = token or None
            self.opts.os_username = username or None
            self.opts.os_password = password or None
            self.opts.os_tenant_name = tenant_name or None
            self.opts.os_auth_url = auth_url or None
            self.opts.os_backup_url = endpoint or None
            self.opts.os_endpoint_type = endpoint_type or None
            self.opts.os_project_name = project_name or None
            self.opts.os_project_id = project_id or None
            self.opts.os_user_domain_name = user_domain_name or None
            self.opts.os_user_domain_id = user_domain_id or None
            self.opts.os_project_domain_name = project_domain_name or None
            self.opts.os_project_domain_id = project_domain_id or None
            self.opts.auth_version = version
            self.opts.os_cacert = cacert or None
            self.opts.insecure = insecure
            self.opts.cert = cert
        else:
            self.opts = opts

        self.cert = cert
        self.cacert = cacert or self.opts.os_cacert
        self._session = session
        verify = self.opts.os_cacert
        if self.opts.insecure:
            verify = False

        self.validate()

        self.jobs = jobs.JobManager(self, verify=verify)
        self.clients = clients.ClientManager(self, verify=verify)
        self.backups = backups.BackupsManager(self, verify=verify)
        self.sessions = sessions.SessionManager(self, verify=verify)
        self.actions = actions.ActionManager(self, verify=verify)

    @utils.CachedProperty
    def session(self):
        if self._session:
            return self._session
        auth_plugin = get_auth_plugin(self.opts)
        return ksa_session.Session(auth=auth_plugin,
                                   verify=(self.cacert or
                                           not self.opts.insecure),
                                   cert=self.cert)

    @utils.CachedProperty
    def endpoint(self):
        if self.opts.os_backup_url:
            return self.opts.os_backup_url
        else:
            auth_ref = self.session.auth.get_auth_ref(self.session)
            endpoint = auth_ref.service_catalog.url_for(
                service_type=FREEZER_SERVICE_TYPE,
                interface=self.opts.os_endpoint_type,
            )
        return endpoint

    @property
    def auth_token(self):
        return self.session.get_token()

    @utils.CachedProperty
    def client_id(self):
        return '{0}_{1}'.format(self.session.get_project_id(),
                                socket.gethostname())

    def validate(self):
        """Validate that the client objects gets created correctly.
        :return: bool
        """
        if not self._session and self.opts.os_auth_url is None:
            raise Exception('OS_AUTH_URL should be provided.')
