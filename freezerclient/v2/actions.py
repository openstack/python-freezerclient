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

from cliff import command
from cliff import lister
from cliff import show

from freezerclient import exceptions
from freezerclient import utils


logging = logging.getLogger(__name__)


class ActionShow(show.ShowOne):
    """Show a single action """
    def get_parser(self, prog_name):
        parser = super(ActionShow, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the action')
        return parser

    def take_action(self, parsed_args):
        action = self.app.client.actions.get(parsed_args.action_id)

        if not action:
            raise exceptions.ApiClientException('Action not found')

        column = (
            'Action ID',
            'Name',
            'Action',
            'Mode',
            'Path to Backup or Restore',
            'Storage',
            'Snapshot'
        )

        data = (
            action.get('action_id'),
            action.get('freezer_action', {}).get('backup_name', ''),
            action.get('freezer_action', {}).get('action', 'backup'),
            action.get('freezer_action', {}).get('mode', 'fs'),
            action.get('freezer_action', {}).get('path_to_backup', ''),
            action.get('freezer_action', {}).get('storage', 'swift'),
            action.get('freezer_action', {}).get('snapshot', 'False'),
        )

        return column, data


class ActionList(lister.Lister):
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

        actions = self.app.client.actions.list(
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
                     action.get('freezer_action', {}).get('storage', 'swift'),
                     action.get('freezer_action', {}).get('snapshot', 'False')
                     ) for action in actions)

        return columns, data


class ActionDelete(command.Command):
    """Delete an action from the api"""
    def get_parser(self, prog_name):
        parser = super(ActionDelete, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the action')
        return parser

    def take_action(self, parsed_args):
        self.app.client.actions.delete(parsed_args.action_id)
        logging.info('Action {0} deleted'.format(parsed_args.action_id))


class ActionCreate(command.Command):
    """Create an action from a file"""
    def get_parser(self, prog_name):
        parser = super(ActionCreate, self).get_parser(prog_name)
        parser.add_argument('--file',
                            dest='file',
                            required=True,
                            help='Path to json file with the action')
        return parser

    def take_action(self, parsed_args):
        action = utils.doc_from_json_file(parsed_args.file)
        action_id = self.app.client.actions.create(action)
        logging.info('Action {0} created'.format(action_id))


class ActionUpdate(command.Command):
    """Update an action from a file"""
    def get_parser(self, prog_name):
        parser = super(ActionUpdate, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the session')

        parser.add_argument(dest='file',
                            help='Path to json file with the action')
        return parser

    def take_action(self, parsed_args):
        action = utils.doc_from_json_file(parsed_args.file)
        self.app.client.actions.update(parsed_args.action_id, action)
        logging.info('Action {0} updated'.format(parsed_args.action_id))
