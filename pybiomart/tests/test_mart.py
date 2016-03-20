import os
import pickle
import mock

import pytest
import pkg_resources

from .. import mart as mart_mod
from ..server import Server

from .test_server import marts_request


@pytest.fixture
def datasets_request():
    """Loads cached mart request from pickle."""

    # Code for saving pickle.
    # req = mart.get(type='datasets', mart=mart._name)
    # with open('mart_request.pkl', 'wb') as file_:
    #     pickle.dump(req, file=file_, protocol=2)

    # Load cached request.
    rel_path = os.path.join('tests', 'data', 'datasets_request.pkl')
    file_path = pkg_resources.resource_filename(mart_mod.__name__, rel_path)

    with open(file_path, 'rb') as file_:
        return pickle.load(file_)


@pytest.fixture
def mart(marts_request):
    """Returns a default mart for testing."""

    with mock.patch.object(Server, 'get', return_value=marts_request):
        server_obj = Server(host='http://www.ensembl.org')
        return server_obj['ENSEMBL_MART_ENSEMBL']


class TestMart(object):

    def test_attributes(self, mart):
        assert mart.name == 'ENSEMBL_MART_ENSEMBL'
        assert mart.display_name == 'Ensembl Genes 84'
        assert mart.database_name == 'ensembl_mart_84'

    def test_datasets(self, mart, datasets_request):
        with mock.patch.object(mart_mod.Mart, 'get',
                               return_value=datasets_request) as mock_get:
            assert len(mart.datasets) > 0
            mock_get.assert_called_once_with(type='datasets',
                                             mart='ENSEMBL_MART_ENSEMBL')

    def test_get_item(self, mart, datasets_request):
        with mock.patch.object(mart_mod.Mart, 'get',
                               return_value=datasets_request) as mock_get:
            dataset = mart['mmusculus_gene_ensembl']
            assert dataset.name == 'mmusculus_gene_ensembl'
