import pytest

from pybiomart.server import Server

# pylint: disable=redefined-outer-name, no-self-use


class TestServerStatic(object):
    """Offline unit tests for Server (using a static response)."""

    def test_marts(self, mocker, server_marts_response):
        """Test fetching marts."""

        mock_get = mocker.patch.object(
            Server, 'get', return_value=server_marts_response)

        server = Server(host='http://www.ensembl.org')

        assert len(server.marts) > 0
        mock_get.assert_called_once_with(type='registry')

    def test_get_item(self, mocker, server_marts_response):
        """Test getting mart as key."""

        mock_get = mocker.patch.object(
            Server, 'get', return_value=server_marts_response)

        server = Server(host='http://www.ensembl.org')
        mart = server['ENSEMBL_MART_ENSEMBL']

        assert mart.name == 'ENSEMBL_MART_ENSEMBL'
        mock_get.assert_called_once_with(type='registry')
