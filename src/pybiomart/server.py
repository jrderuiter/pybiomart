from __future__ import absolute_import, division, print_function

# pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import
from builtins import *
# pylint: enable=wildcard-import,redefined-builtin,unused-wildcard-import

from xml.etree.ElementTree import fromstring as xml_from_string

import pandas as pd

# pylint: disable=import-error
from .base import ServerBase
from .mart import Mart

# pylint: enable=import-error


class Server(ServerBase):
    """Class representing a biomart server.

    Typically used as main entry point to the biomart server. Provides
    functionality for listing and loading the marts that are available
    on the server.

    Args:
        host (str): Url of host to connect to.
        path (str): Path on the host to access to the biomart service.
        port (int): Port to use for the connection.
        use_cache (bool): Whether to cache requests.

    Examples:
        Connecting to a server and listing available marts:
            >>> server = Server(host='http://www.ensembl.org')
            >>> server.list_marts()

        Retrieving a mart:
            >>> mart = server['ENSEMBL_MART_ENSEMBL']

    """

    _MART_XML_MAP = {
        'name': 'name',
        'database_name': 'database',
        'display_name': 'displayName',
        'host': 'host',
        'path': 'path',
        'virtual_schema': 'serverVirtualSchema'
    }

    def __init__(self, host=None, path=None, port=None, use_cache=True):
        super().__init__(host=host, path=path, port=port, use_cache=use_cache)
        self._marts = None

    def __getitem__(self, name):
        return self.marts[name]

    @property
    def marts(self):
        """List of available marts."""
        if self._marts is None:
            self._marts = self._fetch_marts()
        return self._marts

    def list_marts(self):
        """Lists available marts in a readable DataFrame format.

        Returns:
            pd.DataFrame: Frame listing available marts.
        """

        def _row_gen(attributes):
            for attr in attributes.values():
                yield (attr.name, attr.display_name)

        return pd.DataFrame.from_records(
            _row_gen(self.marts), columns=['name', 'display_name'])

    def _fetch_marts(self):
        response = self.get(type='registry')

        xml = xml_from_string(response.content)
        marts = [
            self._mart_from_xml(child)
            for child in xml.findall('MartURLLocation')
        ]

        return {m.name: m for m in marts}

    def _mart_from_xml(self, node):
        params = {k: node.attrib[v] for k, v in self._MART_XML_MAP.items()}
        params['extra_params'] = {
            k: v
            for k, v in node.attrib.items()
            if k not in set(self._MART_XML_MAP.values())
        }
        return Mart(use_cache=self.use_cache, **params)

    def __repr__(self):
        return ('<biomart.Server host={!r}, path={!r}, port={!r}>'
                .format(self.host, self.path, self.port))
