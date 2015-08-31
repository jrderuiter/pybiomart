from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import pandas as pd
from io import StringIO
from xml.etree import ElementTree

from .base import ServerBase, DEFAULT_SCHEMA


class Dataset(ServerBase):

    def __init__(self, name, display_name='', host=None,
                 path=None, port=None, use_cache=True,
                 virtual_schema=DEFAULT_SCHEMA):
        super().__init__(host=host, path=path,
                         port=port, use_cache=use_cache)

        self._name = name
        self._display_name = display_name
        self._virtual_schema = virtual_schema

        self._filters = None
        self._attributes = None

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

    @property
    def filters(self):
        if self._filters is None:
            self._filters, self._attributes = self._fetch_configuration()
        return self._filters

    @property
    def attributes(self):
        if self._attributes is None:
            self._filters, self._attributes = self._fetch_configuration()
        return self._attributes

    def list_attributes(self):
        def _row_gen(attributes):
            for attr in attributes.values():
                yield (attr.name, attr.display_name, attr.description)

        return pd.DataFrame.from_records(
            _row_gen(self.attributes),
            columns=['name', 'display_name', 'description'])

    def _fetch_configuration(self):
        # Get datasets using biomart.
        response = self.get(type='configuration', dataset=self._name)

        # Get filters and attributes from xml.
        xml = ElementTree.fromstring(response.text)

        filters = {f.name: f for f in self._filters_from_xml(xml)}
        attributes = {a.name: a for a in self._attributes_from_xml(xml)}

        return filters, attributes

    @staticmethod
    def _filters_from_xml(xml):
        for node in xml.iter('FilterDescription'):
            attrib = node.attrib
            yield Filter(name=attrib['internalName'],
                         type=attrib.get('type', ''))

    @staticmethod
    def _attributes_from_xml(xml):
        for page in xml.iter('AttributePage'):
            for desc in page.iter('AttributeDescription'):
                attrib = desc.attrib
                yield Attribute(name=attrib['internalName'],
                                display_name=attrib.get('displayName', ''),
                                description=attrib.get('description', ''))

    def query(self, attributes=None, filters=None):
        # Example query from Ensembl biomart:
        #
        # <?xml version="1.0" encoding="UTF-8"?>
        # <!DOCTYPE Query>
        # <Query  virtualSchemaName = "default" formatter = "TSV" header = "0"
        #  uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
        #   <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
        #       <Filter name = "chromosome_name" value = "1,2"/>
        #       <Filter name = "end" value = "10000000"/>
        #       <Filter name = "start" value = "1"/>
        #       <Attribute name = "ensembl_gene_id" />
        #       <Attribute name = "ensembl_transcript_id" />
        #   </Dataset>
        # </Query>

        # Setup query element.
        root = ElementTree.Element('Query')
        # root.set('virtualSchemaName', self._virtual_schema)
        root.set('formatter', 'TSV')
        root.set('header', '1')
        root.set('uniqueRows', '1')
        root.set('datasetConfigVersion', '0.6')

        # Add dataset element.
        dataset = ElementTree.SubElement(root, 'Dataset')
        dataset.set('name', self.name)
        dataset.set('interface', 'default')

        if attributes is not None:
            # Add attribute elements.
            for name in attributes:
                attr = self.attributes[name]
                self._add_attr_node(dataset, attr)

        if filters is not None:
            # Add filter elements.
            for name, value in filters.items():
                filter_ = self.filters[name]
                self._add_filter_node(dataset, filter_, value)

        # Fetch and parse response into a DataFrame.
        response = self.get(query=ElementTree.tostring(root))
        result = pd.read_csv(StringIO(response.text), sep='\t')

        return result

    @staticmethod
    def _add_attr_node(root, attr):
        attr_el = ElementTree.SubElement(root, 'Attribute')
        attr_el.set('name', attr.name)

    @staticmethod
    def _add_filter_node(root, filter_, value):
        """Adds filter xml node to root."""
        filter_el = ElementTree.SubElement(root, 'Filter')
        filter_el.set('name', filter_.name)

        # Set filter value depending on type.
        if filter_.type == 'boolean':
            # Boolean case.
            if value is True or value.lower() in {'included', 'only'}:
                filter_el.set('excluded', '0')
            elif value is False or value.lower() == 'excluded':
                filter_el.set('excluded', '1')
            else:
                raise ValueError('Invalid value for boolean filter ({})'
                                 .format(value))
        elif isinstance(value, list) or isinstance(value, tuple):
            # List case.
            filter_el.set('value', ','.join(map(str, value)))
        else:
            # Default case.
            filter_el.set('value', str(value))

    def __repr__(self):
        return ('<biomart.Dataset name={!r}, display_name={!r}>'
                .format(self._name, self._display_name))


class Attribute(object):

    def __init__(self, name, display_name='', description=''):
        self._name = name
        self._display_name = display_name
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    def __repr__(self):
        return (('<biomart.Attribute name={!r},'
                 ' display_name={!r}, description={!r}>')
                .format(self._name, self._display_name, self._description))


class Filter(object):

    def __init__(self, name, type, description=''):
        self._name = name
        self._type = type
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    def __repr__(self):
        return ('<biomart.Filter name={!r}, type={!r}>'
                .format(self.name, self.type))
