""" module:: gogclient.db_handler
    :platform: All
    :synopsis: A basic interface to an sqlite3 db file to keep history on discounts.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from pathlib import Path
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Tuple, Sequence, List
import logging

from gogclient.client import GOGClient
from gogclient.utils import get_url_from_product_data, extract_product_id_from_api_v2_url, \
    extract_product_type_from_product_data, extract_product_slug_from_download_url, \
    extract_product_title_from_product_data, is_patch_download

LOGGER = logging.getLogger(__name__)

DB3PATH = Path("gog_db.db3")


# TODO: db_handler should not use client directly, move the get_details functionality into utils or into repo...


class DataBaseHandler:

    def __init__(self, db_path: Path = DB3PATH):
        self.db_path = db_path
        self._cursor = None
        self._conn = None
        if not self.db_path.exists():
            self.create_db(db_path=db_path)

    @staticmethod
    def create_db(db_path: Path) -> None:
        """
        Create the database
        :return: Nothing.
        """
        with sqlite3.connect(str(db_path)) as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE discount_history (
                    productId INTEGER NOT NULL,
                    baseAmount FLOAT NOT NULL,
                    finalAmount FLOAT NOT NULL,
                    discountPercentage FLOAT NOT NULL,
                    currency TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    UNIQUE (productId, timestamp)
                    )""")
            c.execute("""CREATE TABLE product_data (
                    productId INTEGER NOT NULL PRIMARY KEY,
                    url TEXT,
                    slug TEXT NOT NULL,
                    productType TEXT,
                    timestamp TIMESTAMP NOT NULL
                    )""")
            # NOTE: some products don't have url like 2109162628 Full Throttle Pre-Order Bonus
            c.execute("""CREATE TABLE t18n (
                    slug TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    t18n_text TEXT NOT NULL
                    )""")
            c.execute("""CREATE TABLE geo_blocked (
                    productId INTEGER NOT NULL PRIMARY KEY,
                    locale TEXT,
                    blocked BOOLEAN,
                    timestamp TIMESTAMP NOT NULL
                    )""")
            c.execute("""CREATE TABLE owned_products (
                     productId INTEGER NOT NULL PRIMARY KEY,
                     owned BOOLEAN,
                     timestamp TIMESTAMP NOT NULL
                     )""")

            # NOTE: a big downside of GOG is that it is obscured what product_id is behind a DLC,
            # because DLCs json is part of the main product json that is returned for any product in the game library

            c.execute("""CREATE TABLE downloads (
                    downloadId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    productId INTEGER NOT NULL,
                    language TEXT,
                    os TEXT,
                    url TEXT NOT NULL,
                    name TEXT NOT NULL,
                    version TEXT,
                    size TEXT NOT NULL,
                    dlSection TEXT,
                    dlType TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    UNIQUE(productId, url, version)
                    )""")
            c.execute("""CREATE TABLE dlc (
                    productId INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    parentId INTEGER,
                    UNIQUE(productId, parentId)
                    )""")
            c.execute("""CREATE TABLE pack (
                    productId INTEGER NOT NULL,
                    childId INTEGER NOT NULL,
                    UNIQUE(productId, childId)
                    )""")
            c.execute("""CREATE TABLE files (
                    downloadId INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    sha256 TEXT,
                    md5 TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    FOREIGN KEY (downloadId) REFERENCES downloads (downloadId) ON DELETE CASCADE
                    )""")
            c.execute("""CREATE TABLE storage_path (
                    productId INTEGER NOT NULL,
                    storagePath TEXT NOT NULL,
                    FOREIGN KEY (productId) REFERENCES product_data (productId) ON DELETE CASCADE
                    )""")
            c.execute("""CREATE TABLE broken_downloads (
                    downloadId INTEGER NOT NULL,
                    httpError TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    FOREIGN KEY (downloadId) REFERENCES downloads (downloadId) ON DELETE CASCADE
                    )""")
            c.execute("""CREATE TABLE serial_keys (
                    productId INTEGER NOT NULL,
                    serialKey TEXT NOT NULL,
                    FOREIGN KEY (productId) REFERENCES product_data (productId) ON DELETE CASCADE
                    )""")

    def __enter__(self):
        self._conn = sqlite3.connect(str(self.db_path), detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self._conn.__enter__()
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor = None
        self._conn.__exit__(exc_type, exc_val, exc_tb)
        self._conn = None

    def get_product_data_for_product_id(self, product_id: int):
        """
        Get the product_data table entry for a product_id
        :param product_id: The product id.
        :return: The contents of the sql call.
        """
        data = self._cursor.execute("""SELECT productId,url,slug,productType,timestamp
                                       FROM product_data WHERE productId=?""", (product_id,)).fetchone()
        return data

    def is_product_id_in_db(self, product_id: int) -> bool:
        """
        Check if there is an entry for this product id
        :param product_id: The product id.
        :return: True if the sql call returned data for this product_id,
                 False otherwise.
        """
        return self.get_product_data_for_product_id(product_id=product_id) is not None

    def add_new_product_to_db(self,
                              product_id: int,
                              url: str,
                              slug: str,
                              product_type: str,
                              timestamp: Optional[datetime] = None,
                              ) -> None:
        """
        Add an item to the database, let the logic and the different tables are handled in here.
        :param product_id: The gog product id.
        :param url: The url to the product.
        :param slug: The product title in a locale independent form.
        :param product_type: The product type, DLC, GAME, PACK, ...
        :param timestamp: The timestamp. If None now() is used.
        :return: Nothing
        """
        assert not self.is_product_id_in_db(product_id)
        timestamp = timestamp or datetime.now()
        LOGGER.debug("Adding new product_id {0} slug {1}".format(product_id, slug))
        try:
            self._cursor.execute(
                "INSERT INTO product_data (productid,url,slug,productType,timestamp) VALUES (?,?,?,?,?)",
                (product_id, url, slug, product_type, timestamp))
        except sqlite3.OperationalError as e:
            print("Error while adding product_id {0} {1}".format(product_id, e))

    def add_new_discount_for_product_to_db(self,
                                           product_id: int,
                                           base_amount: float,
                                           final_amount: float,
                                           discount: float,  # '-75%'
                                           currency: str,  # EUR, USD
                                           locale: str,  # de_DE, en_US
                                           timestamp: Optional[datetime] = None,
                                           ) -> None:
        """
        Add an item to the database, let the logic and the different tables are handled in here.
        :param product_id: The gog product id.
        :param base_amount: The regular price.
        :param final_amount: The current price.
        :param discount: The current discount.
        :param currency: The currency of the price information.
        :param timestamp: The timestamp. If None now() is used.
        :param locale: The locale.

        :return: Nothing
        """
        timestamp = timestamp or datetime.now()
        LOGGER.debug("Adding new discount for product_id {0} discount {1}".format(product_id, discount))
        try:
            self._cursor.execute("INSERT INTO discount_history (productId,baseAmount,finalAmount,discountPercentage,"
                                 "currency, locale, timestamp) VALUES (?,?,?,?,?,?,?)",
                                 (product_id, base_amount, final_amount, discount,
                                  currency, locale, timestamp))
        except sqlite3.OperationalError as e:
            print("Error while adding discount for product_id {0} {1}".format(product_id, e))

    def get_t18n_for_slug(self, slug: str, locale: str):
        """
        Get the translation for a slug in a specific locale
        :param slug: A not localised string.
        :param locale: The locale for the translation.
        :return: The contents of the sql call.
        """
        t18n = None
        data = self._cursor.execute("SELECT t18n_text FROM t18n WHERE slug=? AND locale=?", (slug, locale)).fetchone()
        if data:
            t18n = data[0]
        return t18n

    def get_title_for_product_id(self, product_id: int) -> str:
        data = [x[0] for x in self._cursor.execute(
            """
            SELECT t18n_text FROM t18n
            JOIN product_data ON t18n.slug=product_data.slug
            WHERE product_data.productId=?
            """, (product_id,)).fetchall()]
        ret = None
        if len(data) > 0:
            ret = data[0]
        return ret

    def get_url_for_product_id(self, product_id: int) -> Optional[str]:
        data = [x[0] for x in self._cursor.execute("SELECT url FROM product_data WHERE productId=?",
                                                   (product_id,)).fetchall()]
        ret = None
        if len(data) > 0:
            ret = data[0]
        return ret

    def is_slug_in_db(self, slug: str, locale: str) -> bool:
        """
        Check if there is a translation for a slug in a specific locale
        :param slug: A not localised string.
        :param locale: The locale for the translation.
        :return: True if the sql call returned data for this product_id,
                 False otherwise.
        """
        return self.get_t18n_for_slug(slug=slug, locale=locale) is not None

    def add_t18n_for_slug(self, slug, locale, t18n):
        """
        Add a translation for a slug. A slug is a unique not localised string,
        that is an identifier for a localised string.
        :param slug: A not localised string.
        :param locale: The locale for the translation.
        :param t18n: The translation of the slug.
        :return: Nothing.
        """
        assert not self.is_slug_in_db(slug=slug,
                                      locale=locale)
        LOGGER.debug("Adding Slug {0} Locale {1} t18n {2}".format(slug, locale, t18n))
        try:
            self._cursor.execute("INSERT INTO t18n (slug,locale,t18n_text) VALUES (?,?,?)",
                                 (slug, locale, t18n))
        except sqlite3.OperationalError as e:
            print("Error while adding t18n for slug {0} locale {1} {2}".format(slug, locale, e))

    def add_new_product_or_discount_from_catalog_dict(self,
                                                      product_id: int,
                                                      product_data: dict,
                                                      client: Optional[GOGClient] = None,
                                                      locale: str = "de_DE",
                                                      timestamp: Optional[datetime] = None,
                                                      force_update_of_product_data: bool = False,
                                                      ) -> None:
        """
        :param product_id: The product id.
        :param product_data: A catalog dict for a product
        :param client: The GOGClient. This is currently only necessary if the product is new to retrieve the url.
        :param locale: The locale to use for the entry
        :param timestamp: The timestamp. If None now() is used.
        :param force_update_of_product_data: A switch to force the update of product data, e.g. linking structures
        :return:
        """
        timestamp = timestamp or datetime.now()
        gog_client = client or GOGClient()
        title = product_data.get("title")
        price = product_data.get("price")
        base_money = price.get("baseMoney")
        final_money = price.get("finalMoney")
        base_amount = float(base_money.get("amount"))
        currency = base_money.get("currency")
        final_amount = float(final_money.get("amount"))
        discount_str = price.get("discount")
        discount = None
        if discount_str:
            discount = int(discount_str.lstrip("-").rstrip("%")) / 100
        else:
            LOGGER.error("No discount field for {0} {1}".format(product_id, title))

        if ((not self.is_product_id_in_db(product_id))
                or (force_update_of_product_data is True)):
            self.add_new_product_from_catalog_data(product_id=product_id,
                                                   catalog_product_data=product_data,
                                                   client=gog_client,
                                                   timestamp=timestamp,
                                                   locale=locale,
                                                   )

        if discount:
            self.add_new_discount_for_product_to_db(product_id=product_id,
                                                    base_amount=base_amount,
                                                    final_amount=final_amount,
                                                    discount=discount,
                                                    currency=currency,
                                                    locale=locale,
                                                    timestamp=timestamp)

    def add_new_product_from_catalog_data(self,
                                          product_id: int,
                                          catalog_product_data: dict,
                                          details_product_data: Optional[dict] = None,  # can be supplied
                                          client: Optional[GOGClient] = None,
                                          timestamp: Optional[datetime] = None,
                                          locale: str = "de_DE",
                                          ):
        # problem, a product that has a product card, e.g. is found via catalog, has details,
        # but not necessarily the other way around!

        timestamp = timestamp or datetime.now()
        gog_client = client or GOGClient()
        if details_product_data is None:
            details_product_data = gog_client.get_product_data(product_id=product_id)
        url = get_url_from_product_data(details_product_data)
        product_type = extract_product_type_from_product_data(product_data=details_product_data)
        title = extract_product_title_from_product_data(product_data=details_product_data)

        slug = catalog_product_data.get("slug")
        print("Adding new product from catalog_data {0}".format(slug))
        if product_type is None:
            LOGGER.error("Problem with product_type in product_id {0}".format(product_id))

        # cross-linking stage if DLC is found, link it to the parent game
        requires_games_links = details_product_data.get("_links").get("requiresGames")  # type DLC
        if requires_games_links is not None:
            requires_games = [extract_product_id_from_api_v2_url(x.get("href")) for x in
                              requires_games_links]
            for parent_id in requires_games:
                self.add_dlc(product_id=product_id,
                             parent_id=parent_id)

        # cross-linking stage if GAME with DLCs is found, link the dlcs to the parent game
        is_required_by_games_links = details_product_data.get("_links").get("isRequiredByGames")  # type GAME
        if is_required_by_games_links:
            is_required_by_games = [extract_product_id_from_api_v2_url(x.get("href")) for x in
                                    is_required_by_games_links]
            for child_id in is_required_by_games:
                self.add_dlc(product_id=child_id,
                             parent_id=product_id)

        # cross-linking stage if a PACK or sometimes a GAME is found that includes other things, link it in packs
        included_product_ids_links = details_product_data.get("_links").get("includesGames")  # type PACK
        if included_product_ids_links:
            included_product_ids = [extract_product_id_from_api_v2_url(x.get("href")) for x in
                                    included_product_ids_links]
            self.add_pack(product_id=product_id,
                          included_product_ids=included_product_ids)

        if not self.is_slug_in_db(slug=slug, locale=locale):
            self.add_t18n_for_slug(slug=slug, t18n=title, locale=locale)

        if not self.is_product_id_in_db(product_id):
            self.add_new_product_to_db(product_id=product_id,
                                       url=url,
                                       slug=slug,
                                       product_type=product_type,
                                       timestamp=timestamp)
        elif self.get_product_type(product_id=product_id) is None:
            self.update_product_type(product_id=product_id,
                                     product_type=product_type)

    def get_current_discounts(self,
                              since: datetime = (datetime.now() - timedelta(days=1)),
                              currency="EUR",
                              locale="de_DE") -> dict:
        """
        Get the most recent discounts.
        :param since: A date, defaults to since 1 Day
        :param currency: The currency.
        :param locale: The locale # UNUSED!
        :return: The discounts from database matching this query.
        """
        try:
            r = self._cursor.execute(
                """
                SELECT productId, baseAmount, finalAmount, discountPercentage
                FROM discount_history
                WHERE timestamp>? AND currency=?
                ORDER BY discountPercentage DESC
                """,
                (since, currency)).fetchall()
        except sqlite3.OperationalError as e:
            print(
                "Error while selecting discounts since {0} for currency {1} locale {2} {3}".format(since, currency,
                                                                                                   locale, e))
            r = []
        ret = {}
        print("current raw {0}".format(len(r)))
        for item in r:
            product_id, base_amount, final_amount, discount = item
            if product_id not in ret:
                ret.update({product_id: {"url": self.get_url_for_product_id(product_id=product_id),
                                         "title": self.get_title_for_product_id(product_id=product_id),
                                         "base_amount": base_amount,
                                         "final_amount": final_amount,
                                         "discount": discount,
                                         "currency": currency}})
        return ret

    def get_discount_history_for_product(self,
                                         product_id: int) -> list:
        """

        :param product_id: The product id.
        :return:
        """
        try:
            res = self._cursor.execute(
                """SELECT discountPercentage, timestamp
                FROM discount_history WHERE productId=? ORDER BY timestamp DESC""",
                (product_id,)).fetchall()
        except sqlite3.OperationalError as e:
            print("Error while selecting discounts for product_id {0} {1}".format(product_id, e))
            res = None

        return res

    def get_max_discount_and_date_for_product(self, product_id: int) -> Optional[Tuple[float, datetime]]:
        """
        Get the max discount for a specific product and the first (oldest) date when it occurred.
        This gives statistical information about how good a discount is.
        :param product_id: The product id.
        :return: A tuple of the discount value and the datetime of the first occurrence.
        """
        discount_history = self.get_discount_history_for_product(product_id=product_id)
        ret = None
        discounts = None
        if discount_history:
            discounts = [discount[0] for discount in discount_history]
        if discounts:
            max_discount = max(discounts)
            max_discount_occurrences = [x for x in discount_history if x[0] == max_discount]
            ret = (max_discount, max_discount_occurrences[-1][1])
        return ret

    def add_geo_blocked_entry(self,
                              product_id: int,
                              is_blocked: Optional[bool],
                              locale: Optional[str],
                              timestamp: Optional[datetime] = None,
                              ) -> None:
        """

        :param product_id: The product_id
        :param is_blocked: Actually Tristate, None means to be checked with clean connection. For some reason GOG finds
                           out which locale it currently is and gog_loc does no longer work.
        :param locale: The locale.
        :param timestamp: The Timestamp.
        :return:
        """
        timestamp = timestamp or datetime.now()
        LOGGER.debug("Adding geo_blocked entry product_id {0} is_blocked {1}".format(product_id, is_blocked))
        try:
            self._cursor.execute("INSERT INTO geo_blocked (productId, blocked, locale, timestamp) VALUES (?,?,?,?)",
                                 (product_id, is_blocked, locale, timestamp))
        except sqlite3.OperationalError as e:
            print("Error while adding geo_blocked entry for product_id {0} {1}".format(product_id, e))

    def get_geo_blocked_info(self,
                             product_id: int
                             ):
        geo_blocked = self._cursor.execute(
            "SELECT DISTINCT blocked,timestamp FROM geo_blocked WHERE productId=?",
            (product_id,)).fetchone()
        return geo_blocked

    def is_product_geo_blocked_for_locale(self,
                                          product_id: int,
                                          locale: str = "DE_EUR_de-DE"):
        geo_blocked = self._cursor.execute(
            "SELECT DISTINCT blocked,timestamp FROM geo_blocked WHERE productId=? AND locale=? ORDER BY timestamp DESC",
            (product_id, locale)).fetchone()
        is_blocked = False
        if geo_blocked is not None and bool(geo_blocked[0]) is True:
            is_blocked = True
        return is_blocked

    def get_owned_products(self) -> set:
        return set(x[0] for x in self._cursor.execute("SELECT DISTINCT productId FROM owned_products WHERE owned=?",
                                                      (True,)).fetchall())

    def update_owned_products(self,
                              product_ids: Sequence[int]) -> None:
        product_ids_to_add = set(product_ids) - self.get_owned_products()
        for product_id in product_ids_to_add:
            self.set_owned(product_id=product_id)
        self.update_owned_packs_by_component_assembly()
        self.update_owned_by_owned_packs()

    def is_owned(self,
                 product_id: int):
        return self._cursor.execute("SELECT DISTINCT owned FROM owned_products WHERE productId=?",
                                    (product_id,)).fetchone()

    def set_owned(self,
                  product_id: int,
                  owned: bool = True,
                  timestamp: Optional[datetime] = None,
                  ) -> None:
        timestamp = timestamp or datetime.now()
        # # print(product_id, owned, timestamp)
        # if self.is_owned(product_id=product_id):
        #     self._cursor.execute("UPDATE owned_products SET owned=? , timestamp=? WHERE productId=?",
        #                          (owned, timestamp, product_id))
        # else:
        self._cursor.execute("INSERT INTO owned_products (productId, owned, timestamp) VALUES (?,?,?)",
                             (product_id, owned, timestamp))

    def is_download_in_db(self,
                          product_id: int,
                          url: str,
                          name: str,
                          version: Optional[str] = None,
                          ) -> bool:
        """
        Check if a specific download is already in the database.

        :param product_id: The gog product id.
        :param url: The url to the download.
        :param name: The name of the download.
        :param version: The download's version.
        :return: True if already inside.
        """
        if version is None:
            data = self._cursor.execute("SELECT * FROM downloads WHERE productId=? AND url=?",
                                        (product_id, url)).fetchone()
        elif is_patch_download(url=url):
            # patch with version
            #
            # The problem with patches is that they change their download url over time,
            # they move one down the list, incrementing the number instead of giving each patch a new number
            # GOG is so incompetent!
            data = self._cursor.execute("SELECT * FROM downloads WHERE productId=? AND name=? AND version=?",
                                        (product_id, name, version)).fetchone()
        else:
            # regular download with version
            data = self._cursor.execute("SELECT * FROM downloads WHERE productId=? AND url=? AND version=?",
                                        (product_id, url, version)).fetchone()
        return data is not None

    def add_download(self,
                     product_id: int,
                     url: str,
                     name: str,
                     size: str,
                     language: Optional[str] = None,
                     os: Optional[str] = None,
                     version: Optional[str] = None,
                     dl_section: Optional[str] = None,
                     dl_type: Optional[str] = None,
                     timestamp: Optional[datetime] = None,
                     ):
        """
        Add a download to the database, let the logic and the different tables are handled in here.

        :param product_id: The gog product id.
        :param language: The download language.
        :param os: The download operating system.
        :param url: The url to the product.
        :param name: The download's (file)name.
        :param version: The download's version.
        :param dl_section: The sort option DLC / GAME etc.
        :param dl_type: The sort type game-add-on / manual etc.
        :param size: The size of the download.
        :param timestamp: The timestamp. If None now() is used.
        :return: Nothing.
        """

        timestamp = timestamp or datetime.now()
        if not self.is_download_in_db(product_id=product_id,
                                      url=url,
                                      name=name,
                                      version=version):
            LOGGER.debug("Adding new download for product_id {0} {1} {2}".format(product_id, name, version))
            try:
                self._cursor.execute(
                    """INSERT INTO downloads (productId,language,os,url,name,version,size,dlSection,dlType,timestamp)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""", (product_id, language, os, url, name, version, size, dl_section,
                                                      dl_type, timestamp))
            except sqlite3.OperationalError as e:
                LOGGER.error(
                    "Error while adding download product_id {0} {1} {2} {3}".format(product_id, name, version, e))

    def get_latest_downloads_without_files(self,
                                           product_id: int,
                                           ) -> list:

        files = set(x[0] for x in self._cursor.execute("""SELECT DISTINCT downloadId FROM files""").fetchall())
        broken_downloads = self.get_broken_downloads()

        result = [(download_id, url, name, size) for download_id, url, name, size in self._cursor.execute(
            """SELECT DISTINCT downloadId,url,name,size FROM downloads WHERE productId=? ORDER BY timestamp DESC""",
            (product_id,)).fetchall() if download_id not in files and download_id not in broken_downloads]
        return result

    def get_owned_products_with_missing_downloads(self) -> set:
        """
        DEPRECATED FUNCTION
        :return:
        """
        products_with_downloads = set(x[0] for x in self._cursor.execute(
            """SELECT DISTINCT productId FROM downloads""").fetchall())

        owned = set(x for x in self.get_owned_products())
        packs = set(self.get_packs().keys())
        # NOTE: problem case tombraider 1,2,3 are product_ids without catalog page and subsequently no data entry
        #        have to filter owned products instead of going through owned entries!
        #        WORKAROUND: find all PACKS that have no games, e.g. are not parent_id in DLC structures
        owned_dlcs = self.get_owned_dlcs()

        owned_products_with_missing_downloads = owned - owned_dlcs - products_with_downloads - packs
        return owned_products_with_missing_downloads

    def get_owned_products_with_downloads(self) -> set:
        products_with_downloads = set(x[0] for x in self._cursor.execute(
            """SELECT DISTINCT productId FROM downloads""").fetchall())
        return products_with_downloads

    def add_dlc(self,
                product_id: int,
                parent_id: int,
                ):
        LOGGER.debug("Adding DLC for product_id {0} parent_id {1}".format(product_id, parent_id))
        self.update_product_type(product_id=product_id,
                                 product_type="DLC")
        if not self.is_dlc(product_id=product_id):
            try:
                self._cursor.execute("INSERT INTO dlc (productId,parentId) VALUES (?,?)", (product_id, parent_id))
            except sqlite3.OperationalError as e:
                LOGGER.error(
                    "Adding DLC for product_id {0} parent_id {1} with Error {2}".format(product_id, parent_id, e))

    def get_broken_downloads(self) -> set:
        return set(
            x[0] for x in self._cursor.execute("""SELECT DISTINCT downloadId FROM broken_downloads""").fetchall())

    def add_broken_download(self,
                            download_id: int,
                            http_error: int,
                            timestamp: Optional[datetime] = None,
                            ) -> None:
        timestamp = timestamp or datetime.now()
        self._cursor.execute("INSERT INTO broken_downloads (downloadId,httpError,timestamp) VALUES (?,?,?)",
                             (download_id, http_error, timestamp))

    def get_base_product_for_dlc(self, product_id: int) -> Optional[int]:
        result = self._cursor.execute("""SELECT DISTINCT parentId FROM dlc WHERE productId=?""",
                                      (product_id,)).fetchone()
        base_product_id = None
        if result is not None:
            base_product_id = result[0]
        return base_product_id

    def is_dlc(self,
               product_id: int):
        return self.get_base_product_for_dlc(product_id=product_id)

    def add_pack(self,
                 product_id: int,
                 included_product_ids: Sequence[int, ],
                 ):
        LOGGER.debug("Adding PACK for product_id {0} includes {1}".format(product_id, included_product_ids))
        self.update_product_type(product_id=product_id,
                                 product_type="PACK")
        if not self.is_pack(product_id=product_id):
            for child_id in included_product_ids:
                try:
                    self._cursor.execute("INSERT INTO pack (productId,childId) VALUES (?,?)", (product_id, child_id))
                except sqlite3.OperationalError as e:
                    LOGGER.error(
                        "Adding DLC for product_id {0} child_id {1} with Error {2}".format(product_id, child_id, e))

    def is_pack(self,
                product_id: int):
        return self._cursor.execute("""SELECT DISTINCT productId FROM pack WHERE productId=?""",
                                    (product_id,)).fetchone()

    def get_packs(self) -> dict:
        packs = {}
        for product_id, child_id in self._cursor.execute("""SELECT DISTINCT productId, childId FROM pack""").fetchall():
            if product_id not in packs:
                packs.update({product_id: []})
            packs.get(product_id).append(child_id)
        return packs

    def get_product_parent(self, product_id: int) -> Optional[int]:
        ret = None
        result = self._cursor.execute("""SELECT DISTINCT productId FROM pack WHERE childId=?""",
                                      (product_id,)).fetchone()
        if result is not None:
            ret = result[0]
        return ret

    def get_product_siblings(self, product_id: int) -> List[int]:
        """
        Return the sibling products in a pack.
        :param product_id: The product ID
        :return: A list of siblings if there are any.
        """
        siblings = [x[0] for x in self._cursor.execute(
            """SELECT childId FROM pack
               WHERE productId = ( SELECT productId FROM pack WHERE childId=?)
               AND NOT childId=?""",
            (product_id, product_id,)).fetchall()]
        return siblings

    def update_product_type(self,
                            product_id: int,
                            product_type: str = "GAME",
                            ):
        try:
            self._cursor.execute("UPDATE product_data SET productType=? WHERE productId=?", (product_type, product_id))
        except sqlite3.OperationalError as e:
            LOGGER.error(
                "Update product_type for product_id {0} to {1} with Error {2}".format(product_id, product_type, e))

    def get_product_type(self,
                         product_id: int,
                         ):
        resp = self._cursor.execute("""SELECT DISTINCT productType FROM product_data WHERE productId=?""",
                                    (product_id,)).fetchone()
        product_type = None
        if resp is not None:
            product_type = resp[0]
        return product_type

    def update_owned_packs_by_component_assembly(self):
        owned = set(x[0] for x in self._cursor.execute("SELECT DISTINCT productId FROM owned_products WHERE owned=?",
                                                       (True,)).fetchall())
        for pack, components in self.get_packs().items():
            not_owned_components = set(components) - owned
            LOGGER.debug("Pack {0} - Non owned components {1}".format(pack, not_owned_components))
            if not self.is_owned(product_id=pack) \
                    and (len(not_owned_components) == 0):
                LOGGER.info("Adding pack {0} to owned because all contents are owned".format(pack))
                self.set_owned(product_id=pack)

    def update_owned_by_owned_packs(self):
        for pack, components in self.get_packs().items():
            if self.is_owned(product_id=pack):
                for component in components:
                    if not self.is_owned(product_id=component):
                        LOGGER.info("Adding component {0} to owned because pack {1} is owned".format(component, pack))
                        self.set_owned(product_id=component)

    def get_owned_products_with_dlcs(self):
        owned_with_dlcs = set(x[0] for x in
                              self._cursor.execute("""SELECT DISTINCT owned_products.productId FROM owned_products
                                                      JOIN dlc ON owned_products.productId=dlc.parentId
                                                      WHERE owned_products.owned=? and NOT dlc.productId is NULL""",
                                                   (True,)).fetchall())
        return owned_with_dlcs

    def get_dlcs_of_owned_products_without_product_data(self):
        # get productid of dlcs where the base game is owned
        dlcs_of_owned_products = set(x[0] for x in
                                     self._cursor.execute("""SELECT DISTINCT dlc.productId FROM dlc
                                                      JOIN owned_products ON dlc.parentId=owned_products.productId
                                                      WHERE owned_products.owned=?""",
                                                          (True,)).fetchall())

        dlcs_of_owned_products_wo_product_data = {x for x in dlcs_of_owned_products if
                                                  not self.is_product_id_in_db(product_id=x)}
        return dlcs_of_owned_products_wo_product_data

    def get_owned_dlcs(self):
        owned_dlcs = set(x[0] for x in
                         self._cursor.execute("""
                         SELECT DISTINCT dlc.productId FROM dlc
                         JOIN owned_products ON dlc.parentId=owned_products.productId
                         WHERE owned_products.owned=?""", (True,)).fetchall())
        return owned_dlcs

    def reverse_find_product_id_by_url_of_dlc(self,
                                              url: str) -> Optional[int]:
        """
        The problem: For whatever reason, GOG does not list dlc downloads by their product id but instead as
                     products in the DLC entries of the parent product. Therefore, there is no connection from the
                     product_id of the DLC to the download, e.g. you can't find out what purchased product_id leads
                     to which download.
        The Solution: Reverse find the product_id by checking the TITLE of the DLC and the download_url path which
                      contains the slug of the DLC.
                      This function makes active use of the fact that GOG uses underscores in urls which also represents
                      a wildcard type in sqlite3 LIKE operation.
        :param url: The url of the download.
        :return: The product_id for the dlc
        """
        slug = extract_product_slug_from_download_url(url)
        result = self._cursor.execute("""SELECT DISTINCT productId FROM product_data WHERE slug LIKE ?""",
                                      (slug,)).fetchone()
        product_id = None
        if result is not None:
            product_id = result[0]
        return product_id

    def reverse_assign_product_ids_for_dlc_downloads(self):
        """
        The problem: For whatever reason, GOG does not list dlc downloads by their product id but instead as
                     products in the DLC entries of the parent product. Therefore, there is no connection from the
                     product_id of the DLC to the download, e.g. you can't find out what purchased product_id leads
                     to which download.
        The Solution: Reverse find the product_id by checking the TITLE of the DLC and the download_url path which
                      contains the slug of the DLC.
        :return: Nothing.
        """
        for download_id, old_product_id, url, in self._cursor.execute(
                """SELECT DISTINCT downloadId, productId, url FROM downloads WHERE name=?""", ("DLC",)).fetchall():
            product_id = self.reverse_find_product_id_by_url_of_dlc(url=url)
            if product_id is None:
                LOGGER.error("Could not determine product_id from download {0} {1}".format(old_product_id, url))
            if (product_id != old_product_id) and (product_id is not None):
                LOGGER.info("Updating product_id {0} -> {1}, {2}".format(old_product_id, product_id, url))
                self._cursor.execute("UPDATE downloads SET productId=? WHERE downloadId=?",
                                     (product_id, download_id))

    def get_products_with_discount_history(self) -> set:
        """
        Get a set of product_ids with discount history
        :return: A set of product_ids
        """
        products_with_discount_data = set(x[0] for x in self._cursor.execute(
            """SELECT DISTINCT productId FROM discount_history""").fetchall())
        return products_with_discount_data

    def cleanup_discounts(self):
        """
        Discounts usually last a while and then turn up at another date, so don't keep the entries
        in between to save db space.
        :return: Nothing.
        """
        # iter over all known products with available discounts
        products_with_discount_history = self.get_products_with_discount_history()

        for product_id in products_with_discount_history:
            previous_discount_percentage = 1.0
            timestamps_with_same_discount = list()
            previous_timestamp = datetime.now()
            history = self.get_discount_history_for_product(product_id=product_id)
            for discount_percentage, timestamp in history:
                # check if we have the same discount as before
                if discount_percentage == previous_discount_percentage:
                    # check if we have less than 2 days between the record
                    if (previous_timestamp - timestamp) < timedelta(days=2):  # DESC
                        # append this timestamp
                        timestamps_with_same_discount.append(timestamp)
                    else:
                        if len(timestamps_with_same_discount) > 3:
                            LOGGER.info("Cleanup Discounts for ProdudctID {0} removing {1} entries with same discount "
                                        "in range {2} - {3}".format(product_id,
                                                                    len(timestamps_with_same_discount),
                                                                    timestamps_with_same_discount[1],
                                                                    timestamps_with_same_discount[-2]))
                            self._cursor.execute(
                                "DELETE FROM discount_history WHERE productId=? AND timestamp BETWEEN ? AND ?",
                                (product_id, timestamps_with_same_discount[-1], timestamps_with_same_discount[0]))
                        timestamps_with_same_discount.clear()

                # update trailing variables
                previous_timestamp = timestamp
                previous_discount_percentage = discount_percentage

    def compress(self):
        self._cursor.execute("VACUUM")  # COMPRESS and free space

    def get_storage_path_for_product_id(self,
                                        product_id: int) -> Optional[Path]:
        result = self._cursor.execute(
            """SELECT DISTINCT storagePath FROM storage_path WHERE productId=?""", (product_id,)).fetchone()
        storage_path = None
        if result is not None:
            storage_path = Path(result[0])
        else:
            LOGGER.error("No storage_path for product_id {0}".format(product_id))
        return storage_path

    def set_storage_path_for_product_id(self,
                                        product_id: int,
                                        storage_path: Path,
                                        ):
        if self.get_storage_path_for_product_id(product_id=product_id) is None:
            self._cursor.execute(
                "INSERT INTO storage_path (productId,storagePath) VALUES (?,?)",
                (product_id, str(storage_path)))
        else:
            self._cursor.execute("UPDATE storage_path SET storagePath=? WHERE productId=?",
                                 (str(storage_path), product_id))

    def add_file(self,
                 download_id: int,
                 filename: Path,
                 size: int,
                 sha256: str,
                 md5: str,
                 timestamp: Optional[datetime] = None,
                 ):
        timestamp = timestamp or datetime.now()

        try:
            self._cursor.execute(
                "INSERT INTO files (downloadId,filename,size,sha256,md5,timestamp) VALUES (?,?,?,?,?,?)",
                (download_id, str(filename), size, sha256, md5, timestamp))
        except sqlite3.OperationalError as e:
            print("Error while adding file for download_id {0} {1}".format(download_id, e))

    def get_download_id_for_url(self, url: str) -> Optional[int]:
        result = self._cursor.execute(
            """SELECT DISTINCT downloadId FROM downloads WHERE url=? ORDER BY timestamp DESC""", (url,)).fetchone()
        download_id = None
        if result is not None:
            download_id = result[0]
        else:
            LOGGER.error("No download_id for url {0}".format(url))
        return download_id

    def get_products_without_type(self):
        result = set(x[0] for x in self._cursor.execute(
            """SELECT DISTINCT productId, productType FROM product_data""").fetchall() if x[1] is None)
        return result

    def dev_helper_make_storage_path_relative_to_base(self):
        for product_id, storage_path in self._cursor.execute("""
        SELECT DISTINCT productId, storagePath FROM storage_path""").fetchall():
            if Path(storage_path).is_absolute():
                rel_storage_path = storage_path.rsplit("/", maxsplit=1)[-1]
                self._cursor.execute("UPDATE storage_path SET storagePath=? WHERE productId=?",
                                     (str(rel_storage_path), product_id))

    def commit(self):
        if self._conn is not None:
            self._conn.commit()
        else:
            LOGGER.error("Commit without Connection - not inside a with statement ?!")

    def get_serial_key(self, product_id: int) -> Optional[str]:
        result = self._cursor.execute("""SELECT serialKey from serial_keys WHERE productId=?""",
                                      (product_id,)).fetchone()
        if result is not None:
            result = result[0]
        return result

    def add_serial_key(self, product_id: int, serial_key: str):
        if self.get_serial_key(product_id=product_id) is None:
            self._cursor.execute("""INSERT INTO serial_keys (productId, serialKey) VALUES (?,?)""",
                                 (product_id, serial_key))

    def is_extra_a_duplicate(self,
                             product_id: int,
                             extra_name: str,
                             ) -> bool:
        ret = False
        siblings = self.get_product_siblings(product_id=product_id)
        if siblings is not None:
            ret = any(self._cursor.execute(
                """SELECT DISTINCT downloadId FROM downloads WHERE productId=? AND name=?""",
                (sibling, extra_name)).fetchone() for sibling in siblings)

        return ret
