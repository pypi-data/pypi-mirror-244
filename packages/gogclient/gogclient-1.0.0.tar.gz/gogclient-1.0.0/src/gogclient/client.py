""" module:: gogclient.client
    :platform: All
    :synopsis: A client to access your GOG.com account.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import datetime
import logging
import os
import re
import tempfile
import time
from hashlib import sha256, md5
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Tuple, Optional, Union, Generator, Any
from urllib.parse import urljoin
from zipfile import ZipFile

import requests
from requests import HTTPError, Response
from tqdm import tqdm

from gogclient.utils import get_credentials, \
    get_country_code_from_locale, extract_login_url_from_gog_base_url, extract_client_id_from_login_url, parse_form, \
    user_input_second_step_code, save_debug_data, extract_code_from_return_login_success_url, \
    get_catalog_from_get_products_url, ReCaptchaException, extract_filename_from_download_url, iter_catalog, \
    parse_file_info_xml, check_local_file, get_fileinfo_url, check_chunk_md5


class GOGClient:

    def __init__(self,
                 gog_base_url: str = r"https://www.gog.com",
                 login_check_url: str = r"https://login.gog.com/login_check",
                 redirect_uri: str = r"https://www.gog.com/on_login_success",
                 user_agent: str = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
                 gog_lc: Optional[str] = None,
                 log_base_path: Optional[Path] = None,
                 ):
        self._user_agent = user_agent
        self._gog_base_url = gog_base_url
        self._login_check_url = login_check_url
        self._redirect_uri = redirect_uri
        self._gog_lc = gog_lc,

        if log_base_path is None:
            log_base_path = Path(tempfile.gettempdir())
        logging.basicConfig(
            handlers=[
                RotatingFileHandler(filename=log_base_path / "gogclient.log", maxBytes=5 * 1024 * 1024, backupCount=2)],
            format="%(asctime)s %(name)s %(levelname)s: %(message)s",
            level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)

        self._session = requests.session()
        self._credentials = get_credentials()

    @property
    def session(self):
        return self._session

    def _get(self,
             url: str,
             headers: Optional[Any] = None,
             cookies: Optional[Any] = None,
             stream: bool = False,
             timeout: int = 60,
             retry: int = 3) -> Response:
        if stream is False and isinstance(headers, dict):
            assert "Range" not in headers
        r = Response()
        for i in range(retry):
            r = self._session.get(url=url,
                                  headers=headers,
                                  cookies=cookies,
                                  stream=stream,
                                  timeout=timeout)
            if r.status_code == 429:
                self._logger.debug("GOT 429 on GET {0} - sleeping {1}".format(r.url, r.headers["Retry-After"]))
                time.sleep(int(r.headers.get("Retry-After")))
            else:
                break
        return r

    def login(self):
        username = self._credentials.get("login[username]")
        password = self._credentials.get("login[password]")
        headers = {"user-agent": self._user_agent,
                   "Referer": "https://www.gog.com/",
                   }
        self._logger.debug("HTTP GET base url and retrieve login_url and client_id")
        r = self._get(url=self._gog_base_url)
        r.raise_for_status()
        cookies = r.cookies
        login_url = extract_login_url_from_gog_base_url(r.text)
        assert login_url
        client_id = extract_client_id_from_login_url(login_url)
        assert client_id
        if self._gog_lc is not None:
            self._logger.debug("Mangle the gog_lc in the login url, just in case")
            location_mangled_login_url = re.sub(pattern="gog_lc=[^&']*",
                                                repl="gog_lc={0}".format(self._gog_lc),
                                                string=login_url)
            self._logger.debug("HTTP GET login url and retrieve the login form fields")
            r = self._get(url=location_mangled_login_url, cookies=cookies, headers=headers)
        else:
            r = self._get(url=login_url, cookies=cookies, headers=headers)
        r.raise_for_status()
        cookies = r.cookies

        try:
            form_fields = {field: value for field, value in parse_form(r.text).items() if field.startswith("login")}
        except ReCaptchaException:
            self._logger.error("Found Recaptcha at first login stage - Cannot Handle it.")
            raise GogClientException("Cannot login due to Recaptcha on first login stage")
        else:
            form_fields.update({"login[username]": username,
                                "login[password]": password,
                                })
            std_params = {"brand": "gog",
                          "gog_lc": self._gog_lc,
                          "redirect_uri": self._redirect_uri,
                          "client_id": client_id,
                          "layout": "default",
                          "response_type": "code",
                          }

            self._logger.debug("HTTP POST form data to login check url")

            r = self._session.post(url=self._login_check_url, data=form_fields, cookies=cookies, params=std_params)

            if r.url.startswith("https://login.gog.com/login/two_step"):
                try:
                    # 2fa step auth via email
                    form_2fa_fields = parse_form(r.text)
                    second_step_authentication_token = form_2fa_fields.get("second_step_authentication[_token]")
                    if second_step_authentication_token:
                        self._logger.debug("second step authentication requested by server Token: {0}".format(
                            second_step_authentication_token))
                        second_step_url = r.url
                        form_2fa_fields.update(user_input_second_step_code())
                        self._logger.debug("Fields after user input 2fa {0}".format(form_2fa_fields))
                        r = self._session.post(second_step_url, data=form_2fa_fields, params=std_params)
                        r.raise_for_status()
                except HTTPError:
                    save_debug_data(r, "after_2fa")

            if not r.url.startswith("https://www.gog.com/on_login_success?code="):
                save_debug_data(r, "before_login_success_assert")
            assert r.url.startswith("https://www.gog.com/on_login_success?code=")

            self._logger.debug("Login successful - redirected to on_login_success with code")
            if self._gog_lc is not None:
                cookies.get_dict(domain=".gog.com").update({"gog_lc": self._gog_lc})
            code = extract_code_from_return_login_success_url(r.url)
            self._logger.debug("Extracted Code {0}".format(code))
            assert self.is_logged_in()

    def is_logged_in(self) -> bool:
        """
        Poll a json endpoint if logged in.
        json {"isLoggedIn":false,"cacheExpires":<EPOCH TIME>}
        :return True if logged in.
        :rtype bool
        """
        url = r"https://menu.gog.com/v1/account/basic"
        r = self._get(url=url)
        r.raise_for_status()
        return r.json().get("isLoggedIn")

    def logout(self):
        url = r"https://www.gog.com/logout"
        r = self._get(url=url)
        r.raise_for_status()

    def __enter__(self):
        if not self.is_logged_in():
            self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        return

    def get_catalog_products(self, currency: str = "EUR", locale: Optional[str] = None,
                             limit: Optional[int] = 48, order: str = "desc:discount", discounted: str = "eq:true",
                             product_type: Optional[list] = None, query_string: Optional[str] = None,
                             price: Optional[Tuple[Union[float, int], Union[float, int]]] = None,
                             hide_owned: bool = False):
        """
        Get filtered products by json call to catalog.gog.com
        This is far more sufficient than going over the browser pages.
        Reverse Engineering this database language, some commands are obvious,
        if <operation>:<values> is present, operation can be
        a sort option "desc"(descending), maybe "asc" as well, known from databases.
        "desc:trending" is descending popularity, e.g. the best sales first, how convenient.
        "desc:discount" also works great!
        "eq:true" is obviously an equality operation, a string equality!
        :NOTE: There is either a plausibility check in between locale, country, currency
        or some unhandled exception in GOG backend. It does not return anything in certain cases.
        GOG does filter products on catalog based on given countryCode parameter! This function
        takes that value from given locale. There is apparently a countryCode "REST".
        :param price: The price range.
        :param currency: The currency string.
        :param locale: The locale string.
        :param limit: The limit per page, meant for the browser pages.
        :param order: The order of display.
        :param discounted: Display only discounted.
        :param product_type: The product type.
        :param query_string: The optional query string.
        :param hide_owned: Hide already owned products. To be tested once login works Param "hideOwned=true"
        :return: A dictionary.
        """
        if product_type is None:
            product_type = ["game", "pack", "dlc"]
        url = r"https://catalog.gog.com/v1/catalog"
        if query_string:
            params = {"query": "like:{0}".format(query_string),
                      "order": "desc:score",
                      }
        else:
            locale = locale or "de_DE"
            country_code = get_country_code_from_locale(locale)
            params = {"currencyCode": currency,
                      "locale": locale,
                      "countryCode": country_code,
                      "order": order,
                      "discounted": discounted,
                      "productType": "in:{0}".format(",".join(product_type)),
                      "page": 1,
                      }
            if price:
                params.update({price: "between:{0}".format(",".join(str(x) for x in price))})
            if limit:
                params.update({"limit": limit, })
            if hide_owned:
                assert self.is_logged_in()
                params.update({"hideOwned": "true", })

        return get_catalog_from_get_products_url(session=self._session,
                                                 url=url,
                                                 params=params)

    def get_product_data(self, product_id) -> dict:
        """
        Get the product specific json from api.gog.com
        :param product_id: The product id.
        :return: A dictionary with the json data.
        """
        url = r"https://api.gog.com/v2/games/{0}".format(product_id)
        r = self._get(url)
        r.raise_for_status()
        return r.json()

    def get_owned_products(self) -> list:
        """
        This is a service from GOG where you get alist of purchased items.
        It does not match with what your account actually shows you in
        account / getFilteredProducts.
        Therefore, it is dangerous to make lists / sets from.
        It is discouraged to use this.
        -> use iter_owned_products() instead
        :return: A list of owned product_ids, it does not include all products from purchased PACKs or DLCs or whatever!
        """
        url = r"https://www.gog.com/user/data/games"
        r = self._get(url)
        r.raise_for_status()
        return r.json().get("owned")

    def iter_updated_products(self):
        url = "https://www.gog.com/account/getFilteredProducts"
        params = {"isUpdated": 1,
                  "mediaType": 1,
                  "page": 1,
                  "sortBy": "date_purchased",
                  "totalPages": 1,
                  }
        return iter_catalog(session=self._session,
                            url=url,
                            params=params)

    def iter_owned_products(self) -> Generator[dict, None, None]:
        url = "https://www.gog.com/account/getFilteredProducts"
        params = {"mediaType": 1,
                  "page": 1,
                  "sortBy": "date_purchased",
                  "totalPages": 1,
                  }
        return iter_catalog(session=self._session,
                            url=url,
                            params=params)

    def get_owned_game_details(self, product_id: int) -> dict:
        url = r"https://www.gog.com/account/gameDetails/{0}.json".format(product_id)
        r = self._get(url)
        r.raise_for_status()
        return r.json()

    def download_game_file(self,
                           url: str,
                           filepath: Path,
                           url_prefix: str = "https://www.gog.com/",
                           chunk_size: int = 1024 ** 2,  # 1 MiB
                           ) -> Optional[dict]:
        """
        Download a game file.

        NOTE: This function is way too complex (14), Refactor it.
        TODO: Rewrite , too complex (19)

        :param url: The remote URL.
        :param filepath: The local path to store it.
        :param url_prefix: The url_prefix or host, usually www.gog.com.
        :param chunk_size: The chunk_size to use for download.
        :return: A dict if everything went smooth. None otherwise.
        """
        dl_url = url
        if not url.startswith(url_prefix):
            dl_url = urljoin(url_prefix, url)
        headers = self._session.headers
        if "Range" in headers:
            headers.pop("Range")
        headers.update({"Referer": "https://www.gog.com/en/account",
                        "User-Agent": self._user_agent,
                        })

        r_dl = self._get(url=dl_url, headers=headers, stream=True, timeout=60)
        try:
            r_dl.raise_for_status()
        except HTTPError as e:
            save_debug_data(r_dl, "missed_download")
            raise e
        else:
            remote_file_size = int(r_dl.headers.get("content-length", 0))
            remote_file_ctime = r_dl.headers.get("Last-Modified")
            fmt = "%a, %d %b %Y %H:%M:%S %Z"
            remote_file_mtime = datetime.datetime.strptime(remote_file_ctime, fmt)
            file_info = {"total_size": remote_file_size,
                         "mtime": remote_file_mtime,
                         }

            # remote file info section
            remote_file_info = None
            file_extensions_without_fileinfo = [".txt", ".zip"]
            if not any(filter(lambda x: r_dl.url.endswith(x), file_extensions_without_fileinfo)):
                remote_file_info = self._get_remote_file_info(file_url=r_dl.url, headers=headers)

            has_remote_fileinfo = (remote_file_info is not None)

            if has_remote_fileinfo:
                # evaluate and update contents
                if remote_file_size != file_info.get("total_size"):
                    self._logger.warning(
                        "File Size missmatch Header {0} != {1} FileInfoXML".format(remote_file_size,
                                                                                   file_info.get("total_size")))
                chunk_size = remote_file_info.get("chunk_size")
                self._logger.debug("chunk size from fileinfo xml is {0} bytes".format(chunk_size))
                file_info.update(remote_file_info)

            # filepath section
            if filepath.is_dir():
                filename = extract_filename_from_download_url(url=r_dl.url)
                finalpath = filepath / filename
            else:
                finalpath = filepath

            file_dict = check_local_file(filepath=finalpath, file_info=file_info)

            if file_dict is not None and file_dict.get("file_ok") is True:
                self._logger.info("File already downloaded {0} - skipping".format(finalpath))
            else:
                # loop initializers
                position = 0
                sha256_ = sha256()
                md5_ = md5()
                mode = 'wb'
                if isinstance(file_dict, dict) and file_dict.get("size") < file_info.get("total_size"):
                    broken_chunks = file_dict.get("broken_chunks")
                    if len(broken_chunks) == 0:
                        r_dl.close()
                        start = file_dict.get("size")
                        stop = int(r_dl.headers.get("content-length", 0))
                        headers.update({"Range": "bytes={0}-{1}".format(start, stop)})
                        r_dl = self._get(url=dl_url, headers=headers, stream=True, timeout=60)
                        sha256_ = file_dict.get("sha256_obj")
                        md5_ = file_dict.get("md5_obj")
                        position = start
                        self._logger.info("File incomplete on disk - Resuming Download at Position {0:%}".format(
                            (file_dict.get("size") / file_info.get("total_size"))))
                        mode = 'ab'

                with finalpath.open(mode=mode) as fd:
                    # fd.seek(position)  # seek to the file position
                    # A quick hack to get some progressbar
                    with tqdm(desc=finalpath.name,
                              total=file_info.get("total_size"),
                              unit="iB",
                              unit_scale=True,
                              unit_divisor=1024,
                              ascii=" .oO0",
                              initial=position,
                              ) as bar:
                        try:
                            for chunk_index, chunk in enumerate(r_dl.iter_content(chunk_size=chunk_size)):
                                check_chunk_md5(file_info=file_info,
                                                chunk=chunk,
                                                position=position)

                                written = fd.write(chunk)

                                bar.update(written)
                                position += written

                                # overall hashes
                                sha256_.update(chunk)
                                md5_.update(chunk)
                        except requests.exceptions.ConnectionError:
                            self._logger.error("Connection error url {0}".format(r_dl.url))

                # finally sync our local mtime to the remote one
                mtime = atime = file_info.get("mtime").timestamp()
                os.utime(finalpath, times=(atime, mtime))

                # final file check
                file_ok = False
                actual_file_md5 = md5_.hexdigest()
                md5_match = None
                if has_remote_fileinfo:
                    expected_file_md5 = file_info.get("md5")
                    md5_match = (expected_file_md5 == actual_file_md5)
                    if md5_match is False:
                        self._logger.warning(
                            "file md5 missmatch expected {0} != {1} actual".format(
                                expected_file_md5, actual_file_md5))
                    else:
                        file_ok = True
                elif finalpath.suffix.lower().endswith("zip"):
                    if ZipFile(file=finalpath).testzip() is None:
                        file_ok = True
                    else:
                        self._logger.warning(
                            "zipfile is broken {0}".format(finalpath.name))
                else:
                    file_ok = True
                file_dict = dict(filepath=finalpath,
                                 size=position,
                                 sha256=sha256_.hexdigest(),
                                 md5=actual_file_md5,
                                 md5_match=md5_match,
                                 mtime=file_info.get("mtime"),
                                 has_remote_fileinfo=has_remote_fileinfo,
                                 file_ok=file_ok,
                                 )

            return file_dict

    def _get_remote_file_info(self, file_url, headers) -> Optional[dict]:
        """
        Retrieve the remote file info xml and return it's parsed contents.

        Follows the best effort strategy.

        :param file_url: The final (after redirect) url to the file.
        :param headers: The url headers.
        :return: The remote file info dict or None.
        """
        remote_file_info = None
        try:
            r_fileinfo = self._get(url=get_fileinfo_url(file_url), headers=headers)
            r_fileinfo.raise_for_status()

            # this overwrites total_size and timestamp
            remote_file_info = parse_file_info_xml(r_fileinfo.text)

        except HTTPError as e:
            self._logger.error(e)
            pass

        return remote_file_info


class GogClientException(BaseException):
    pass
