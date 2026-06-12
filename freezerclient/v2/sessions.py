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
import pprint

from freezerclient import base
from freezerclient import exceptions
from freezerclient import utils


logging = logging.getLogger(__name__)


def format_session(session):
    column = (
        'Session ID',
        'Session tag',
        'Description',
        'Status',
        'Result',
        'Jobs',
        'Hold off',
        'Schedule',
        'Last start',
        'Time start',
        'Time end',
        'Project id',
        'User id',
    )

    data = (
        session.get('session_id'),
        session.get('session_tag'),
        session.get('description'),
        session.get('status'),
        session.get('result'),
        pprint.pformat(session.get('jobs')),
        session.get('hold_off'),
        pprint.pformat(session.get('schedule')),
        session.get('last_start'),
        session.get('time_start'),
        session.get('time_end'),
        session.get('project_id'),
        session.get('user_id'),
    )
    return column, data


class SessionShow(base.FreezerShowOne):
    """Show a single session"""
    def get_parser(self, prog_name):
        parser = super(SessionShow, self).get_parser(prog_name)
        parser.add_argument(dest='session_id',
                            help='ID of the session')
        return parser

    def take_action(self, parsed_args):
        session = self.client.sessions.get(parsed_args.session_id)

        if not session:
            raise exceptions.ApiClientException('Session not found')

        return format_session(session)


class SessionList(base.FreezerLister):
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
        search = utils.prepare_search(parsed_args.search)
        sessions = self.client.sessions.list_all(
            limit=parsed_args.limit,
            offset=parsed_args.offset,
            search=search
        )

        # Print empty table if no sessions found
        if not sessions:
            sessions = [{}]
        columns = ('Session ID', 'Description', 'Status',
                   'Result', '# Jobs')
        data = ((
            session.get('session_id', ''),
            session.get('description', ''),
            session.get('status', ''),
            session.get('result', ''),
            len(session.get('jobs', [])) if session.get(
                'session_id') else '',
        ) for session in sessions)

        return columns, data


class SessionCreate(base.FreezerShowOne):
    """Create a session from a file"""
    def get_parser(self, prog_name):
        parser = super(SessionCreate, self).get_parser(prog_name)
        parser.add_argument('--file',
                            dest='file',
                            required=True,
                            help='Path to json file with the job')
        return parser

    def take_action(self, parsed_args):
        session_data = utils.doc_from_json_file(parsed_args.file)
        session_id = self.client.sessions.create(session_data)
        session = self.client.sessions.get(session_id)
        if not session:
            raise exceptions.ApiClientException(
                'Session created but not found')
        return format_session(session)


class SessionDelete(base.FreezerCommand):
    """Delete a session"""
    def get_parser(self, prog_name):
        parser = super(SessionDelete, self).get_parser(prog_name)
        parser.add_argument(dest='session_id',
                            help='ID of the session')
        return parser

    def take_action(self, parsed_args):
        session = self.client.sessions.get(parsed_args.session_id)
        if not session:
            raise exceptions.ApiClientException('Session not found')

        self.client.sessions.delete(parsed_args.session_id)


class SessionAddJob(base.FreezerCommand):
    """Add a job to a session"""
    def get_parser(self, prog_name):
        parser = super(SessionAddJob, self).get_parser(prog_name)
        parser.add_argument('--session-id',
                            dest='session_id',
                            required=True,
                            help='ID of the session')
        parser.add_argument('--job-id',
                            dest='job_id',
                            required=True,
                            help='ID of the job to add')
        return parser

    def take_action(self, parsed_args):
        self.client.sessions.add_job(parsed_args.session_id,
                                     parsed_args.job_id)


class SessionRemoveJob(base.FreezerCommand):
    """Remove a job from a session"""
    def get_parser(self, prog_name):
        parser = super(SessionRemoveJob, self).get_parser(prog_name)
        parser.add_argument('--session-id',
                            dest='session_id',
                            required=True,
                            help='ID of the session')
        parser.add_argument('--job-id',
                            dest='job_id',
                            required=True,
                            help='ID of the job to add')
        return parser

    def take_action(self, parsed_args):
        try:
            self.client.sessions.remove_job(parsed_args.session_id,
                                            parsed_args.job_id)
        except Exception as error:
            # there is an error coming from the api when a job is removed
            # with the following text:
            # Additional properties are not allowed
            # ('job_event' was unexpected)
            # but in reality the job gets removed correctly.
            if 'Additional properties are not allowed' in error.message:
                pass
            else:
                raise exceptions.ApiClientException(error.message)


class SessionUpdate(base.FreezerShowOne):
    """Update a session from a file"""
    def get_parser(self, prog_name):
        parser = super(SessionUpdate, self).get_parser(prog_name)
        parser.add_argument(dest='session_id',
                            help='ID of the session')

        parser.add_argument(dest='file',
                            help='Path to json file with the session')
        return parser

    def take_action(self, parsed_args):
        session_data = utils.doc_from_json_file(parsed_args.file)
        self.client.sessions.update(parsed_args.session_id, session_data)
        session = self.client.sessions.get(parsed_args.session_id)
        if not session:
            raise exceptions.ApiClientException('Session not found')
        return format_session(session)


class SessionStart(base.FreezerCommand):
    """Start a session"""
    def get_parser(self, prog_name):
        parser = super(SessionStart, self).get_parser(prog_name)
        parser.add_argument('--session-id',
                            dest='session_id',
                            required=True,
                            help='ID of the session')
        parser.add_argument('--job-id',
                            dest='job_id',
                            required=True,
                            help='ID of the job')
        parser.add_argument('--job-tag',
                            dest='job_tag',
                            required=True,
                            help='Job tag value')

        return parser

    def take_action(self, parsed_args):
        session = self.client.sessions.get(parsed_args.session_id)
        if not session:
            raise exceptions.ApiClientException('Session not found')

        self.client.sessions.start_session(
            parsed_args.session_id,
            parsed_args.job_id,
            parsed_args.job_tag
        )
