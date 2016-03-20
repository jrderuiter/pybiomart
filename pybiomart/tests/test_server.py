import os
import pickle
import mock

import pytest
import pkg_resources

from .. import server
from ..server import Server


@pytest.fixture
def marts_request():
    # Code for saving cached request.
    # server = Server(host='http://www.ensembl.org')
    # req = server.get(type='registry')
    # with open('server_request.pkl', 'wb') as file_:
    #     pickle.dump(req, file=file_, protocol=2)

    # Load cached request.
    rel_path = os.path.join('tests', 'data', 'marts_request.pkl')
    file_path = pkg_resources.resource_filename(server.__name__, rel_path)

    with open(file_path, 'rb') as file_:
        return pickle.load(file_)


class TestServer(object):

    def test_marts(self, marts_request):
        """Test fetching marts."""

        with mock.patch.object(Server, 'get',
                               return_value=marts_request) as mock_get:
            server = Server(host='http://www.ensembl.org')

            assert len(server.marts) > 0
            mock_get.assert_called_once_with(type='registry')

    def test_get_item(self, marts_request):
        """Test getting mart as key."""

        with mock.patch.object(Server, 'get',
                               return_value=marts_request) as mock_get:
            server = Server(host='http://www.ensembl.org')
            mart = server['ENSEMBL_MART_ENSEMBL']

            assert mart.name == 'ENSEMBL_MART_ENSEMBL'
            mock_get.assert_called_once_with(type='registry')
