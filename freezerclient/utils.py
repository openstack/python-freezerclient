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


import json
import logging

logging = logging.getLogger(__name__)


class Namespace(dict):
    """A dict subclass that exposes its items as attributes.

    Warning: Namespace instances do not have direct access to the
    dict methods.

    """

    def __init__(self, obj={}):
        super(Namespace, self).__init__(obj)

    def __dir__(self):
        return tuple(self)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__,
                           super(Namespace, self).__repr__())

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            # Return None in case the value doesn't exists
            # this is not an issue for the apiclient because it skips
            # None values
            return None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    @classmethod
    def from_object(cls, obj, names=None):
        if names is None:
            names = dir(obj)
        ns = {name: getattr(obj, name) for name in names}
        return cls(ns)

    @classmethod
    def from_mapping(cls, ns, names=None):
        if names:
            ns = {name: ns[name] for name in names}
        return cls(ns)

    @classmethod
    def from_sequence(cls, seq, names=None):
        if names:
            seq = {name: val for name, val in seq if name in names}
        return cls(seq)

    @staticmethod
    def hasattr(ns, name):
        try:
            object.__getattribute__(ns, name)
        except AttributeError:
            return False
        return True

    @staticmethod
    def getattr(ns, name):
        return object.__getattribute__(ns, name)

    @staticmethod
    def setattr(ns, name, value):
        return object.__setattr__(ns, name, value)

    @staticmethod
    def delattr(ns, name):
        return object.__delattr__(ns, name)


class CachedProperty(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def doc_from_json_file(path_to_file):
    """Build a json from a file in the file system
    :param path_to_file: path to file
    :return: in memory file in json format
    """
    with open(path_to_file, 'rb') as fd:
        try:
            return json.load(fd)
        except Exception as err:
            logging.error(err)
            raise Exception('Unable to load conf file. {0}'.format(err))


def create_headers_for_request(token):
    """Create a header dict to be passed to the api.

    :param token: token string coming from the api
    :return: a dict containing all the headers for a request
    """
    return {
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


def prepare_search(search_term):
    """Return a search term that the api can use to query the db
    :param search_term: string
    :return: search dict
    """
    if search_term:
        return {"match": [{"_all": search_term}, ], }
    return {}
