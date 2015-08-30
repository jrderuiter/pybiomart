from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import requests

DEFAULT_HOST = 'http://www.biomart.org'
DEFAULT_PATH = '/biomart/martservice'
DEFAULT_PORT = 80
DEFAULT_SCHEMA = 'default'


class ServerBase(object):

    def __init__(self, host=None, path=None, port=None):
        host = host or DEFAULT_HOST
        path = path or DEFAULT_PATH
        port = port or DEFAULT_PORT

        self._host = self._add_http_prefix(host)
        self._path = path
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def path(self):
        return self._path

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._host + self._path

    @staticmethod
    def _add_http_prefix(url, prefix='http://'):
        if not url.startswith('http://') or url.startswith('https://'):
            url = prefix + url
        return url

    def get(self, **params):
        r = requests.get(self.url, params=params)
        r.raise_for_status()
        return r

    def post(self, params):
        pass


class BiomartException(Exception):
    pass
