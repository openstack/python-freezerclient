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
from pprint import pprint

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from freezerclient import exceptions
from freezerclient.utils import doc_from_json_file


logging = logging.getLogger(__name__)


class JobShow(ShowOne):
    """Show a single job"""
    def get_parser(self, prog_name):
        parser = super(JobShow, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        job = self.app.client.jobs.get(parsed_args.job_id)

        if not job:
            raise exceptions.ApiClientException('Job not found')

        column = (
            'Job ID',
            'Client ID',
            'User ID',
            'Session ID',
            'Description',
            'Actions',
            'Start Date',
            'End Date',
            'Interval',
        )
        data = (
            job.get('job_id'),
            job.get('client_id'),
            job.get('user_id'),
            job.get('session_id', ''),
            job.get('description'),
            pformat(job.get('job_actions')),
            job.get('job_schedule', {}).get('schedule_start_date', ''),
            job.get('job_schedule', {}).get('schedule_interval', ''),
            job.get('job_schedule', {}).get('schedule_end_date', ''),
        )
        return column, data


class JobList(Lister):
    """List all the jobs for your user"""
    def get_parser(self, prog_name):
        parser = super(JobList, self).get_parser(prog_name)

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
        jobs = self.app.client.jobs.list_all(
                limit=parsed_args.limit,
                offset=parsed_args.offset,
                search=parsed_args.search
        )

        return (('Job ID', 'Description', '# Actions', 'Result', 'Event', 'Session ID'),
                ((job.get('job_id'),
                  job.get('description'),
                  len(job.get('job_actions', [])),
                  job.get('job_schedule', {}).get('result', ''),
                  job.get('job_schedule', {}).get('event', ''),
                  job.get('session_id', '')
                  ) for job in jobs))


class JobGet(Command):
    """Download a job as a json file"""
    def get_parser(self, prog_name):
        parser = super(JobGet, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')

        parser.add_argument('--no-format',
                            dest='no_format',
                            default=False,
                            action='store_true',
                            help='Return a job in json without pretty print')
        return parser

    def take_action(self, parsed_args):
        job = self.app.client.jobs.get(parsed_args.job_id)

        if not job:
            raise exceptions.ApiClientException('Job not found')

        if parsed_args.no_format:
            print(job)
        else:
            pprint(job)


class JobDelete(Command):
    """Delete a job from the api"""
    def get_parser(self, prog_name):
        parser = super(JobDelete, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.delete(parsed_args.job_id)
        logging.info('Job {0} deleted'.format(parsed_args.job_id))


class JobCreate(Command):
    """Create a new job from a file"""
    def get_parser(self, prog_name):
        parser = super(JobCreate, self).get_parser(prog_name)
        parser.add_argument('--file',
                            dest='file',
                            help='Path to json file with the job')
        return parser

    def take_action(self, parsed_args):
        job = doc_from_json_file(parsed_args.file)
        job_id = self.app.client.jobs.create(job)
        logging.info('Job {0} created'.format(job_id))


class JobStart(Command):
    """Send a start signal for a job"""
    def get_parser(self, prog_name):
        parser = super(JobStart, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.start_job(parsed_args.job_id)
        logging.info('Job {0} has started'.format(parsed_args.job_id))


class JobStop(Command):
    """Send a stop signal for a job"""
    def get_parser(self, prog_name):
        parser = super(JobStop, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.stop_job(parsed_args.job_id)
        logging.info('Job {0} has stopped'.format(parsed_args.job_id))


class JobAbort(Command):
    """Abort a running job"""
    def get_parser(self, prog_name):
        parser = super(JobAbort, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.abort_job(parsed_args.job_id)
        logging.info('Job {0} has been aborted'.format(parsed_args.job_id))


class JobUpdate(Command):
    """Update a job from a file"""
    def get_parser(self, prog_name):
        parser = super(JobUpdate, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')

        parser.add_argument(dest='file',
                            help='Path to json file with the job')
        return parser

    def take_action(self, parsed_args):
        job = doc_from_json_file(parsed_args.file)
        self.app.client.jobs.update(parsed_args.job_id, job)
        logging.info('Job {0} updated'.format(parsed_args.job_id))
