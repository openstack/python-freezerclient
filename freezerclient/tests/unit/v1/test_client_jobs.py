# (c) Copyright 2014,2015,2016 Hewlett-Packard Development Company, L.P.
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

import unittest
from unittest import mock

from oslo_serialization import jsonutils as json

from freezerclient import exceptions
from freezerclient.v1.managers import jobs


class TestJobManager(unittest.TestCase):
    def setUp(self):
        self.mock_client = mock.Mock()
        self.mock_response = mock.Mock()
        self.mock_client.endpoint = 'http://testendpoint:9999'
        self.mock_client.auth_token = 'testtoken'
        self.mock_client.client_id = 'test_client_id_78900987'
        self.job_manager = jobs.JobManager(self.mock_client)
        self.headers = {
            'X-Auth-Token': 'testtoken',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_create(self, mock_requests):
        self.assertEqual('http://testendpoint:9999/v1/jobs/',
                         self.job_manager.endpoint)
        self.assertEqual({'X-Auth-Token': 'testtoken',
                          'Content-Type': 'application/json',
                          'Accept': 'application/json'},
                         self.job_manager.headers)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_create_ok(self, mock_requests):
        self.mock_response.status_code = 201
        self.mock_response.json.return_value = {'job_id': 'qwerqwer'}
        mock_requests.post.return_value = self.mock_response
        retval = self.job_manager.create({'job': 'metadata'})
        self.assertEqual('qwerqwer', retval)

    @mock.patch('freezerclient.v1.managers.jobs.json')
    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_create_adds_client_id_if_not_provided(self, mock_requests,
                                                   mock_json):
        self.mock_response.status_code = 201
        self.mock_response.json.return_value = {'job_id': 'qwerqwer'}
        mock_json.dumps.return_value = {'job': 'mocked'}
        mock_requests.post.return_value = self.mock_response

        retval = self.job_manager.create({'job': 'metadata'})

        mock_json.dumps.assert_called_with({
            'job': 'metadata', 'client_id': 'test_client_id_78900987'
        })
        self.assertEqual('qwerqwer', retval)

    @mock.patch('freezerclient.v1.managers.jobs.json')
    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_create_leaves_provided_client_id(self, mock_requests, mock_json):
        self.mock_response.status_code = 201
        self.mock_response.json.return_value = {'job_id': 'qwerqwer'}
        mock_json.dumps.return_value = {'job': 'mocked'}
        mock_requests.post.return_value = self.mock_response

        retval = self.job_manager.create(
            {'job': 'metadata', 'client_id': 'parmenide'})

        mock_json.dumps.assert_called_with({'job': 'metadata',
                                            'client_id': 'parmenide'})
        self.assertEqual('qwerqwer', retval)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_create_fail_when_api_return_error_code(self, mock_requests):
        self.mock_response.status_code = 500
        mock_requests.post.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.job_manager.create, {'job': 'metadata'})

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_delete_ok(self, mock_requests):
        self.mock_response.status_code = 204
        mock_requests.delete.return_value = self.mock_response
        retval = self.job_manager.delete('test_job_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_delete_fail(self, mock_requests):
        self.mock_response.status_code = 500
        mock_requests.delete.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.job_manager.delete, 'test_job_id')

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_get_ok(self, mock_requests):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {'job_id': 'qwerqwer'}
        mock_requests.get.return_value = self.mock_response
        retval = self.job_manager.get('test_job_id')
        self.assertEqual({'job_id': 'qwerqwer'}, retval)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_get_fails_on_error_different_from_404(self, mock_requests):
        self.mock_response.status_code = 500
        mock_requests.get.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException, self.job_manager.get,
                          'test_job_id')

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_get_none(self, mock_requests):
        self.mock_response.status_code = 404
        mock_requests.get.return_value = self.mock_response
        retval = self.job_manager.get('test_job_id')
        self.assertIsNone(retval)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_list_ok(self, mock_requests):
        self.mock_response.status_code = 200
        job_list = [{'job_id_0': 'bomboloid'}, {'job_id_1': 'asdfasdf'}]
        self.mock_response.json.return_value = {'jobs': job_list}
        mock_requests.get.return_value = self.mock_response
        retval = self.job_manager.list()
        self.assertEqual(job_list, retval)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_list_error(self, mock_requests):
        self.mock_response.status_code = 404
        job_list = [{'job_id_0': 'bomboloid'}, {'job_id_1': 'asdfasdf'}]
        self.mock_response.json.return_value = {'clients': job_list}
        mock_requests.get.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException, self.job_manager.list)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_update_ok(self, mock_requests):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {
            "patch": {"status": "bamboozled"},
            "version": 12,
            "job_id": "d454beec-1f3c-4d11-aa1a-404116a40502"
        }
        mock_requests.patch.return_value = self.mock_response
        retval = self.job_manager.update(
            'd454beec-1f3c-4d11-aa1a-404116a40502', {'status': 'bamboozled'})
        self.assertEqual(12, retval)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_update_raise_MetadataUpdateFailure_when_api_return_error_code(
            self, mock_requests):
        self.mock_response.json.return_value = {
            "patch": {"status": "bamboozled"},
            "version": 12,
            "job_id": "d454beec-1f3c-4d11-aa1a-404116a40502"
        }
        self.mock_response.status_code = 404
        self.mock_response.text = (
            '{"title": "Not Found","description":"No document found with ID '
            'd454beec-1f3c-4d11-aa1a-404116a40502x"}'
        )
        mock_requests.patch.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.job_manager.update,
                          'd454beec-1f3c-4d11-aa1a-404116a40502',
                          {'status': 'bamboozled'})

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_start_job_posts_proper_data(self, mock_requests):
        job_id = 'jobdfsfnqwerty1234'
        self.mock_response.status_code = 202
        self.mock_response.json.return_value = {'result': 'success'}
        mock_requests.post.return_value = self.mock_response
        # /v1/jobs/{job_id}/event

        endpoint = '{0}/v1/jobs/{1}/event'.format(self.mock_client.endpoint,
                                                  job_id)
        data = {"start": None}
        retval = self.job_manager.start_job(job_id)
        self.assertEqual({'result': 'success'}, retval)

        args = mock_requests.post.call_args[0]
        kwargs = mock_requests.post.call_args[1]
        self.assertEqual(endpoint, args[0])
        self.assertEqual(data, json.loads(kwargs['data']))
        self.assertEqual(self.headers, kwargs['headers'])

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_start_job_raise_ApiClientException_when_api_return_error_code(
            self, mock_requests):
        job_id = 'jobdfsfnqwerty1234'
        self.mock_response.status_code = 500
        self.mock_response.json.return_value = {'result': 'success'}
        mock_requests.post.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.job_manager.start_job, job_id)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_stop_job_posts_proper_data(self, mock_requests):
        job_id = 'jobdfsfnqwerty1234'
        self.mock_response.status_code = 202
        self.mock_response.json.return_value = {'result': 'success'}
        mock_requests.post.return_value = self.mock_response
        # /v1/jobs/{job_id}/event

        endpoint = '{0}/v1/jobs/{1}/event'.format(self.mock_client.endpoint,
                                                  job_id)
        data = {"stop": None}
        retval = self.job_manager.stop_job(job_id)
        self.assertEqual({'result': 'success'}, retval)

        args = mock_requests.post.call_args[0]
        kwargs = mock_requests.post.call_args[1]
        self.assertEqual(endpoint, args[0])
        self.assertEqual(data, json.loads(kwargs['data']))
        self.assertEqual(self.headers, kwargs['headers'])

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_stop_job_raise_ApiClientException_when_api_return_error_code(
            self, mock_requests):
        job_id = 'jobdfsfnqwerty1234'
        self.mock_response.status_code = 500
        self.mock_response.json.return_value = {'result': 'success'}
        mock_requests.post.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.job_manager.start_job, job_id)

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_abort_job_posts_proper_data(self, mock_requests):
        job_id = 'jobdfsfnqwerty1234'
        self.mock_response.status_code = 202
        self.mock_response.json.return_value = {'result': 'success'}
        mock_requests.post.return_value = self.mock_response
        # /v1/jobs/{job_id}/event

        endpoint = '{0}/v1/jobs/{1}/event'.format(self.mock_client.endpoint,
                                                  job_id)
        data = {"abort": None}
        retval = self.job_manager.abort_job(job_id)
        self.assertEqual({'result': 'success'}, retval)

        args = mock_requests.post.call_args[0]
        kwargs = mock_requests.post.call_args[1]
        self.assertEqual(endpoint, args[0])
        self.assertEqual(data, json.loads(kwargs['data']))
        self.assertEqual(self.headers, kwargs['headers'])

    @mock.patch('freezerclient.v1.managers.jobs.requests')
    def test_abort_job_raise_ApiClientException_when_api_return_error_code(
            self, mock_requests):
        job_id = 'jobdfsfnqwerty1234'
        self.mock_response.status_code = 500
        self.mock_response.json.return_value = {'result': 'success'}
        mock_requests.post.return_value = self.mock_response
        self.assertRaises(exceptions.ApiClientException,
                          self.job_manager.abort_job, job_id)
