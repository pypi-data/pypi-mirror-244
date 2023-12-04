""" module:: gogclient.repo
    :platform: All
    :synopsis: A smart repository / mirror of your gog titles,
               it glues together the client and the db_handler
               presenting logical high level operations
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import stat
import time
from pathlib import Path
from typing import Optional, List

from requests import HTTPError

from gogclient.client import GOGClient
from gogclient.db_handler import DataBaseHandler
from gogclient.utils import filter_downloads, extract_product_title_from_product_data, filter_extras, \
    get_url_from_product_data, extract_product_type_from_product_data


def get_local_storage_path_for_product_id(product_id: int,
                                          dbh: DataBaseHandler,
                                          client: GOGClient,
                                          base_dir: Path,
                                          ) -> Path:
    assert base_dir.exists()
    storage_path = dbh.get_storage_path_for_product_id(product_id=product_id)
    if storage_path is None:
        # determine the storage path from slug
        if dbh.is_product_id_in_db(product_id=product_id):
            product_id, url, slug, product_type, timestamp = dbh.get_product_data_for_product_id(
                product_id=product_id)
            if product_type == "DLC":
                parent_id = dbh.get_base_product_for_dlc(product_id=product_id)
                parent_id, url, slug, product_type, timestamp = dbh.get_product_data_for_product_id(
                    product_id=parent_id)

            storage_path = slug.replace("-", "_")

        else:
            # this should not happen, we did this in conditionally_add_product_id_to_db
            # section to clean up previous data mess
            # example tomb raider 1-3 pack --> no product_page and no slug
            product_details = client.get_product_data(product_id=product_id)
            storage_path = extract_product_title_from_product_data(product_details).lower().replace(" ", "_").replace(
                ":", "")

        assert storage_path is not None

        dbh.set_storage_path_for_product_id(product_id=product_id, storage_path=Path(storage_path))

    filepath = base_dir / storage_path

    return filepath


class GOGRepo:

    def __init__(self,
                 client: Optional[GOGClient] = None,
                 dbh: Optional[DataBaseHandler] = None,
                 config: Optional[dict] = None,
                 ):
        self._config = config
        if self._config is not None:
            # preferred way of usage
            self._repo_path = Path(self._config.get("repo-base-dir"))
            self._dbh = DataBaseHandler(self._repo_path / "gog_repo.db3")
            self._log_base_dir = None
            log_base_dir = self._config.get("log-base-dir")
            if log_base_dir is not None:
                self._log_base_dir = Path(log_base_dir)
            self._client = GOGClient(log_base_path=self._log_base_dir)
        else:
            assert client is not None
            self._client = client
            assert dbh is not None
            self._dbh = dbh

    def __enter__(self):
        self._dbh.__enter__()
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.__exit__(exc_type, exc_val, exc_tb)
        self._dbh.__exit__(exc_type, exc_val, exc_tb)

    def update_owned_product_downloads(self,
                                       product_id: int,
                                       product_details: dict,
                                       dl_section: str = "DOWNLOAD",
                                       ):

        assert isinstance(product_details, dict)
        title = product_details.get("title")

        for language, os_dict in filter_downloads(downloads_dict=product_details.get("downloads"),
                                                  languages=self._config.get("prefered-languages"),
                                                  os_names=self._config.get("prefered-os"),
                                                  ).items():
            for os_name, os_downloads in os_dict.items():
                for os_download in os_downloads:
                    dl_name = os_download.get("name")
                    if dl_name == "DLC":
                        dl_name = title
                    self._dbh.add_download(product_id=product_id,
                                           language=language,
                                           os=os_name,
                                           url=os_download.get("manualUrl"),
                                           name=dl_name,
                                           version=os_download.get("version"),
                                           size=os_download.get("size"),
                                           dl_section=dl_section,
                                           )

        for extra_download in filter_extras(extras_list=product_details.get("extras"),
                                            languages=self._config.get("prefered-manual-languages"),
                                            audio_formats=["FLAC", "OGG", "MP3"],
                                            video_formats=["1080", ],
                                            os_list=["Linux", ]):
            if self._dbh.is_extra_a_duplicate(product_id=product_id, extra_name=extra_download.get("name")):
                print("Found an duplicate extra {name} {type} {size}".format_map(extra_download))
                continue
            if int(extra_download.get("size").split(" ")[0]) == 0:
                print("Found an zero size download {info} {name} {type} {size} {manualUrl}".format_map(extra_download))
                continue

            self._dbh.add_download(product_id=product_id,
                                   url=extra_download.get("manualUrl"),
                                   name=extra_download.get("name"),
                                   size=extra_download.get("size"),
                                   dl_section="EXTRA",
                                   dl_type=extra_download.get("type"),
                                   )
        for dlc in product_details.get("dlcs"):
            self.update_owned_product_downloads(product_id=product_id,
                                                product_details=dlc,
                                                dl_section="DLC")

        serial_keys = product_details.get("cdKey")
        if serial_keys is not None and len(serial_keys) > 0:
            if self._dbh.get_serial_key(product_id=product_id) is None:
                self._dbh.add_serial_key(product_id=product_id,
                                         serial_key=product_details.get("cdKey"))
                filepath = get_local_storage_path_for_product_id(product_id=product_id,
                                                                 dbh=self._dbh,
                                                                 client=self._client,
                                                                 base_dir=self._repo_path)
                if not filepath.exists():
                    Path.mkdir(filepath, parents=True)
                serials_filepath = filepath / "serials.txt"
                with serials_filepath.open(mode="w") as serials_file:
                    serials_file.write(serial_keys)

    def get_downloads_for_product(self,
                                  product_id: int):
        # must be used with client and dbh
        filepath = get_local_storage_path_for_product_id(product_id=product_id,
                                                         dbh=self._dbh,
                                                         client=self._client,
                                                         base_dir=self._repo_path)
        print("Saving to {0}".format(filepath))
        if not filepath.exists():
            Path.mkdir(filepath, parents=True)

        for download_id, url, download_name, download_size in self._dbh.get_latest_downloads_without_files(
                product_id=product_id):

            time.sleep(1)
            try:
                file_info = self._client.download_game_file(url=url,
                                                            filepath=filepath,
                                                            )
            except HTTPError as e:
                # found problem with dead links in Warhammer 2022 Goodies, can be found by using the "info" key,
                # which invalidates the link as it seems
                print("Problem {0} for {1} --> {2}".format(e, download_name, url))
                self._dbh.add_broken_download(download_id=download_id,
                                              http_error=int(str(e).split(" ", maxsplit=1)[0]))

            else:
                if file_info.get("file_ok") is True:
                    self._dbh.add_file(download_id=download_id,
                                       filename=file_info.get("filepath").name,
                                       size=file_info.get("size"),
                                       sha256=file_info.get("sha256"),
                                       timestamp=file_info.get("mtime"),
                                       md5=file_info.get("md5"),
                                       )
                    finalpath: Path = file_info.get("filepath")
                    if finalpath.suffix.lower() in [".exe", ]:
                        finalpath.chmod(mode=(finalpath.lstat().st_mode | stat.S_IEXEC | stat.S_IRWXG | stat.S_IRWXO))
                self._dbh.commit()

    def fetch_updates(self):
        print("Fetching Updates via client")
        for product in self._client.iter_updated_products():
            self.conditionally_add_product_id_to_db(product=product)
            product_id = product.get("id")
            product_title = product.get("title")
            print("Update available for {0} {1}".format(product_id, product_title))
            self.update_product(product_id=product_id)

    def conditionally_add_product_id_to_db(self, product: dict):
        """
        A convenience function to keep database working
        :param product:
        :return:
        """
        product_id = product.get("id")
        if not self._dbh.is_product_id_in_db(product_id=product_id):
            try:
                details_product_data = self._client.get_product_data(product_id=product_id)
                url = get_url_from_product_data(details_product_data)
                product_type = extract_product_type_from_product_data(product_data=details_product_data)
            except HTTPError:
                url = None
                product_type = None

            self._dbh.add_new_product_to_db(product_id=product_id,
                                            url=url,
                                            slug=product.get("slug"),
                                            product_type=product_type,
                                            )

    def lazy_download(self,
                      product_count: int = 1,
                      force_update: bool = False,
                      update_specific: Optional[List[int]] = None):
        self._dbh.update_owned_products(product_ids=self._client.get_owned_products())
        remaining = 0
        owned_products_with_downloads = self._dbh.get_owned_products_with_downloads()
        for product in self._client.iter_owned_products():
            product_id = product.get("id")
            product_title = product.get("title")
            is_updated = product.get("updates")
            is_new = product.get("isNew")
            is_missing_downloads = len(self._dbh.get_latest_downloads_without_files(product_id=product_id)) or (
                    product_id not in owned_products_with_downloads)

            self.conditionally_add_product_id_to_db(product=product)

            if is_updated or is_new or is_missing_downloads or force_update or (product_id in update_specific):
                if (product_count > 0) or force_update or (product_id in update_specific):
                    print("Downloading {0} updated? {1} new? {2} is_missing_downloads? {3} forced {4}".format(
                        product_title,
                        is_updated,
                        is_new,
                        is_missing_downloads,
                        force_update))
                    self.update_product(product_id=product_id)
                    product_count -= 1
                    if not force_update:
                        print("{0} products remaining this run".format(product_count))
                else:
                    remaining += 1

        if remaining > 0:
            print("{0} products remaining overall".format(remaining))

    def update_product(self, product_id: int):
        print("updating product_id {0}".format(product_id))
        details = self._client.get_owned_game_details(product_id=product_id)

        self.update_owned_product_downloads(product_id=product_id,
                                            product_details=details,
                                            )
        self.get_downloads_for_product(product_id=product_id)
