from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

from xml.etree.ElementTree import fromstring as xml_from_string

from .base import ServerBase
from .mart import Mart


class Server(ServerBase):

    MART_XML_MAP = {
        'name': 'name',
        'database_name': 'database',
        'display_name': 'displayName',
        'host': 'host',
        'path': 'path',
        'virtual_schema': 'serverVirtualSchema'
    }

    def __init__(self, host=None, path=None, port=None):
        super().__init__(host=host, path=path, port=port)
        self._marts = None

    def __getitem__(self, name):
        return self.marts[name]

    @property
    def marts(self):
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
                  for k, v in self.MART_XML_MAP.items()}
        params['extra_params'] = {k: v for k, v in node.attrib.items()
                                  if k not in set(self.MART_XML_MAP.values())}
        return Mart(**params)

    def __repr__(self):
        return ('<biomart.Server host={!r}, path={!r}, port={!r}>'
                .format(self.host, self.path, self.port))
