import pytest

from pybiomart import Dataset
from pybiomart.server import Server

# pylint: disable=redefined-outer-name, no-self-use


@pytest.fixture
def query_params():
    """Example query parameters."""

    return {
        'attributes': ['ensembl_gene_id'],
        'filters': {
            'chromosome_name': ['1']
        }
    }


class TestDatasetStatic(object):
    """Static (offline) tests for Dataset class."""

    def test_attibutes(self, mock_dataset):
        """Tests basic attributes."""
        assert mock_dataset.name == 'mmusculus_gene_ensembl'
        assert mock_dataset.display_name == 'Mus musculus genes (GRCm38.p4)'

    def test_fetch_configuration(self, mocker, mock_dataset,
                                 dataset_config_response):
        """Tests fetching of filters/attributes."""

        mock_get = mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_config_response)

        assert len(mock_dataset.filters) > 0
        assert len(mock_dataset.attributes) > 0

        mock_get.assert_called_once_with(
            type='configuration', dataset=mock_dataset.name)

    def test_fetch_attribute(self, mocker, mock_dataset,
                             dataset_config_response):
        """Tests attributes of example attribute."""

        mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_config_response)

        # Test example attribute.
        attr = mock_dataset.attributes['ensembl_gene_id']
        assert attr.name == 'ensembl_gene_id'
        assert attr.display_name == 'Ensembl Gene ID'
        assert attr.description == 'Ensembl Stable ID of the Gene'
        assert attr.default

    def test_fetch_filters(self, mocker, mock_dataset,
                           dataset_config_response):
        """Tests attributes of example filter."""

        mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_config_response)

        # Test example filter.
        filt = mock_dataset.filters['chromosome_name']
        assert filt.name == 'chromosome_name'
        assert filt.type == 'list'
        assert filt.description == ''

    def test_query(self, mocker, mock_dataset_with_config, query_params,
                   dataset_query_response):
        """Tests example query."""

        mock_dataset = mock_dataset_with_config

        mock_get = mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_query_response)

        # Perform query.
        res = mock_dataset.query(**query_params)

        # Check query result.
        assert len(res) > 0
        assert 'Ensembl Gene ID' in res

        # Check query xml.
        query = b"""<Query datasetConfigVersion="0.6" formatter="TSV"
 header="1" uniqueRows="1" virtualSchemaName="default">
<Dataset interface="default" name="mmusculus_gene_ensembl">
<Attribute name="ensembl_gene_id" />
<Filter name="chromosome_name" value="1" />
</Dataset></Query>"""
        query = b''.join(query.split(b'\n'))

        mock_get.assert_called_once_with(query=query)

    def test_query_attr_name(self, mocker, mock_dataset_with_config,
                             query_params, dataset_query_response):
        """Tests example query, renaming columns to names."""

        mock_dataset = mock_dataset_with_config

        mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_query_response)

        # Perform query.
        res = mock_dataset.query(use_attr_names=True, **query_params)

        # Check query result.
        assert len(res) > 0
        assert 'ensembl_gene_id' in res

    def test_query_data_types(self, mocker, mock_dataset_with_config,
                             query_params, dataset_query_response):
        """Tests example query with data types specified."""

        mock_dataset = mock_dataset_with_config

        mock_get = mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_query_response)

        data_types = {'Ensembl Gene ID': str}
        query_params['dtypes'] = data_types

        # Perform query.
        res = mock_dataset.query(**query_params)

        # Check query result.
        assert len(res) > 0
        assert 'Ensembl Gene ID' in res

    def test_query_non_valid_data_types(self, mocker, mock_dataset_with_config,
                                         query_params, dataset_query_response):
        """Tests example query with non valid data types specified."""

        mock_dataset = mock_dataset_with_config

        mock_get = mocker.patch.object(
            mock_dataset, 'get', return_value=dataset_query_response)

        data_types = {'Ensembl Gene ID': 'hello'}
        query_params['dtypes'] = data_types

        # Perform query.
        with pytest.raises(ValueError):
            res = mock_dataset.query(**query_params)



class TestDatasetLive(object):
    """Live unit tests for dataset."""

    def test_ensembl(self):
        """Tests example query to ensembl."""

        dataset = Dataset(
            name='hsapiens_gene_ensembl',
            host='http://www.ensembl.org',
            use_cache=False)

        result = dataset.query(
            attributes=['ensembl_gene_id', 'external_gene_name'])

        assert result.shape[0] > 0
        assert result.shape[1] == 2
