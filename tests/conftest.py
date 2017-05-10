from os import path
import pickle
import pkg_resources

import pytest

from pybiomart import Server

BASE_DIR = path.dirname(__file__)


@pytest.helpers.register
def data_path(relative_path, relative_to=BASE_DIR):
    """Returns data path to test file."""

    return path.join(relative_to, 'data', relative_path)


class MockResponse(object):
    """Mock response class."""

    def __init__(self, text=''):
        self.text = text
        self.content = text.encode('utf-8')

    def raise_for_status(self):
        """Mock raise_for_status function."""
        pass


@pytest.helpers.register
def mock_response(text=''):
    """Helper function for creating a mock response."""
    return MockResponse(text=text)


@pytest.fixture
def server_marts_response():
    """Returns a cached Server response containing marts."""

    # Code for saving cached request.
    # server = Server(host='http://www.ensembl.org')
    # req = server.get(type='registry')
    # with open('server_request.pkl', 'wb') as file_:
    #     pickle.dump(req.text, file=file_, protocol=2)

    # Load cached request.
    file_path = pytest.helpers.data_path('marts_response.pkl')

    with open(file_path, 'rb') as file_:
        return MockResponse(text=pickle.load(file_))


@pytest.fixture
def mock_mart(mocker, server_marts_response):
    """Returns an example mart, built using a cached response."""

    mocker.patch.object(Server, 'get', return_value=server_marts_response)

    server = Server(host='http://www.ensembl.org')
    return server['ENSEMBL_MART_ENSEMBL']


@pytest.fixture
def mart_datasets_response():
    """Returns a cached Mart response containing datasets."""

    # Code for saving pickle.
    # req = mart.get(type='datasets', mart=mart._name)
    # with open('mart_request.pkl', 'wb') as file_:
    #     pickle.dump(req, file=file_, protocol=2)

    # Load cached request.
    file_path = pytest.helpers.data_path('datasets_response.pkl')

    with open(file_path, 'rb') as file_:
        return pytest.helpers.mock_response(text=pickle.load(file_))


@pytest.fixture
def mock_dataset(mocker, mock_mart, mart_datasets_response):
    """Returns an example dataset, built using a cached response."""

    mocker.patch.object(mock_mart, 'get', return_value=mart_datasets_response)
    return mock_mart.datasets['mmusculus_gene_ensembl']


@pytest.fixture
def mock_dataset_with_config(mocker, mock_dataset, dataset_config_response):
    """Returns an example dataset, mocked to return a configuration."""

    mocker.patch.object(
        mock_dataset, 'get', return_value=dataset_config_response)
    mock_dataset.attributes
    return mock_dataset


@pytest.fixture
def dataset_config_response():
    """Returns a cached Dataset config response."""

    # Dumped using the following code.
    # req = dataset.get(type='configuration', dataset=dataset_.name)
    # with open('config_response.pkl', 'wb') as file_:
    #    pickle.dump(req, file=file_, protocol=2)

    # Load cached request.
    file_path = pytest.helpers.data_path('config_response.pkl')

    with open(file_path, 'rb') as file_:
        return pytest.helpers.mock_response(pickle.load(file_))


@pytest.fixture
def dataset_query_response():
    """Returns a cached Dataset query response."""

    # Dumped from inside query using the below code.
    # import pickle
    # with open('query_response.pkl', 'wb') as file_:
    #    pickle.dump(response, file=file_, protocol=2)

    # Load cached request.
    file_path = pytest.helpers.data_path('query_response.pkl')

    with open(file_path, 'rb') as file_:
        return pytest.helpers.mock_response(pickle.load(file_))
