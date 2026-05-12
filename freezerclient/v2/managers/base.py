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

from freezerclient import utils


class BaseManager(object):
    resource_name = None

    def __init__(self, client, verify=True):
        self.client = client
        self.verify = verify

    @property
    def endpoint(self):
        endpoint = self.client.endpoint.rstrip('/')
        if '/v2' in endpoint:
            return '{0}/{1}/'.format(endpoint, self.resource_name)
        return '{0}/v2/{1}/{2}/'.format(
            endpoint, self.client.project_id, self.resource_name)

    @property
    def headers(self):
        return utils.create_headers_for_request(self.client.auth_token)

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def list(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError
