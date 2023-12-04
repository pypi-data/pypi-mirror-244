""" module:: tests.test_utils
    :platform: All
    :synopsis: A selection of pytest tests
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
from pathlib import Path

import pytest

from gogclient.utils import filter_extras, parse_file_info_xml, check_local_file

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def file_info_mock_path() -> Path:
    yield list(Path(".").glob("**/data/setup_guacamelee_super_turbo_championship_edition_1.00_(24522).exe.xml"))[0]


@pytest.fixture()
def file_info_mock_content(file_info_mock_path):
    with file_info_mock_path.open("r") as fp:
        yield fp.read()


@pytest.fixture()
def file_info_mock(file_info_mock_content):
    yield parse_file_info_xml(file_info_mock_content)


@pytest.fixture()
def file_to_check_mock_path():
    yield list(Path("/tmp").glob("setup_guacamelee_super_turbo_championship_edition_1.00_(24522).exe"))[0]


class TestHelpers:
    @pytest.mark.parametrize("test_data,languages,audio_formats,video_formats,expected", [
        ([{"name": "Anno 1404 manual (EN, FR, ITA, SPA)",
           "type": "manual"}],
         ["English", "EN"],
         [],
         [],
         [{"name": "Anno 1404 manual (EN, FR, ITA, SPA)",
           "type": "manual"}],
         ),
        ([{"name": "Anno 1404 manual (EN, FR, ITA, SPA)",
           "type": "manual"}],
         ["JAPANESE", "JP"],
         [],
         [],
         [],
         ),
        ([{"name": "editor manual (129 pages)",
           "type": "manual"}],
         ["JAPANESE", "JP"],
         [],
         [],
         [{"name": "editor manual (129 pages)",
           "type": "manual"}],
         ),
        ([{"name": "manual (French)",
           "type": "manual"}],
         ["JAPANESE", "JP"],
         [],
         [],
         [],
         ),
        ([{"name": "manual (French)",
           "type": "manual"}],
         ["French", "FR"],
         [],
         [],
         [{"name": "manual (French)",
           "type": "manual"}],
         ),
        ([{"name": "manual(RU)",
           "type": "manual"}],
         ["French", "FR"],
         [],
         [],
         [],
         ),
        ([{"name": "Linux Russian localization (Fargus)",
           "type": "game add-ons"}],
         ["French", "FR"],
         [],
         [],
         [],
         ),
        ([{"name": "Russian localization (Fargus)",
           "type": "game add-ons"}],
         ["French", "FR"],
         [],
         [],
         [],
         ),
        ([{"name": "soundtrack (MP3)",
           "type": "audio"}],
         [],
         ["MP3"],
         [],
         [{"name": "soundtrack (MP3)",
           "type": "audio"}],
         ),
        ([{"name": "soundtrack (FLAC)",
           "type": "audio"}],
         [],
         ["MP3"],
         [],
         [],
         ),
        ([{"name": "Machinarium Remixed (MP3)",
           "type": "audio"}],
         [],
         ["MP3"],
         [],
         [{"name": "Machinarium Remixed (MP3)",
           "type": "audio"}],
         ),
        ([{"name": "original soundtrack",
           "type": "audio"}],
         [],
         ["MP3"],
         [],
         [{"name": "original soundtrack",
           "type": "audio"}],
         ),
        ([{"name": "soundtrack (Homeworld 2, FLAC)",
           "type": "audio"}],
         [],
         ["FLAC"],
         [],
         [{"name": "soundtrack (Homeworld 2, FLAC)",
           "type": "audio"}],
         ),
        ([{"name": "soundtrack (Homeworld 2, FLAC)",
           "type": "audio"}],
         [],
         ["MP3"],
         [],
         [],
         ),
        ([{"name": "developer interview (English)",
           "type": "video"}],
         ["English", "EN"],
         [],
         [],
         [{"name": "developer interview (English)",
           "type": "video"}],
         ),
        ([{"name": "developer interview (English)",
           "type": "video"}],
         ["German", "DE"],
         [],
         [],
         [],
         ),
        ([{"name": "Video Game Show — The Witcher 3: Wild Hunt concert (720p)",
           "type": "video"},
          {"name": "Video Game Show — The Witcher 3: Wild Hunt concert (1080p)",
           "type": "video"},
          {"name": "Video Game Show — The Witcher 3: Wild Hunt concert (dvd)",
           "type": "video"},
          {"name": "Video Game Show — The Witcher 3: Wild Hunt concert (4K)",
           "type": "video"},
          ],
         ["German", "DE"],
         [],
         ["4k", "dvd"],
         [{"name": "Video Game Show — The Witcher 3: Wild Hunt concert (dvd)",
           "type": "video"},
          {"name": "Video Game Show — The Witcher 3: Wild Hunt concert (4K)",
           "type": "video"},
          ],
         ),
        ([{"name": "Witcher 3 GOTY Classic BR Language Patch Part1",
           "type": "game add-on"},
          {"name": "Witcher 3 GOTY Classic FR Language Patch Part1",
           "type": "game add-on"},
          {"name": "Witcher 3 GOTY Classic EN Language Patch Part1",
           "type": "game add-on"},
          {"name": "Witcher 3 GOTY Classic DE Language Patch Part1",
           "type": "game add-on"},
          {"name": "Witcher 3 GOTY Classic RU Language Patch Part1",
           "type": "game add-on"},
          {"name": "Witcher 3 GOTY Classic JP Language Patch Part1",
           "type": "game add-on"},
          {"name": "Witcher 3 GOTY Classic PL Language Patch Part1",
           "type": "game add-on"},
          ],
         ["German", "DE"],
         [],
         [],
         [{"name": "Witcher 3 GOTY Classic DE Language Patch Part1",
           "type": "game add-on"},
          ],
         ),
        ([{"name": "Legacy Version (OSX)",
           "type": "game add-ons"},
          {"name": "Legacy Version (Windows)",
           "type": "game add-ons"},
          {"name": "Legacy Version (Linux)",
           "type": "game add-ons"},
          ],
         ["German", "DE"],
         [],
         [],
         [{"name": "Legacy Version (Linux)",
           "type": "game add-ons"},
          ],
         ),
        ([{"name": "Some fancy name",
           "type": "avatars"},
          {"name": "Nice ringtones",
           "type": "audio"},
          ],
         ["German", "DE"],
         [],
         [],
         [],
         ),
    ])
    def test_filter_extras(self, test_data, languages, audio_formats, video_formats, expected):
        result = filter_extras(extras_list=test_data,
                               languages=languages,
                               audio_formats=audio_formats,
                               video_formats=video_formats,
                               os_list=["Linux", ])  # Todo: put into parameterize
        assert result == expected


def test_parse_file_info_xml(file_info_mock_content):
    parsed_content = parse_file_info_xml(file_info_mock_content)
    assert parsed_content.get("total_size") == 862253176
    assert parsed_content.get("chunk_size") == 10485760
    assert parsed_content.get("name") == "setup_guacamelee_super_turbo_championship_edition_1.00_(24522).exe"
    assert parsed_content.get("md5") == "7079c3e70e88936f349738459b0dcb6e"
    last_chunk = parsed_content.get("chunks")[-1]
    assert last_chunk.get("content_range") == (859832320, 862253175)
    assert last_chunk.get("md5") == "60785b9911661543ed37a15f75dcb64f"


@pytest.mark.skip("No temp file")
def test_check_local_file(file_info_mock, file_to_check_mock_path):
    result = check_local_file(file_to_check_mock_path, file_info_mock)
    assert result
