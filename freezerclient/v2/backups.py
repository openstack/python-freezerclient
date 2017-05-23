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

import datetime
import logging
import pprint

from cliff import command
from cliff import lister
from cliff import show

from freezerclient import exceptions
from freezerclient import utils


logging = logging.getLogger(__name__)


class BackupShow(show.ShowOne):
    """Show the metadata of a single backup"""
    def get_parser(self, prog_name):
        parser = super(BackupShow, self).get_parser(prog_name)
        parser.add_argument(dest='backup_uuid',
                            help='ID of the backup')
        return parser

    def take_action(self, parsed_args):
        backup = self.app.client.backups.get(parsed_args.backup_uuid)
        if not backup:
            raise exceptions.ApiClientException('Backup not found')

        column = (
            'Backup ID',
            'Metadata'
        )
        data = (
            backup.get('backup_uuid'),
            pprint.pformat(backup.get('backup_metadata'))
        )
        return column, data


class BackupList(lister.Lister):
    """List all backups for your user"""
    def get_parser(self, prog_name):
        parser = super(BackupList, self).get_parser(prog_name)

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

        backups = self.app.client.backups.list(limit=parsed_args.limit,
                                               offset=parsed_args.offset,
                                               search=search)

        columns = ('Backup ID', 'Backup UUID', 'Hostname', 'Path',
                   'Created at', 'Level')

        # Print empty table if no backups found
        if not backups:
            backups = [{}]

        data = ((b.get('backup_id', ''),
                 b.get('backup_uuid', ''),
                 b.get('backup_metadata', {}).get('hostname', ''),
                 b.get('backup_metadata', {}).get('path_to_backup', ''),
                 datetime.datetime.fromtimestamp(
                     int(b.get('backup_metadata', {}).get(
                         'time_stamp', ''))) if b.get(
                     'backup_metadata') else '',
                 b.get('backup_metadata', {}).get('curr_backup_level', '')
                 ) for b in backups)

        return columns, data


class BackupDelete(command.Command):
    """Delete a backup from the api"""
    def get_parser(self, prog_name):
        parser = super(BackupDelete, self).get_parser(prog_name)
        parser.add_argument(dest='backup_uuid',
                            help='UUID of the backup')
        return parser

    def take_action(self, parsed_args):
        self.app.client.backups.delete(parsed_args.backup_uuid)
        logging.info('Backup {0} deleted'.format(parsed_args.backup_uuid))
