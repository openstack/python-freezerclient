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

from freezerclient import base
from freezerclient import exceptions
from freezerclient import utils


logging = logging.getLogger(__name__)


# Explicit label overrides for action fields that require special casing,
# acronym capitalization (e.g. ID, AZ, LVM, SSH, FTP, VSS), or custom names.
# Fields not listed here are automatically formatted from snake_case to
# Title Case.
ACTION_FIELD_LABELS = {
    # Custom names
    'path_to_backup': 'Path to Backup or Restore',
    'cinder_vol_name': 'Cinder Volume Name',
    'nova_inst_name': 'Nova Instance Name',
    'lvm_dirmount': 'LVM Mount Directory',
    'mysql_conf': 'MySQL Config',
    'sql_server_conf': 'SQL Server Config',
    'shadow': 'VSS Shadow',
    'shadow_path': 'VSS Shadow Path',

    # Acronyms: ID
    'action_id': 'Action ID',
    'user_id': 'User ID',
    'project_id': 'Project ID',
    'cinder_vol_id': 'Cinder Volume ID',
    'cinderbrick_vol_id': 'Cinder Brick Volume ID',
    'cindernative_vol_id': 'Cinder Native Volume ID',
    'cindernative_backup_id': 'Cinder Native Backup ID',
    'nova_inst_id': 'Nova Instance ID',
    'glance_image_id': 'Glance Image ID',
    'os_trust_id': 'Trust ID',

    # Acronyms: AZ
    'cindernative_backup_az': 'Cinder Native Backup AZ',

    # Acronyms: LVM
    'lvm_auto_snap': 'LVM Auto Snap',
    'lvm_volgroup': 'LVM Volume Group',
    'lvm_snapname': 'LVM Snapshot Name',
    'lvm_snapperm': 'LVM Snapshot Permission',
    'lvm_snapsize': 'LVM Snapshot Size',
    'lvm_srcvol': 'LVM Source Volume',

    # Acronyms: SSH & FTP
    'ssh_key': 'SSH Key',
    'ssh_username': 'SSH Username',
    'ssh_host': 'SSH Host',
    'ssh_port': 'SSH Port',
    'ssh_password': 'SSH Password',
    'ftp_host': 'FTP Host',
    'ftp_port': 'FTP Port',
    'ftp_username': 'FTP Username',
    'ftp_keyfile': 'FTP Key File',
    'ftp_certfile': 'FTP Cert File',
    'ftp_password': 'FTP Password',
}

SENSITIVE_KEYS = {'ssh_password', 'ftp_password', 'secret_key'}


def _format_label(key):
    return ACTION_FIELD_LABELS.get(key, key.replace('_', ' ').title())


def _format_value(key, val):
    if key in SENSITIVE_KEYS and val:
        return '********'
    return val


def format_action(action):
    freezer_action = action.get('freezer_action') or {}
    columns = []
    data = []

    columns.append('Action ID')
    data.append(action.get('action_id'))

    primary_fa_keys = [
        ('backup_name', freezer_action.get('backup_name', '')),
        ('action', freezer_action.get('action', 'backup')),
        ('mode', freezer_action.get('mode', 'fs')),
        ('storage', freezer_action.get('storage', '')),
    ]
    for key, default_val in primary_fa_keys:
        columns.append(_format_label(key))
        data.append(_format_value(key, freezer_action.get(key, default_val)))

    handled_fa_keys = {'backup_name', 'action', 'mode', 'storage'}

    for key in sorted(freezer_action.keys()):
        if key not in handled_fa_keys:
            columns.append(_format_label(key))
            data.append(_format_value(key, freezer_action[key]))
            handled_fa_keys.add(key)

    top_level_keys = [
        ('max_retries_interval', action.get('max_retries_interval', '6')),
        ('max_retries', action.get('max_retries', '5')),
        ('user_id', action.get('user_id', '')),
        ('project_id', action.get('project_id', '')),
    ]
    for key, val in top_level_keys:
        columns.append(_format_label(key))
        data.append(_format_value(key, val))

    handled_top_keys = {'action_id', 'freezer_action', 'max_retries_interval',
                        'max_retries', 'user_id', 'project_id'}
    for key in sorted(action.keys()):
        if key not in handled_top_keys:
            columns.append(_format_label(key))
            data.append(_format_value(key, action[key]))
            handled_top_keys.add(key)

    return tuple(columns), tuple(data)


class ActionShow(base.FreezerShowOne):
    """Show a single action """
    def get_parser(self, prog_name):
        parser = super(ActionShow, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the action')
        return parser

    def take_action(self, parsed_args):
        action = self.client.actions.get(parsed_args.action_id)

        if not action:
            raise exceptions.ApiClientException('Action not found')

        return format_action(action)


class ActionList(base.FreezerLister):
    """List all actions for your user"""
    def get_parser(self, prog_name):
        parser = super(ActionList, self).get_parser(prog_name)

        parser.add_argument(
            '--limit',
            dest='limit',
            default=100,
            help='Specify a limit for search query',
        )

        parser.add_argument(
            '--offset',
            dest='offset',
            default=0,
            help='',
        )

        parser.add_argument(
            '--search',
            dest='search',
            default='',
            help='Define a filter for the query',
        )
        return parser

    def take_action(self, parsed_args):
        search = utils.prepare_search(parsed_args.search)

        actions = self.client.actions.list(
            limit=parsed_args.limit,
            offset=parsed_args.offset,
            search=search
        )

        columns = ('Action ID', 'Name', 'Action',
                   'Path to Backup or Restore', 'Mode', 'Storage', 'snapshot')

        # Print empty table if no actions found
        if not actions:
            actions = [{}]
            data = ((action.get('action-id', ''),
                     action.get('freezer_action', {}).get('backup_name', ''),
                     action.get('freezer_action', {}).get('action', ''),
                     action.get('freezer_action', {}).get(
                         'path_to_backup', ''),
                     action.get('freezer_action', {}).get('mode', ''),
                     action.get('freezer_action', {}).get('storage', ''),
                     action.get('freezer_action', {}).get('snapshot', '')
                     ) for action in actions)
        else:
            data = ((action.get('action_id'),
                     action.get('freezer_action', {}).get('backup_name', ''),
                     action.get('freezer_action', {}).get('action', 'backup'),
                     action.get('freezer_action', {}).get(
                         'path_to_backup', ''),
                     action.get('freezer_action', {}).get('mode', 'fs'),
                     action.get('freezer_action', {}).get('storage', ''),
                     action.get('freezer_action', {}).get('snapshot', 'False')
                     ) for action in actions)

        return columns, data


class ActionDelete(base.FreezerCommand):
    """Delete an action from the api"""
    def get_parser(self, prog_name):
        parser = super(ActionDelete, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the action')
        return parser

    def take_action(self, parsed_args):
        self.client.actions.delete(parsed_args.action_id)


class ActionCreate(base.FreezerShowOne):
    """Create an action from a file"""
    def get_parser(self, prog_name):
        parser = super(ActionCreate, self).get_parser(prog_name)
        parser.add_argument('--file',
                            dest='file',
                            required=True,
                            help='Path to json file with the action')
        return parser

    def take_action(self, parsed_args):
        action_data = utils.doc_from_json_file(parsed_args.file)
        action_id = self.client.actions.create(action_data)
        action = self.client.actions.get(action_id)
        if not action:
            raise exceptions.ApiClientException('Action created but not found')
        return format_action(action)


class ActionUpdate(base.FreezerShowOne):
    """Update an action from a file"""
    def get_parser(self, prog_name):
        parser = super(ActionUpdate, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the session')

        parser.add_argument(dest='file',
                            help='Path to json file with the action')
        return parser

    def take_action(self, parsed_args):
        action_data = utils.doc_from_json_file(parsed_args.file)
        self.client.actions.update(parsed_args.action_id, action_data)
        action = self.client.actions.get(parsed_args.action_id)
        if not action:
            raise exceptions.ApiClientException('Action not found')
        return format_action(action)
