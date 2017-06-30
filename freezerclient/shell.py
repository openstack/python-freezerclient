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

import logging
import os
import sys

from cliff import app
from cliff import commandmanager

import freezerclient
from freezerclient.v1 import client as v1_client
from freezerclient.v2 import client as v2_client


log = logging.getLogger(__name__)
# Suppress output from requests
logging.getLogger('requests').setLevel(logging.WARN)


def check_api_version():
    """Check freezer version API to use
    1: not multi-tenant, useful for infrastructure
    2: multi-tenant, useful for backup as a service
    :return: str
    """
    freezer_api_version = os.environ.get('OS_BACKUP_API_VERSION', '1')
    if freezer_api_version == '1':
        return '1'
    elif freezer_api_version == '2':
        return '2'
    else:
        raise Exception('Freezer API version not supported')


class FreezerCommandManager(commandmanager.CommandManager):
    """All commands available for the shell are registered here"""
    if check_api_version() == '1':
        from freezerclient.v1 import actions
        from freezerclient.v1 import backups
        from freezerclient.v1 import clients
        from freezerclient.v1 import jobs
        from freezerclient.v1 import sessions
    else:
        from freezerclient.v2 import actions
        from freezerclient.v2 import backups
        from freezerclient.v2 import clients
        from freezerclient.v2 import jobs
        from freezerclient.v2 import sessions

    SHELL_COMMANDS = {
        'job-show': jobs.JobShow,
        'job-list': jobs.JobList,
        'job-create': jobs.JobCreate,
        'job-get': jobs.JobGet,
        'job-delete': jobs.JobDelete,
        'job-start': jobs.JobStart,
        'job-stop': jobs.JobStop,
        'job-abort': jobs.JobAbort,
        'job-update': jobs.JobUpdate,
        'client-list': clients.ClientList,
        'client-show': clients.ClientShow,
        'client-register': clients.ClientRegister,
        'client-delete': clients.ClientDelete,
        'backup-list': backups.BackupList,
        'backup-show': backups.BackupShow,
        'backup-delete': backups.BackupDelete,
        'session-list': sessions.SessionList,
        'session-show': sessions.SessionShow,
        'session-create': sessions.SessionCreate,
        'session-delete': sessions.SessionDelete,
        'session-add-job': sessions.SessionAddJob,
        'session-remove-job': sessions.SessionRemoveJob,
        'session-update': sessions.SessionUpdate,
        'session-start': sessions.SessionStart,
        'action-show': actions.ActionShow,
        'action-list': actions.ActionList,
        'action-delete': actions.ActionDelete,
        'action-create': actions.ActionCreate,
        'action-update': actions.ActionUpdate
    }

    def load_commands(self, namespace):
        for name, command_class in self.SHELL_COMMANDS.items():
            self.add_command(name, command_class)


class FreezerShell(app.App):
    def __init__(self):
        super(FreezerShell, self).__init__(
            description='Python Freezer Client',
            version=freezerclient.__version__,
            deferred_help=True,
            command_manager=FreezerCommandManager(None),
        )

    def build_option_parser(self, description, version):
        parser = super(FreezerShell, self).build_option_parser(description,
                                                               version)
        parser.add_argument(
            '--os-auth-url',
            dest='os_auth_url',
            default=os.environ.get('OS_AUTH_URL'),
            help='Specify identity endpoint',
        )

        parser.add_argument(
            '--os-backup-url',
            dest='os_backup_url',
            default=os.environ.get('OS_BACKUP_URL'),
            help='Specify the Freezer backup service endpoint to use'
        )

        parser.add_argument(
            '--os-endpoint-type',
            dest='os_endpoint_type',
            default=os.environ.get('OS_ENDPOINT_TYPE') or 'public',
            help='''Endpoint type to select. Valid endpoint types:
                    "public" or "publicURL", "internal" or "internalURL",
                    "admin" or "adminURL"'''
        )

        parser.add_argument(
            '--os-identity-api-version',
            dest='os_identity_api_version',
            default=os.environ.get('OS_IDENTITY_API_VERSION'),
            help='Identity API version: 2.0 or 3'
        )

        parser.add_argument(
            '--os-password',
            dest='os_password',
            default=os.environ.get('OS_PASSWORD'),
            help='''Password used for authentication with the OpenStack
                    Identity service'''
        )

        parser.add_argument(
            '--os-username',
            dest='os_username',
            default=os.environ.get('OS_USERNAME'),
            help='''Name used for authentication with the OpenStack
                    Identity service'''
        )

        parser.add_argument(
            '--os-token',
            dest='os_token',
            default=os.environ.get('OS_TOKEN'),
            help='''Specify an existing token to use instead of retrieving
                    one via authentication'''
        )

        parser.add_argument(
            '--os-project-domain-name',
            dest='os_project_domain_name',
            default=os.environ.get('OS_PROJECT_DOMAIN_NAME'),
            help='Domain name containing project'
        )

        parser.add_argument(
            '--os-project-domain-id',
            dest='os_project_domain_id',
            default=os.environ.get('OS_PROJECT_DOMAIN_ID'),
            help='OpenStack project domain ID. '
                 'Defaults to env[OS_PROJECT_ID].'
        )

        parser.add_argument(
            '--os-project-name',
            dest='os_project_name',
            default=os.environ.get('OS_PROJECT_NAME'),
            help='Project name to scope to'
        )

        parser.add_argument(
            '--os-region-name',
            dest='os_region_name',
            default=os.environ.get('OS_REGION_NAME'),
            help='Specify the region to use'
        )

        parser.add_argument(
            '--os-tenant-id',
            dest='os_tenant_id',
            default=os.environ.get('OS_TENANT_ID'),
            help='Tenant to request authorization on'
        )

        parser.add_argument(
            '--os-project-id',
            dest='os_project_id',
            default=os.environ.get('OS_PROJECT_ID'),
            help='Project to request authorization on'
        )

        parser.add_argument(
            '--os-tenant-name',
            dest='os_tenant_name',
            default=os.environ.get('OS_TENANT_NAME'),
            help='Tenant to request authorization on'
        )

        parser.add_argument(
            '--os-user-domain-name',
            dest='os_user_domain_name',
            default=os.environ.get('OS_USER_DOMAIN_NAME'),
            help='User domain name'
        )

        parser.add_argument(
            '--os-user-domain-id',
            dest='os_user_domain_id',
            default=os.environ.get('OS_USER_DOMAIN_ID'),
            help='OpenStack user domain ID. '
                 'Defaults to env[OS_USER_DOMAIN_ID].'
        )

        parser.add_argument(
            '-k', '--insecure',
            dest='insecure',
            action='store_true',
            default=os.environ.get('OS_INSECURE'),
            help='use python-freezerclient with insecure connections'
        )

        parser.add_argument(
            '--os-cacert',
            dest='os_cacert',
            default=os.environ.get('OS_CACERT'),
            help='''Path of CA TLS certificate(s) used to verify the
                    remote server's certificate. Without this option
                    freezer looks for the default system CA certificates.'''
        )

        parser.add_argument(
            '--os-cert',
            dest='os_cert',
            default=os.environ.get('OS_CERT'),
            help='''Path of CERT TLS certificate(s) used to verify the
                    remote server's certificate.1'''
        )

        return parser

    @property
    def client(self):
        """Factory function to create a new freezer service client.

        The returned client will be either a V1 or V2 client.

        :return: freezerclient object
        """
        opts = {
            'token': self.options.os_token,
            'version': self.options.os_identity_api_version,
            'username': self.options.os_username,
            'password': self.options.os_password,
            'tenant_name': self.options.os_tenant_name,
            'auth_url': self.options.os_auth_url,
            'endpoint': self.options.os_backup_url,
            'endpoint_type': self.options.os_endpoint_type,
            'project_name': self.options.os_project_name,
            'project_id': self.options.os_project_id,
            'user_domain_name': self.options.os_user_domain_name,
            'user_domain_id': self.options.os_user_domain_id,
            'project_domain_name': self.options.os_project_domain_name,
            'project_domain_id': self.options.os_project_domain_id,
            'cert': self.options.os_cert,
            'cacert': self.options.os_cacert,
            'insecure': self.options.insecure
        }
        if check_api_version() == '1':
            return v1_client.Client(**opts)
        else:
            return v2_client.Client(**opts)


def main(argv=sys.argv[1:]):
    return FreezerShell().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
