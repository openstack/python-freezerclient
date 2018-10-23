# (c) Copyright 2018 ZTE Corporation.
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
import os


def Client(version=None, endpoint=None, username=None, password=None,
           project_name=None, auth_url=None, project_id=None, token=None,
           cacert=None, project_domain_name=None, user_domain_id=None,
           user_domain_name=None, **kwargs):
    """Initialize client object based on given version.

    HOW-TO:
    The simplest way to create a client instance is initialization with your
    credentials::

        >>> from freezerclient import client
        >>> freezer = client.Client('2',username='admin',password='stack')

    Here ``VERSION`` is freezer API Version, you can use ``1``(v1) or ``2``
    (v2),default is API v2.

    Alternatively, you can create a client instance using the keystoneauth
    session API. See "The freezerclient Python API" page at
    python-freezerclient's doc.
    """
    if endpoint:
        kwargs["endpoint"] = endpoint
    else:
        kwargs["endpoint"] = os.environ.get('OS_BACKUP_URL')

    if username:
        kwargs["username"] = username
    else:
        kwargs["username"] = os.environ.get('OS_USERNAME')

    if password:
        kwargs["password"] = password
    else:
        kwargs["password"] = os.environ.get('OS_PASSWORD')

    if project_name:
        kwargs["project_name"] = project_name
    else:
        kwargs["project_name"] = os.environ.get('OS_PROJECT_NAME')

    if auth_url:
        kwargs["auth_url"] = auth_url
    else:
        kwargs["auth_url"] = os.environ.get('OS_AUTH_URL')

    if token:
        kwargs["token"] = token
    else:
        kwargs["token"] = os.environ.get('OS_TOKEN')

    kwargs["project_domain_name"] = os.environ.get('OS_PROJECT_DOMAIN_NAME')
    if project_domain_name:
        kwargs["project_domain_name"] = project_domain_name

    if user_domain_name:
        kwargs["user_domain_name"] = user_domain_name
    else:
        kwargs["user_domain_name"] = os.environ.get('OS_USER_DOMAIN_NAME')

    if user_domain_id:
        kwargs["user_domain_id"] = user_domain_id
    else:
        kwargs["user_domain_id"] = os.environ.get('OS_USER_DOMAIN_ID')

    if project_id:
        kwargs["project_id"] = project_id
    else:
        kwargs["project_id"] = os.environ.get('OS_PROJECT_ID')

    kwargs["cacert"] = cacert or os.environ.get('OS_CACERT')
    kwargs["endpoint_type"] = os.environ.get('OS_ENDPOINT_TYPE') or 'public'

    if not version:
        version = os.environ.get('OS_BACKUP_API_VERSION', '2')

    client_class = utils.get_client_class(version)

    return client_class(**kwargs)
