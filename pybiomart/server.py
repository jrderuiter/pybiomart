from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

from xml.etree.ElementTree import fromstring as xml_from_string

from .base import ServerBase
from .mart import Mart


class Server(ServerBase):

    """Biomart server class.

    Represents a biomart server. Typically used as main entry point to the
    biomart server, by providing functionality for listing and loading
    the databases that are available on the server.

    Attributes:
        marts (list of Marts): Marts available on the server.

    Examples:
        Connecting to a server:
        >>> server = Server(host='http://www.ensembl.org')

        Retrieving a database:
        >>> database = server.marts['ENSEMBL_MART_ENSEMBL']

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
        """Server constructor.

        Args:
            host (str): Url of host to connect to.
            path (str): Path on the host to access to the biomart service.
            port (int): Port to use for the connection.
            use_cache (bool): Whether to cache requests.

        """

        super().__init__(host=host, path=path,
                         port=port, use_cache=use_cache)
        self._marts = None

    def __getitem__(self, name):
        return self._marts[name]

    @property
    def marts(self):
        """List of available databases."""
        if self._marts is None:
            self._marts = self._fetch_marts()
        return self._marts

    def _fetch_marts(self):
        response = self.get(type='registry')

        xml = xml_from_string(response.text)
        marts = [self._mart_from_xml(child)
                 for child in xml.findall('MartURLLocation')]

        return {m.name: m for m in marts}

    def _mart_from_xml(self, node):
        params = {k: node.attrib[v]
                  for k, v in self._MART_XML_MAP.items()}
        params['extra_params'] = {k: v for k, v in node.attrib.items()
                                  if k not in set(self._MART_XML_MAP.values())}
        return Mart(use_cache=self.use_cache, **params)

    def __repr__(self):
        return ('<biomart.Server host={!r}, path={!r}, port={!r}>'
                .format(self.host, self.path, self.port))
