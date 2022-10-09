import unittest
from unittest.mock import patch

from what_is_year_now import *


class TestWhatIsYearNow(unittest.TestCase):
    def test_ymd_format(self):
        with patch('what_is_year_now.urllib.request.urlopen') as mocked_url_open:
            with patch('what_is_year_now.json.load') as mocked_json_load:
                mocked_json_load.return_value = {
                    'id': 1,
                    'currentDateTime': '2019-03-01'
                }
                assert 2019 == what_is_year_now()

    def test_dmy_format(self):
        with patch('what_is_year_now.urllib.request.urlopen') as mocked_url_open:
            with patch('what_is_year_now.json.load') as mocked_json_load:
                mocked_json_load.return_value = {
                    'id': 10,
                    'currentDateTime': '01.03.2019'
                }
                assert 2019 == what_is_year_now()

    def test_invalid_format(self):
        with patch('what_is_year_now.urllib.request.urlopen') as mocked_url_open:
            with patch('what_is_year_now.json.load') as mocked_json_load:
                mocked_json_load.return_value = {
                    'id': 100,
                    'currentDateTime': '1.3.2019'
                }
                with self.assertRaises(ValueError,  msg='Invalid format'):
                    what_is_year_now()
