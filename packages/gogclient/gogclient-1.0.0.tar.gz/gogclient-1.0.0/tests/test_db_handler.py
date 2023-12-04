""" module:: tests.db_handler
    :platform: All
    :synopsis: A selection of pytest tests
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import pytest
from pathlib import Path

from gogclient.db_handler import DataBaseHandler


@pytest.fixture
def real_repo_database() -> DataBaseHandler:
    real_db_path = Path("../gog_repo.db3")
    if real_db_path.exists():
        with DataBaseHandler(real_db_path) as dbh:
            yield dbh
    else:
        pytest.skip("No real Database")


@pytest.mark.skip("Incomplete")
class TestDataBaseHandler:

    @pytest.mark.parametrize("product_id,url,name,version",
                             [(2007520286, "/downloads/shivers/80068", "manual", None),
                              (2056019722, "/downloads/house_party/en1patch1",
                               "Patch (1.0.7 Xmas to 1.0.7 Xmas Redeploy)", "1.0.7 Xmas Redeploy"),  # real entry!
                              (2056019722, "/downloads/house_party/en1patch123456",
                               "Patch (1.0.7 Xmas to 1.0.7 Xmas Redeploy)", "1.0.7 Xmas Redeploy"),
                              # same name but different url!
                              ])
    def test_is_download_in_db(self,
                               real_repo_database,
                               product_id,
                               url,
                               name,
                               version):
        result = real_repo_database.is_download_in_db(product_id=product_id,
                                                      url=url,
                                                      name=name,
                                                      version=version)
        assert result is True


    @pytest.mark.parametrize("product_id, expected", [
        (1, []),
        (1207661413, [1207661423, 1207661433])
    ])
    def test_get_product_siblings(self,
                                  real_repo_database,
                                  product_id,
                                  expected,
                                  ):
        result = real_repo_database.get_product_siblings(product_id=product_id)
        assert result == expected

    @pytest.mark.parametrize("product_id, extra_name, expected", [
        #(1207661413, "manuals (68 pages)", True),
        (1207661413, "Space Quest 1 - The Sarien Encounter", False)

    ])
    def test_is_extra_a_duplicate(self,
                                  real_repo_database,
                                  product_id,
                                  extra_name,
                                  expected,
                                  ):
        result = real_repo_database.is_extra_a_duplicate(product_id=product_id, extra_name=extra_name)
        assert result == expected


    def test_get_owned_products_with_missing_downloads(self,
                                                       real_repo_database):
        owned_products_with_missing_downloads = real_repo_database.get_owned_products_with_missing_downloads()
        print(len(owned_products_with_missing_downloads))
        for product_id in owned_products_with_missing_downloads:
            print(product_id)
            for download_id, url, download_name, download_size in real_repo_database.get_latest_downloads_without_files(
                    product_id=product_id):
                print(url, download_name, download_size)

    @pytest.mark.parametrize("product_id, url",[
        (1075216797, "https://www.gog.com/game/greak_memories_of_azur_deluxe_edition"),
    ])
    def test_get_url_for_product_id(self, real_repo_database, product_id, url):
        assert real_repo_database.get_url_for_product_id(product_id) == url
