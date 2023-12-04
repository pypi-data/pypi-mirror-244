""" module:: tests.test_client
    :platform: All
    :synopsis: A selection of pytest tests
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import pytest

from gogclient.client import GOGClient

import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def gog_client() -> GOGClient:
    yield GOGClient()


class TestGOGClient:

    @pytest.mark.online
    def test_get_catalog_products(self, gog_client):
        result = gog_client.get_catalog_products(price=(1, 15))
        assert result

    @pytest.mark.online
    @pytest.mark.skip("Requires user interaction")
    def test_login(self, gog_client):
        with gog_client:
            assert gog_client.is_logged_in()
