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

from pprint import pformat

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from freezerclient import exceptions
from freezerclient.utils import doc_from_json_file


logging = logging.getLogger(__name__)


class SessionShow(ShowOne):
    """Show a single session"""
    def get_parser(self, prog_name):
        parser = super(SessionShow, self).get_parser(prog_name)
        parser.add_argument(dest='session_id',
                            help='ID of the session')
        return parser

    def take_action(self, parsed_args):
        session = self.app.client.sessions.get(parsed_args.session_id)

        if not session:
            raise exceptions.ApiClientException('Session not found')

        column = (
            'Session ID',
            'Description',
            'Status',
            'Jobs'
        )

        data = (
            session.get('session_id'),
            session.get('description'),
            session.get('status'),
            pformat(session.get('jobs'))
        )
        return column, data


class SessionList(Lister):
    """List all the sessions for your user"""
    def get_parser(self, prog_name):
        parser = super(SessionList, self).get_parser(prog_name)

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
        sessions = self.app.client.sessions.list_all(
            limit=parsed_args.limit,
            offset=parsed_args.offset,
            search=parsed_args.search
        )

        return (('Session ID', 'Description', 'Status', '# Jobs'),
                ((session.get('session_id'),
                  session.get('description'),
                  session.get('status'),
                  len(session.get('jobs', [])),
                  ) for session in sessions))


class SessionCreate(Command):
    """Create a session from a file"""
    def get_parser(self, prog_name):
        parser = super(SessionCreate, self).get_parser(prog_name)
        parser.add_argument('--file',
                            dest='file',
                            help='Path to json file with the job')
        return parser

    def take_action(self, parsed_args):
        session = doc_from_json_file(parsed_args.file)
        session_id = self.app.client.sessions.create(session)
        logging.info('Session {0} created'.format(session_id))


class SessionAddJob(Command):
    """Add a job to a session"""
    def get_parser(self, prog_name):
        parser = super(SessionAddJob, self).get_parser(prog_name)
        parser.add_argument('--session-id',
                            dest='session_id',
                            help='ID of the session')
        parser.add_argument('--job-id',
                            dest='job_id',
                            help='ID of the job to add')
        return parser

    def take_action(self, parsed_args):
        self.app.client.sessions.add_job(parsed_args.session_id,
                                         parsed_args.job_id)
        logging.info('Job {0} added correctly to session {1}'.format(
            parsed_args.job_id, parsed_args.session_id))


class SessionRemoveJob(Command):
    """Remove a job from a session"""
    def get_parser(self, prog_name):
        parser = super(SessionRemoveJob, self).get_parser(prog_name)
        parser.add_argument('--session-id',
                            dest='session_id',
                            help='ID of the session')
        parser.add_argument('--job-id',
                            dest='job_id',
                            help='ID of the job to add')
        return parser

    def take_action(self, parsed_args):
        try:
            self.app.client.sessions.remove_job(parsed_args.session_id,
                                                parsed_args.job_id)
        except Exception as error:
            # there is an error coming from the api when a job is removed
            # with the following text:
            # Additional properties are not allowed ('job_event' was unexpected)
            # but in reality the job gets removed correctly.
            if 'Additional properties are not allowed' in error.message:
                pass
            else:
                raise exceptions.ApiClientException(error.message)
        else:
            logging.info('Job {0} removed correctly from session {1}'.format(
                parsed_args.job_id, parsed_args.session_id))


class SessionStart(Command):
    """Start a session"""
    def get_parser(self, prog_name):
        pass

    def take_action(self, parsed_args):
        pass


class SessionEnd(Command):
    """Stop a session"""
    def get_parser(self, prog_name):
        pass

    def take_action(self, parsed_args):
        pass


class SessionUpdate(Command):
    """Update a session from a file"""
    def get_parser(self, prog_name):
        parser = super(SessionUpdate, self).get_parser(prog_name)
        parser.add_argument(dest='session_id',
                            help='ID of the session')

        parser.add_argument(dest='file',
                            help='Path to json file with the session')
        return parser

    def take_action(self, parsed_args):
        session = doc_from_json_file(parsed_args.file)
        self.app.client.sessions.update(parsed_args.session_id, session)
        logging.info('Session {0} updated'.format(parsed_args.session_id))
