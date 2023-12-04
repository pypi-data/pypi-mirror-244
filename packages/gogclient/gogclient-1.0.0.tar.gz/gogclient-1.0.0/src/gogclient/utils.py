""" module:: gogclient.utils
    :platform: All
    :synopsis: A helper and utility collection.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import datetime
import math
from collections import OrderedDict
from hashlib import md5, sha256
from pathlib import Path
from typing import Optional, List, Generator
from urllib.parse import urlparse, parse_qs, unquote
from getpass import getpass
import pickle
import re
from zipfile import ZipFile

from requests import session, get, Session
from requests.cookies import RequestsCookieJar
from lxml.etree import HTML
from xml.etree import ElementTree as ET

import logging

LOGGER = logging.getLogger(__name__)


class ReCaptchaException(Exception):
    pass


def parse_form(html_text) -> dict:
    """
    Parse a javascript form to a dictionary of fields.
    GOG does hide fields for login flow and token,
    so you don't see it in the form.
    :param html_text: The html response from a GET https://auth.gog.com/auth
    :return: A dictionary with the fields.
             If the value is None, it is a user input field.
    """
    root = HTML(html_text)
    # for whatever reason this check is failing - false positives
    if len(root.findall(".//div[@class=\"g-recaptcha form__recaptcha\"]")) > 1:
        raise ReCaptchaException

    fields = {field.get("name"): field.get("value") for field in root.findall(".//input")}
    return fields


def extract_login_url_from_gog_base_url(html_text) -> str:
    """
    Extract the "client_id" from the GET response.
    "client_id" is necessary for authentication call later.
    :param html_text: The html response from a GET https://www.gog.com
    :return: The client id as numeric string
    """
    login_url = re.search(r"https://(login|auth)\.gog\.com/auth\?[^',]*", html_text, flags=re.MULTILINE)[0]
    return login_url


def extract_client_id_from_login_url(login_url: str) -> str:
    """
    Extract the "client_id" from login_url.
    "client_id" is necessary for authentication call later.
    :param login_url: The html response from a GET https://www.gog.com
    :return: The client id as numeric string
    """
    parsed_url = urlparse(login_url)
    parsed_qs = parse_qs(parsed_url.query)
    client_id = parsed_qs.get("client_id")
    return client_id[0]


def extract_code_from_return_login_success_url(login_success_url: str) -> str:
    parsed_url = urlparse(login_success_url)
    parsed_qs = parse_qs(parsed_url.query)
    code = parsed_qs.get("code")[0]
    return code


def user_input_second_step_code():
    """
    Have the user input the 2fa code until we can read emails.
    """
    second_step_input_letters = ["second_step_authentication[token][letter_1]",
                                 "second_step_authentication[token][letter_2]",
                                 "second_step_authentication[token][letter_3]",
                                 "second_step_authentication[token][letter_4]", ]
    second_step_login_data = {}
    second_step_user_input = input("enter two-step security code: ")
    if len(second_step_user_input) != 4:
        raise ValueError("Length of input code {0} is not 4".format(len(second_step_user_input)))
    for k, c in zip(second_step_input_letters, second_step_user_input):
        second_step_login_data.update({k: c})
    return second_step_login_data


def save_debug_data(r, filebase):
    with open("{0}.html".format(filebase), "w") as f:
        f.write(r.text)
    with open("{0}_cookies.txt".format(filebase), "w") as f:
        f.write(str(r.cookies))
    with open("{0}_url.txt".format(filebase), "w") as f:
        f.write(str(r.url))
    with open("{0}_headers.txt".format(filebase), "w") as f:
        f.write(str(r.headers))


def get_credentials() -> dict:
    """
    This function is a stub to be replaced later with a true secure implementation.
    Read the credentials from file and or have the user input them.
    Optionally save the credentials to that file
    :return: A dictionary with the credentials.
    """
    credentials_file = Path.home().joinpath("gog_credentials.pkl")
    if credentials_file.exists():
        try:
            with credentials_file.open("rb") as f:
                credentials = pickle.load(f)
        except pickle.PickleError:
            print("Pickled credentials problem")
    else:
        user_login = input("login: ")
        user_passwd = getpass()
        credentials = {"login[username]": user_login,
                       "login[password]": user_passwd, }
        if input("write these to file? [Y/N]").upper() == "Y":
            with credentials_file.open("wb") as f:
                pickle.dump(credentials, f)
    return credentials


def parse_catalog_json(catalog_data: dict) -> dict:
    """
    Parse the raw catalog data to a product_id dictionary.
    :param catalog_data: the r.json() from the url response
    :return: A dictionary product_id: {product_data...}
    """
    products = catalog_data.get("products")
    product_dict = OrderedDict()
    for product in products:
        id_ = int(product.pop("id"))
        if id_ not in product_dict:
            product_dict.update({id_: product})

    if len(product_dict) != catalog_data.get("productCount"):
        LOGGER.error(
            "Mismatch between advertised productCount {0} !="
            " {1} number of unique id's in products over".format(
                catalog_data.get("productCount"), len(product_dict)))
    return product_dict


def get_catalog_from_get_products_url(session: Session,
                                      url: str,
                                      params: dict) -> dict:
    s = session
    r = s.get(url=url, params=params)

    r.raise_for_status()
    catalog_data = r.json()
    pages = catalog_data.get("pages")  # regular catalog uses pages
    if pages is None:
        pages = catalog_data.get("totalPages")  # account/getFilteredProducts uses totalPages
    if pages is not None:
        for page in range(2, pages + 1):
            params.update({"page": page})
            r = s.get(url=url, params=params)
            catalog_page_data = r.json().get("products")
            catalog_data.get("products").extend(catalog_page_data)
    return parse_catalog_json(catalog_data)


def iter_catalog(session: Session,
                 url: str,
                 params: dict) -> Generator[dict, None, None]:
    s = session
    r = s.get(url=url, params=params)

    r.raise_for_status()
    catalog_data = r.json()
    products = catalog_data.get("products")
    for product in products:
        yield product
    pages = catalog_data.get("pages")  # regular catalog uses pages
    if pages is None:
        pages = catalog_data.get("totalPages")  # account/getFilteredProducts uses totalPages
    if pages is not None:
        for page in range(2, pages + 1):
            params.update({"page": page})
            r = s.get(url=url, params=params)
            catalog_data = r.json()
            products = catalog_data.get("products")
            for product in products:
                yield product


def normalize_gog_url(url: str) -> str:
    """
    Since about 2022, GOG started to use locales inside their urls,
    e.g. gog.com/de/games/ instead of gog.com/games.
    This invades privacy and should be normalized to make tracking and geo-blocking harder for GOG.
    :param url: The url.
    :return: The normalized url.
    """
    return re.sub(pattern="/(de|en)/", repl="/", string=url, flags=re.IGNORECASE)


def get_url_from_product_data(product_data: dict, normalize_url: bool = True) -> Optional[str]:
    """
    Get the url from product_data json.
    :param product_data: The json dict.
    :param normalize_url: Switch if url should be normalized.
    :return: The url.
    """
    link = product_data.get("_links").get("support").get("href").replace("support", "game")  # some workaround
    if normalize_url is True and link is not None:
        return normalize_gog_url(link)
    else:
        return link


def get_country_code_from_locale(locale: str) -> str:
    """
    There is a dilemma, that gog uses 3 different locales,
    - general locale in url params locale={language}_{country}, e.g. &locale=de_DE
    - country_code in url params countryCode={country}, e.g. &countryCode=DE
    - gog_loc cookie value, {country}_{currency}-{language}_{country}, e.g. gog_loc=DE_EUR-de_DE
    using the locale and derive the country code seems to be the most feasible approach.
    :param locale: The locale as typically used.
    :return: The country code string.
    """
    return locale.split("_")[-1]


def gog_locale_from_locale_and_currency(locale: str,
                                        currency: str) -> str:
    return "{0}_{1}-{2}".format(get_country_code_from_locale(locale=locale),
                                currency,
                                locale)


def is_url_geo_blocked_for_locale(url: str,
                                  gog_locale: str = "DE_EUR_de-DE"):
    """
    Check if the locale is geo-blocked, e.g. do we get redirected
    to the catalog page instead of the url that we requested.
    :param url: The url.
    :param gog_locale: The gog_lc cookie value.
                       In Java Names the gog locale value is
                       {countryCode}_{currency}_{locale}.
    :return: True if blocked, False otherwise.
    """
    cookies = RequestsCookieJar()
    cookies.set(domain=".gog.com", name="gog_lc", value=gog_locale)
    r = get(url=url, cookies=cookies)
    LOGGER.debug("url req {0} resp {1}".format(url, r.url))
    return url != r.url


def get_flash_deals(sess: Optional[session] = None,
                    url: str = r"https://www.gog.com/") -> Optional[dict]:
    """
    Check GOG main page for <div custom-section=XXX flash-deals >
    :param sess: The session to use.
    :param url: The url. Typically, GOG main page.
    :return: True if blocked, False otherwise.
    """
    s = sess or session()
    r = s.get(url=url)
    r.raise_for_status()
    root = HTML(r.text)
    custom_section_node = root.find(".//div[@flash-deals]")
    if custom_section_node is not None:
        custom_section = custom_section_node.get("custom-section")
        if custom_section is not None:
            r = s.get(url=r"https://www.gog.com/custom_sections/{0}".format(custom_section))
            r.raise_for_status()
            return r.json()


def extract_product_id_from_api_v2_url(apiv2url: str) -> int:
    parsed_url = urlparse(apiv2url)
    product_id = int(parsed_url.path.rsplit("/", maxsplit=1)[-1])
    return product_id


def extract_slug_from_product_url(product_url: str) -> str:
    parsed_url = urlparse(product_url)
    slug = parsed_url.path.rsplit("/", maxsplit=1)[-1]
    return slug


def extract_product_type_from_product_data(product_data: dict) -> str:
    product_type = product_data.get("productType")
    if not product_type:
        embedded = product_data.get("_embedded")
        if embedded:
            product_type = embedded.get("productType")
    if isinstance(product_type, str):
        product_type = product_type.upper()
    return product_type


def extract_product_title_from_product_data(product_data: dict) -> str:
    product_title = product_data.get("_embedded").get("product").get("title")
    return product_title


def extract_has_product_card_from_product_data(product_data: dict) -> bool:
    has_product_card = product_data.get("_embedded").get("product").get("hasProductCard")
    return has_product_card


def extract_product_slug_from_download_url(download_url: str) -> str:
    parsed_url = urlparse(download_url)
    slug = parsed_url.path.rsplit("/")[-2]
    return slug


def extract_filename_from_download_url(url: str) -> str:
    parsed_url = urlparse(url=url)
    filename = unquote(parsed_url.path).rsplit("/", maxsplit=1)[-1]
    return filename


def filter_downloads(downloads_dict: dict,
                     languages: List[str],
                     os_names: List[str],
                     language_fallback: str = "English",
                     os_fallback: str = "windows",
                     ):
    ret = dict()
    languages_work = languages.copy()
    os_names_work = os_names.copy()  # need to copy, otherwise changes end up in the input lists
    for language, os_dict in downloads_dict:
        if not any(language in downloads_dict for language in languages_work):
            languages_work.append(language_fallback)
        if language in languages_work:
            ret.update({language: {}})
            ret_os_dict = ret.get(language)
            if not any(osname in os_dict for osname in os_names_work):
                os_names_work.append(os_fallback)
            for os_name, os_downloads in os_dict.items():
                if os_name in os_names_work:
                    ret_os_dict.update({os_name: os_downloads})
    return ret


def filter_extras(extras_list: list,
                  languages: List[str],
                  audio_formats: List[str],
                  video_formats: List[str],
                  os_list: List[str],
                  no_avatars: bool = True,
                  no_ringtones: bool = True
                  ):
    """
    Filter product extras
    TODO: - Wallpapers also have 4K, 1080p filtering
          - no screen saver name=screensaver
          - over series duplicates see bd_ladymageknight.zip in 1207659105, 1207658806

    :param extras_list: A list of dictionaries, one for each extra.
    :param languages: A list of allowed languages
    :param audio_formats: A list of allowed audio formats
    :param video_formats: A list of allowed video formats
    :param os_list: A list of allowed os
    :return: the filtered list of extras
    """
    ret = list()
    for extra_download in extras_list:
        if all((filter_extra_by_language(extra_download, languages=languages),
                filter_audio_by_format(extra_download, audio_formats=audio_formats),
                filter_video_by_format(extra_download, video_formats=video_formats),
                filter_game_addons_by_os(extra_download, os_list=os_list),
                filter_avatars(extra_download, no_avatars=no_avatars),
                filter_ringtones(extra_download, no_ringtones=no_ringtones),
                )):
            ret.append(extra_download)

    return ret


def filter_extra_by_language(extra_download: dict,
                             languages: List[str]) -> bool:
    """
    Filter extra by language if there is language indication
    in the name.

    :param extra_download: A extra download dictionary
    :param languages: A list of allowed languages
    :return: True if filter matches
    """

    REGEX_EXTRA_WITH_LONG_LANGUAGE_INLINE = r".*(GERMAN|ENGLISH|FRENCH|ITALIAN|SPANISH|RUSSIAN|JAPANESE|POLISH|" \
                                            r"UKRAINIAN|DE|EN|FR|ITA|SPA|RU|BR|JP|PL)[\W\)].*"
    # NOTE: WHAT IS BR for a locale, brazil?
    dl_name = extra_download.get("name")
    if re.match(REGEX_EXTRA_WITH_LONG_LANGUAGE_INLINE, dl_name, flags=re.IGNORECASE) \
            and not any(language in dl_name for language in languages):
        return False
    return True


def filter_audio_by_format(extra_download: dict,
                           audio_formats: List[str]) -> bool:
    """
    Filter extra by audio format if it is of type audio and there is
    audio format indication in the name.

    :param extra_download: A extra download dictionary
    :param audio_formats: A list of allowed audio formats
    :return:
    """
    REGEX_AUDIO_WITH_FORMAT = r".*\(.*(MP3|FLAC|WAV|OGG).*\)"
    dl_name = extra_download.get("name")
    dl_type = extra_download.get("type")
    if dl_type == "audio":
        if re.match(REGEX_AUDIO_WITH_FORMAT, dl_name, flags=re.IGNORECASE) \
                and not any(audio.lower() in dl_name.lower() for audio in audio_formats):
            return False
    return True


def filter_video_by_format(extra_download: dict,
                           video_formats: List[str]) -> bool:
    """
    Filter extra by video format if it is of type video and there is
    video format indication in the name.

    :param extra_download: A extra download dictionary
    :param video_formats: A list of allowed video formats
    :return:
    """
    REGEX_AUDIO_WITH_FORMAT = r".*\(.*(DVD|4k|1080p|720p).*\)"
    dl_name = extra_download.get("name")
    dl_type = extra_download.get("type")
    if dl_type == "video":
        if re.match(REGEX_AUDIO_WITH_FORMAT, dl_name, flags=re.IGNORECASE) \
                and not any(video.lower() in dl_name.lower() for video in video_formats):
            return False
    return True


def filter_game_addons_by_os(extra_download: dict,
                             os_list: List[str]) -> bool:
    """
    Filter extra by os names.

    :param extra_download: A extra download dictionary
    :param os_list: A list of allowed os names
    :return:
    """
    REGEX_GAME_ADD_ON_WITH_OS = r".*\(.*(LINUX|WINDOWS|OSX).*\)"
    dl_name = extra_download.get("name")
    dl_type = extra_download.get("type")
    if dl_type == "game add-ons":
        if re.match(REGEX_GAME_ADD_ON_WITH_OS, dl_name, flags=re.IGNORECASE) \
                and not any(os_name.lower() in dl_name.lower() for os_name in os_list):
            return False
    return True


def filter_avatars(extra_download: dict,
                   no_avatars: bool = True
                   ) -> bool:
    """
    Filter avatars, they are annoying.

    :param extra_download: A extra download dictionary
    :param no_avatars: switch to filter avatars
    :return:
    """
    dl_type = extra_download.get("type")
    if dl_type == "avatars":
        return not no_avatars
    else:
        return True


def filter_ringtones(extra_download: dict,
                     no_ringtones: bool = True
                     ) -> bool:
    """
    Filter ringtones, they are annoying.

    :param extra_download: A extra download dictionary
    :param no_ringtones: switch to filter ringtones
    :return:
    """

    dl_name = extra_download.get("name")
    dl_type = extra_download.get("type")
    if dl_type == "audio" and "ringtone".lower() in dl_name.lower():
        return not no_ringtones
    else:
        return True


def is_patch_download(url: str) -> bool:
    """
    Return True if the given url leads to a patch download

    :param url: The url.
    :return: True if patch download, False if not
    """
    return "patch" in url


def parse_file_info_xml(data: str) -> dict:
    """
    Parse a xml-based file info description.
    This description is available for most files on GOG CDN,
    just add ".xml" to the final url.

    :param data: The xml data.
    :return: A dict with parsed info.
    """
    root = ET.fromstring(data)
    chunks = [
        {"content_range": (int(chunk.get("from")), int(chunk.get("to"))),
         chunk.get("method"): chunk.text}
        for chunk in root.findall("./chunk")
    ]

    ret = {"chunks": chunks}
    ret.update({
        "chunk_size": chunks[0].get("content_range")[1] + 1,  # Starts counting at 0 and includes the last one, e.g. +1
    })
    ret.update({key: root.get(key) for key in ["name", "md5"]})
    ret.update({key: int(root.get(key)) for key in ["total_size", ]})
    fmt = "%Y-%m-%d %H:%M:%S"
    ret.update({key: datetime.datetime.strptime(root.get(key), fmt) for key in ["timestamp", ]})
    return ret


def check_local_file(filepath: Path,
                     file_info: dict,
                     chunk_size: int = 10 * 1024 ** 2) -> Optional[dict]:
    """
    Check if the file exists, if the size fits and the md5 fits
    :param filepath: The filepath Path.
    :param file_info: The fileinfo dict.
    :param chunk_size: The size of the chunk.
    :return: True if ok, False otherwise.
    """
    file_dict = None
    md5_obj = None
    sha256_ = None
    md5_ = None
    md5_match = None
    broken_chunks = []
    file_ok = False
    print("checking {0}".format(filepath))
    if filepath.exists():
        LOGGER.info("exists")
        file_lstat = filepath.lstat()
        file_has_correct_size = (file_lstat.st_size == file_info.get("total_size"))
        remote_file_mtime = file_info.get("mtime")
        file_has_correct_mtime = (remote_file_mtime is None
                                  or file_lstat.st_mtime == remote_file_mtime.timestamp())
        if file_has_correct_size \
                and file_has_correct_mtime:
            if file_info.get("chunk_size") is not None:
                chunk_size = file_info.get("chunk_size")

            if (file_info.get("md5") is not None) \
                    or ((filepath.suffix.lower().endswith("zip"))
                        and (ZipFile(file=filepath).testzip() is None)) \
                    or (filepath.suffix.lower() == "txt"):
                md5_obj = md5()
                sha256_obj = sha256()
                chunk_list = file_info.get("chunks")
                position = 0
                with filepath.open("rb") as fp:
                    for chunk_index in range(math.ceil(file_lstat.st_size / chunk_size)):
                        chunk = fp.read(chunk_size)
                        md5_obj.update(chunk)
                        sha256_obj.update(chunk)

                        if check_chunk_md5(file_info=file_info,
                                           chunk=chunk,
                                           position=position) is not True:
                            broken_chunks.append(chunk_list[chunk_index])

                        position += chunk_size

                sha256_ = sha256_obj.hexdigest()
                md5_ = md5_obj.hexdigest()

                if file_info.get("md5") is not None:
                    md5_match = (file_info.get("md5") == md5_)
                    if md5_match is True:
                        LOGGER.info("MD5 OK")
                        file_ok = True
                    else:
                        LOGGER.info("MD5 Missmatch")
                else:
                    file_ok = True
                    LOGGER.info("no md5 available to check {0}".format(filepath.name))
        else:
            LOGGER.error(
                "Invalid local file size {0} or mtime {1}".format(file_has_correct_size, file_has_correct_mtime))

        file_dict = dict(filepath=filepath,
                         size=file_lstat.st_size,  # for partial content dl later
                         sha256=sha256_,
                         sha256_obj=sha256_,
                         md5=md5_,
                         md5_obj=md5_obj,
                         md5_match=md5_match,
                         mtime=datetime.datetime.fromtimestamp(file_lstat.st_mtime),
                         broken_chunks=broken_chunks,
                         file_ok=file_ok,
                         )
    return file_dict


def get_chunk_at_position(chunks: list, position: int) -> dict:
    for chunk in chunks:
        if chunk.get("content_range")[0] == position:
            return chunk


def get_fileinfo_url(url: str) -> str:
    return "{0}.xml".format(url)


def check_chunk_md5(file_info: dict, chunk: bytes, position: int) -> bool:
    """
    Check a freshly downloaded chunk of a file against it's expected hashes.

    This is currently only for debug reasons and does not yet do anything in program flow.

    :param file_info: The file_info dict, actually the remote_file_info dict
    :param chunk: The data bytes.
    :param position: The current position in download.
    :return: True if hash ok.
    """
    ret = True
    chunk_list = file_info.get("chunks")  # in case we have chunks to check
    if chunk_list is not None:
        chunk_hash = md5()
        chunk_hash.update(chunk)
        actual_chunk_md5 = chunk_hash.hexdigest()
        assert isinstance(chunk_list, list)
        expected_chunk = get_chunk_at_position(chunks=chunk_list, position=position)
        expected_chunk_md5 = expected_chunk.get("md5")
        if expected_chunk_md5 != actual_chunk_md5:
            LOGGER.warning(
                "chunk from {0}-{1} has md5 missmatch expected {2} != {3} actual".format(
                    position, position + len(chunk), expected_chunk_md5, actual_chunk_md5))
            ret = False
    return ret


# def is_file_ok(file_info: dict) -> bool:
#     """
#     Check if a file has all properties to count as OK
#
#     :param file_info: The file info dict.
#     :return: True if every condition is fulfilled. False otherwise.
#     """
#     LOGGER.debug("is_file_ok {0}".format(file_info))
#     return all([file_info is not None,
#                 any([
#                     file_info.get("md5_match") is True,
#                     file_info.get("has_remote_fileinfo") is False]
#                     )
#                 ])
