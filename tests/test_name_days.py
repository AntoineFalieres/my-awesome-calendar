import json
import unittest
from unittest.mock import patch

import app as calendar_app


class FranceNameDaysTests(unittest.TestCase):
    def setUp(self):
        calendar_app.FR_NAMEDAYS_CACHE.clear()
        calendar_app.FR_NAME_DAYS_SOURCE_CACHE = None

    @patch("app.urlopen")
    def test_fr_name_days_include_every_date_in_leap_year(self, urlopen_mock):
        payload = (
            '[{"day":2,"month":2,"fr":"Chandeleur",},'
            '{"day":29,"month":2,"fr":"Auguste",},]'
        )
        urlopen_mock.return_value.__enter__.return_value.read.return_value = payload.encode()

        days = calendar_app.fetch_fr_name_days(2024)

        self.assertEqual(len(days), 366)
        self.assertEqual(days[32], {"date": "2024-02-02", "name": "Chandeleur"})
        self.assertEqual(days[59], {"date": "2024-02-29", "name": "Auguste"})

    @patch("app.urlopen")
    def test_fr_name_days_are_cached_by_year(self, urlopen_mock):
        urlopen_mock.return_value.__enter__.return_value.read.return_value = json.dumps(
            [{"day": 1, "month": 1, "fr": "Jour de l'An"}]
        ).encode()

        calendar_app.fetch_fr_name_days(2026)
        calendar_app.fetch_fr_name_days(2026)

        urlopen_mock.assert_called_once()

    def test_fr_name_days_reject_invalid_year(self):
        with self.assertRaises(ValueError):
            calendar_app.fetch_fr_name_days(1899)

    @patch("app.urlopen")
    def test_name_day_endpoint_returns_daily_rows(self, urlopen_mock):
        urlopen_mock.return_value.__enter__.return_value.read.return_value = json.dumps(
            [{"day": 1, "month": 1, "fr": "Jour de l'An"}]
        ).encode()

        with calendar_app.app.test_client() as client:
            response = client.get("/api/name-days/france/2026")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 365)
        self.assertEqual(response.get_json()[0], {"date": "2026-01-01", "name": "Jour de l'An"})

    @patch("app.urlopen")
    def test_name_day_api_returns_explicit_error_for_invalid_payload(self, urlopen_mock):
        urlopen_mock.return_value.__enter__.return_value.read.return_value = b"{}"

        with calendar_app.app.test_client() as client:
            response = client.get("/api/name-days/france/2026")

        self.assertEqual(response.status_code, 502)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
