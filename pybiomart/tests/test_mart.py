import os
import pickle
import mock

import pytest
import pkg_resources

# pylint: disable=import-error
from ._mock import MockResponse

# pylint: disable=import-self
from .. import mart
from ..server import Server

# pylint: disable=redefined-outer-name,unused-import
from .test_server import marts_response


@pytest.fixture
def datasets_response():
    """Loads cached mart request from pickle."""

    # Code for saving pickle.
    # req = mart.get(type='datasets', mart=mart._name)
    # with open('mart_request.pkl', 'wb') as file_:
    #     pickle.dump(req, file=file_, protocol=2)

    # Load cached request.
    rel_path = os.path.join('tests', 'data', 'datasets_response.pkl')
    file_path = pkg_resources.resource_filename(mart.__name__, rel_path)

    with open(file_path, 'rb') as file_:
        return MockResponse(text=pickle.load(file_))


# pylint: disable=no-self-use
@pytest.fixture
def mart_(marts_response):
    """Returns a default mart for testing."""

    with mock.patch.object(Server, 'get', return_value=marts_response):
        server_obj = Server(host='http://www.ensembl.org')
        return server_obj['ENSEMBL_MART_ENSEMBL']


class TestMart(object):

    def test_attributes(self, mart_):
        assert mart_.name == 'ENSEMBL_MART_ENSEMBL'
        assert mart_.display_name == 'Ensembl Genes 84'
        assert mart_.database_name == 'ensembl_mart_84'

    def test_datasets(self, mart_, datasets_response):
        with mock.patch.object(mart_, 'get',
                               return_value=datasets_response) as mock_get:
            assert len(mart_.datasets) > 0
            mock_get.assert_called_once_with(type='datasets',
                                             mart='ENSEMBL_MART_ENSEMBL')

    def test_get_item(self, mart_, datasets_response):
        with mock.patch.object(mart_, 'get', return_value=datasets_response):
            dataset = mart_['mmusculus_gene_ensembl']
            assert dataset.name == 'mmusculus_gene_ensembl'
