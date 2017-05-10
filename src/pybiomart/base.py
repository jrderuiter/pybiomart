from __future__ import absolute_import, division, print_function

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

import requests
import requests_cache

DEFAULT_HOST = 'http://www.biomart.org'
DEFAULT_PATH = '/biomart/martservice'
DEFAULT_PORT = 80
DEFAULT_SCHEMA = 'default'

requests_cache.install_cache('.pybiomart')


class ServerBase(object):
    """Base class that handles requests to the biomart server.

    Attributes:
        host (str): Host to connect to for the biomart service.
        path (str): Path to the biomart service on the host.
        port (str): Port to connect to on the host.
        url (str): Url used to connect to the biomart service.
        use_cache (bool): Whether to cache requests to biomart.

    """

    def __init__(self, host=None, path=None, port=None, use_cache=True):
        """ServerBase constructor.

        Args:
            host (str): Url of host to connect to.
            path (str): Path on the host to access to the biomart service.
            port (int): Port to use for the connection.
            use_cache (bool): Whether to cache requests.

        """
        # Use defaults if arg is None.
        host = host or DEFAULT_HOST
        path = path or DEFAULT_PATH
        port = port or DEFAULT_PORT

        # Add http prefix and remove trailing slash.
        host = self._add_http_prefix(host)
        host = self._remove_trailing_slash(host)

        # Ensure path starts with slash.
        if not path.startswith('/'):
            path = '/' + path

        self._host = host
        self._path = path
        self._port = port
        self._use_cache = use_cache

    @property
    def host(self):
        """Host to connect to for the biomart service."""
        return self._host

    @property
    def path(self):
        """Path to the biomart service on the host."""
        return self._path

    @property
    def port(self):
        """Port to connect to on the host."""
        return self._port

    @property
    def url(self):
        """Url used to connect to the biomart service."""
        return '{}:{}{}'.format(self._host, self._port, self._path)

    @property
    def use_cache(self):
        """Whether to cache requests to biomart."""
        return self._use_cache

    @staticmethod
    def _add_http_prefix(url, prefix='http://'):
        if not url.startswith('http://') or url.startswith('https://'):
            url = prefix + url
        return url

    @staticmethod
    def _remove_trailing_slash(url):
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get(self, **params):
        """Performs get request to the biomart service.

        Args:
            **params (dict of str: any): Arbitrary keyword arguments, which
                are added as parameters to the get request to biomart.

        Returns:
            requests.models.Response: Response from biomart for the request.

        """
        if self._use_cache:
            r = requests.get(self.url, params=params)
        else:
            with requests_cache.disabled():
                r = requests.get(self.url, params=params)
        r.raise_for_status()
        return r


class BiomartException(Exception):
    """Basic exception class for biomart exceptions."""
    pass
