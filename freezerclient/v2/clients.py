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


class ClientShow(show.ShowOne):
    """Show a single client"""
    def get_parser(self, prog_name):
        parser = super(ClientShow, self).get_parser(prog_name)
        parser.add_argument(dest='client_id',
                            help='ID of the client')
        return parser

    def take_action(self, parsed_args):
        client = self.app.client.clients.get(parsed_args.client_id)

        if not client:
            raise exceptions.ApiClientException('Client not found')

        column = (
            'Client ID',
            'Client UUID',
            'hostname',
            'description'
        )
        data = (
            client.get('client', {}).get('client_id'),
            client.get('client', {}).get('uuid'),
            client.get('client', {}).get('hostname'),
            client.get('client', {}).get('description', '')
        )

        return column, data


class ClientList(lister.Lister):
    """List of clients registered in the api"""
    def get_parser(self, prog_name):
        parser = super(ClientList, self).get_parser(prog_name)

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

        clients = self.app.client.clients.list(limit=parsed_args.limit,
                                               offset=parsed_args.offset,
                                               search=search)

        # Print empty table if no clients found
        if not clients:
            clients = [{}]

        columns = ('Client ID', 'uuid', 'hostname', 'description')
        data = ((
            client.get('client', {}).get('client_id', ''),
            client.get('client', {}).get('uuid', ''),
            client.get('client', {}).get('hostname', ''),
            client.get('client', {}).get('description', '')
        ) for client in clients)

        return columns, data


class ClientDelete(command.Command):
    """Delete a client from the api"""
    def get_parser(self, prog_name):
        parser = super(ClientDelete, self).get_parser(prog_name)
        parser.add_argument(dest='client_id',
                            help='ID of the client')
        return parser

    def take_action(self, parsed_args):
        self.app.client.clients.delete(parsed_args.client_id)
        logging.info('Client {0} deleted'.format(parsed_args.client_id))


class ClientRegister(command.Command):
    """Register a new client"""
    def get_parser(self, prog_name):
        parser = super(ClientRegister, self).get_parser(prog_name)
        parser.add_argument('--file',
                            dest='file',
                            required=True,
                            help='Path to json file with the client')
        return parser

    def take_action(self, parsed_args):
        client = utils.doc_from_json_file(parsed_args.file)
        try:
            client_id = self.app.client.clients.create(client)
        except Exception as err:
            raise exceptions.ApiClientException(err.message)
        else:
            logging.info("Client {0} registered".format(client_id))
