from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import pandas as pd
from io import StringIO
from xml.etree import ElementTree

from .base import ServerBase, BiomartException, DEFAULT_SCHEMA


class Dataset(ServerBase):

    """Biomart dataset.

    Main Dataset class that handles queries to biomart datasets. Queries
    can select a subset of attributes (valid attributes are listed in
    the attributes property) and filtered using a subset of filters
    (valid filters are available in the filters property).

    Attributes:
        name (str): Id of the dataset.
        display_name (str): Display name of the dataset.
        virtual_schema (str): Name of the datasets virtual schema.
        filters (list of biomart.Filter): List of dataset filters.
        attributes (list of biomart.Attribute): List of dataset attributes.

    Examples:
        Directly connecting to a dataset:
            >>> dataset = Dataset(name='hsapiens_gene_ensembl',
            >>>                   host='http://www.ensembl.org')

        Querying the dataset:
            >>> dataset.query(attributes=['ensembl_gene_id',
            >>>                           'external_gene_name'],
            >>>               filters={'chromosome_name': ['1','2']})

        Listing available attributes:
            >>> dataset.attributes
            >>> dataset.list_attributes()

        Listing available filters:
            >>> dataset.filters

    """

    def __init__(self, name, display_name='', host=None,
                 path=None, port=None, use_cache=True,
                 virtual_schema=DEFAULT_SCHEMA):
        """Dataset constructor.

        Args:
            name (str): Id of the dataset.
            display_name (str): Display name of the dataset.
            host (str): Url of host to connect to.
            path (str): Path on the host to access to the biomart service.
            port (int): Port to use for the connection.
            use_cache (bool): Whether to cache requests.
            virtual_schema (str): The virtual schema of the dataset.

        """
        super().__init__(host=host, path=path,
                         port=port, use_cache=use_cache)

        self._name = name
        self._display_name = display_name
        self._virtual_schema = virtual_schema

        self._filters = None
        self._attributes = None

    @property
    def name(self):
        """Id of the dataset."""
        return self._name

    @property
    def display_name(self):
        """Display name of the dataset."""
        return self._display_name

    @property
    def filters(self):
        """List of filters available for the dataset (cached)."""
        if self._filters is None:
            self._filters, self._attributes = self._fetch_configuration()
        return self._filters

    @property
    def attributes(self):
        """List of attributes available for the dataset (cached)."""
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
        """Queries the dataset to retrieve the contained data.

        Args:
            attributes (list of str): Names of attributes to fetch in query.
                Attribute names must correspond to valid attributes. See
                the attributes property for a list of valid attributes.
            filters (dict of str: any): Dictionary of filters --> values
                to filter the dataset by. Filter names and values must
                correspond to valid filters and filter values. See the
                filters property for a list of valid filters.

        Returns:
            pandas.DataFrame: DataFrame containing the query results.

        """

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
        root.set('virtualSchemaName', self._virtual_schema)
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
                try:
                    attr = self.attributes[name]
                    self._add_attr_node(dataset, attr)
                except KeyError:
                    raise BiomartException(
                        'Unknown attribute {}, check dataset attributes '
                        'for a list of valid attributes.'.format(name))

        if filters is not None:
            # Add filter elements.
            for name, value in filters.items():
                try:
                    filter_ = self.filters[name]
                    self._add_filter_node(dataset, filter_, value)
                except KeyError:
                    raise BiomartException(
                        'Unknown filter {}, check dataset filters '
                        'for a list of valid filters'.format(name))

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

    """Biomart dataset attribute.

    Attributes:
        name (str): Attribute name.
        display_name (str): Attribute display name.
        description (str): Attribute description.

    """

    def __init__(self, name, display_name='', description=''):
        """Attribute constructor.

        Args:
            name (str): Attribute name.
            display_name (str): Attribute display name.
            description (str): Attribute description.

        """
        self._name = name
        self._display_name = display_name
        self._description = description

    @property
    def name(self):
        """Name of the attribute."""
        return self._name

    @property
    def display_name(self):
        """Display name of the attribute."""
        return self._display_name

    @property
    def description(self):
        """Description of the attribute."""
        return self._description

    def __repr__(self):
        return (('<biomart.Attribute name={!r},'
                 ' display_name={!r}, description={!r}>')
                .format(self._name, self._display_name, self._description))


class Filter(object):

    """Biomart dataset filter.

    Attributes:
        name (str): Filter name.
        type (str): Type of the filter (boolean, int, etc.).
        description (str): Filter description.

    """

    def __init__(self, name, type, description=''):
        """ Filter constructor.

        Args:
            name (str): Filter name.
            type (str): Type of the filter (boolean, int, etc.).
            description (str): Filter description.

        """
        self._name = name
        self._type = type
        self._description = description

    @property
    def name(self):
        """Filter name."""
        return self._name

    @property
    def type(self):
        """Filter type."""
        return self._type

    @property
    def description(self):
        """Filter description."""
        return self._description

    def __repr__(self):
        return ('<biomart.Filter name={!r}, type={!r}>'
                .format(self.name, self.type))
