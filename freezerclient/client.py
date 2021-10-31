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
# from typing import Any

import os


def Client(version: str = None, endpoint: str = None, username: str = None,
           password: str = None, project_name: str = None,
           auth_url: str = None,
           project_id: str = None, token: str = None, cacert: str = None,
           project_domain_name: str = None, user_domain_id: str = None,
           user_domain_name: str = None, project_domain_id: str = None,
           **kwargs) -> str:
    """Initialize client object based on given version.

    HOW-TO:
    The simplest way to create a client instance is initialization with your
    credentials::

        >>> from freezerclient import client
        >>> freezer = client.Client('2',username='admin',password='stack')

    Here ``VERSION`` is freezer API VersrPython API" page at
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

    if project_domain_id:
        kwargs["project_domain_id"] = project_domain_id
    else:
        kwargs["project_domain_id"] = os.environ.get('OS_PROJECT_DOMAIN_ID')

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
