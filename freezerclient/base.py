# (c) Copyright 2026 Cleura AB
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

from cliff import command
from cliff import lister
from cliff import show


def get_client(app):
    if hasattr(app, 'client_manager') and not hasattr(app, 'client'):
        return app.client_manager.backup
    return app.client


class FreezerCommand(command.Command):

    @property
    def client(self):
        return get_client(self.app)


class FreezerLister(lister.Lister):

    @property
    def client(self):
        return get_client(self.app)


class FreezerShowOne(show.ShowOne):

    @property
    def client(self):
        return get_client(self.app)
