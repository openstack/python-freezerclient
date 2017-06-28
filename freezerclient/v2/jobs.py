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

from cliff import command
from cliff import lister
from cliff import show

from freezerclient import exceptions
from freezerclient import utils


logging = logging.getLogger(__name__)


class JobShow(show.ShowOne):
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
            pprint.pformat(job.get('job_actions')),
            job.get('job_schedule', {}).get('schedule_start_date', ''),
            job.get('job_schedule', {}).get('schedule_end_date', ''),
            job.get('job_schedule', {}).get('schedule_interval', ''),
        )
        return column, data


class JobList(lister.Lister):
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
            default={},
            help='Define a filter for the query',
        )

        parser.add_argument(
            '--client', '-C',
            dest='client_id',
            default='',
            help='Get jobs for a specific client',
        )
        return parser

    def take_action(self, parsed_args):

        search = utils.prepare_search(parsed_args.search)

        if parsed_args.client_id:
            jobs = self.app.client.jobs.list(
                limit=parsed_args.limit,
                offset=parsed_args.offset,
                search=search,
                client_id=parsed_args.client_id
            )
        else:
            jobs = self.app.client.jobs.list_all(
                limit=parsed_args.limit,
                offset=parsed_args.offset,
                search=search
            )

        columns = ('Job ID', 'Description', '# Actions', 'Result', 'Status',
                   'Event', 'Session ID')

        # Print empty table if no jobs found
        if not jobs:
            jobs = [{}]
            data = ((job.get('job_id', ''),
                     job.get('description', ''),
                     job.get('job_actions', ''),
                     job.get('job_schedule', {}).get('result', ''),
                     job.get('job_schedule', {}).get('status', ''),
                     job.get('job_schedule', {}).get('event', ''),
                     job.get('session_id', '')
                     ) for job in jobs)
        else:
            data = ((job.get('job_id'),
                     job.get('description'),
                     len(job.get('job_actions', [])),
                     job.get('job_schedule', {}).get('result', ''),
                     job.get('job_schedule', {}).get('status', ''),
                     job.get('job_schedule', {}).get('event', ''),
                     job.get('session_id', '')
                     ) for job in jobs)

        return columns, data


class JobGet(command.Command):
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
            pprint.pprint(job)


class JobDelete(command.Command):
    """Delete a job from the api"""
    def get_parser(self, prog_name):
        parser = super(JobDelete, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.delete(parsed_args.job_id)
        logging.info('Job {0} deleted'.format(parsed_args.job_id))


class JobCreate(command.Command):
    """Create a new job from a file"""
    def get_parser(self, prog_name):
        parser = super(JobCreate, self).get_parser(prog_name)
        parser.add_argument(
            '--file',
            dest='file',
            required=True,
            help='Path to json file with the job')

        parser.add_argument(
            '--client', '-C',
            dest='client_id',
            required=True,
            help='Select a client for this job',
        )

        return parser

    def take_action(self, parsed_args):
        job = utils.doc_from_json_file(parsed_args.file)
        job['client_id'] = parsed_args.client_id
        job_id = self.app.client.jobs.create(job)
        logging.info('Job {0} created'.format(job_id))


class JobStart(command.Command):
    """Send a start signal for a job"""
    def get_parser(self, prog_name):
        parser = super(JobStart, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.start_job(parsed_args.job_id)
        logging.info("Start request sent "
                     "for job {0}".format(parsed_args.job_id))


class JobStop(command.Command):
    """Send a stop signal for a job"""
    def get_parser(self, prog_name):
        parser = super(JobStop, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.stop_job(parsed_args.job_id)
        logging.info("Stop request sent "
                     "for job {0}".format(parsed_args.job_id))


class JobAbort(command.Command):
    """Abort a running job"""
    def get_parser(self, prog_name):
        parser = super(JobAbort, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')
        return parser

    def take_action(self, parsed_args):
        self.app.client.jobs.abort_job(parsed_args.job_id)
        logging.info("Abort request sent "
                     "for job {0}".format(parsed_args.job_id))


class JobUpdate(command.Command):
    """Update a job from a file"""
    def get_parser(self, prog_name):
        parser = super(JobUpdate, self).get_parser(prog_name)
        parser.add_argument(dest='job_id',
                            help='ID of the job')

        parser.add_argument(dest='file',
                            help='Path to json file with the job')
        return parser

    def take_action(self, parsed_args):
        job = utils.doc_from_json_file(parsed_args.file)
        self.app.client.jobs.update(parsed_args.job_id, job)
        logging.info('Job {0} updated'.format(parsed_args.job_id))
