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

import logging

from osc_lib import utils

LOG = logging.getLogger(__name__)

API_NAME = 'backup'
API_VERSION_OPTION = 'os_backup_api_version'
DEFAULT_API_VERSION = '2'
API_VERSIONS = {
    '2': 'freezerclient.v2.client.Client',
}


def make_client(instance):
    """Returns a backup service client"""
    from freezerclient.v2.client import Client

    endpoint = instance.get_endpoint_for_service_type(
        'backup',
        interface=instance.interface,
        region_name=instance.region_name
    )

    insecure = False
    cacert = None
    if isinstance(instance.session.verify, bool):
        insecure = not instance.session.verify
    else:
        cacert = instance.session.verify

    return Client(
        session=instance.session,
        endpoint=endpoint,
        insecure=insecure,
        cacert=cacert,
    )


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-backup-api-version',
        metavar='<backup-api-version>',
        default=utils.env(
            'OS_BACKUP_API_VERSION',
            default=DEFAULT_API_VERSION
        ),
        help='Backup API version, default=2 (Env: OS_BACKUP_API_VERSION)'
    )
    return parser
