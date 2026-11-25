import json
import re
import unittest
from unittest.mock import patch

import app as calendar_app

PUBLIC_HOLIDAYS = [
    {"title": "Jour de l'An", "start": "2026-01-01", "holidayType": "public"},
    {"title": "Lundi de Pâques", "start": "2026-04-06", "holidayType": "public"},
]


class SiteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = calendar_app.app.test_client()
        calendar_app.REVENUE_EVENT_COUNTS.clear()
        calendar_app.METRICS_REQUEST_LOG.clear()


class FranceSeoPageTests(SiteTestCase):
    @patch("app.fetch_fr_public_holidays", return_value=PUBLIC_HOLIDAYS)
    def test_public_holidays_page_uses_french_dates_and_json_ld(self, _fetch):
        response = self.client.get("/france/2026/public-holidays")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("jeudi 1er janvier 2026", html)
        self.assertIn('<time datetime="2026-01-01"', html)
        self.assertIn('"Event"', html)
        self.assertIn("BreadcrumbList", html)
        self.assertIn('property="og:title"', html)

    @patch("app.fetch_fr_public_holidays", side_effect=RuntimeError("upstream down"))
    def test_public_holidays_page_returns_503_when_upstream_fails(self, _fetch):
        response = self.client.get("/france/2026/public-holidays")

        self.assertEqual(response.status_code, 503)
        self.assertNotIn("upstream down", response.get_data(as_text=True))

    def test_school_holidays_page_lists_named_periods(self):
        response = self.client.get("/france/2026/school-holidays/A")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Vacances d&#39;hiver", html)
        self.assertIn("samedi 7 février 2026", html)
        self.assertIn('aria-current="page" class="fw-bold">Zone A', html)

    def test_school_holidays_page_is_404_without_data(self):
        self.assertEqual(self.client.get("/france/2028/school-holidays/A").status_code, 404)

    def test_unknown_zone_and_year_are_404(self):
        self.assertEqual(self.client.get("/france/2026/school-holidays/D").status_code, 404)
        self.assertEqual(self.client.get("/france/1999").status_code, 404)

    def test_lowercase_zone_redirects_permanently(self):
        response = self.client.get("/france/2026/school-holidays/a")

        self.assertEqual(response.status_code, 301)
        self.assertTrue(response.headers["Location"].endswith("/france/2026/school-holidays/A"))

    def test_landing_page_without_school_data_hides_zone_links(self):
        html = self.client.get("/france/2028").get_data(as_text=True)

        self.assertNotIn("/school-holidays/", html)
        self.assertIn("/france/2028/public-holidays", html)

    def test_every_page_has_footer_and_skip_link(self):
        html = self.client.get("/france/2026").get_data(as_text=True)

        self.assertIn('class="skip-link"', html)
        self.assertIn("/privacy-policy", html)
        self.assertIn("/france/", html)


class CrawlabilityTests(SiteTestCase):
    def test_sitemap_lists_only_pages_with_content(self):
        response = self.client.get("/sitemap.xml")
        urls = re.findall(r"<loc>([^<]+)</loc>", response.get_data(as_text=True))

        self.assertEqual(response.mimetype, "application/xml")
        self.assertIn("http://localhost/france/2026/school-holidays/B", urls)
        self.assertIn("http://localhost/france/2028/public-holidays", urls)
        self.assertNotIn("http://localhost/france/2028/school-holidays/A", urls)
        self.assertEqual(len(urls), len(set(urls)))

    def test_robots_blocks_api_and_points_to_sitemap(self):
        body = self.client.get("/robots.txt").get_data(as_text=True)

        self.assertIn("Disallow: /api/", body)
        self.assertIn("Sitemap: http://localhost/sitemap.xml", body)

    def test_canonical_url_prefers_configured_site_url(self):
        with patch.object(calendar_app, "SITE_URL", "https://example.fr"):
            html = self.client.get("/france/2026").get_data(as_text=True)
            sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)

        self.assertIn('<link rel="canonical" href="https://example.fr/france/2026">', html)
        self.assertIn("<loc>https://example.fr/</loc>", sitemap)


class AdsAndConsentTests(SiteTestCase):
    def test_no_ad_markup_or_ad_script_with_placeholder_ids(self):
        for path in ("/", "/france/2026", "/mentions-legales"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertNotIn("googlesyndication", html)
            self.assertNotIn("adsbygoogle", html)

    def test_ad_slots_render_only_with_client_id_and_cmp(self):
        with patch.object(calendar_app, "ADS_ENABLED", True), \
                patch.object(calendar_app, "ADSENSE_CLIENT_ID", "ca-pub-1234567890"):
            without_cmp = self.client.get("/france/2026").get_data(as_text=True)
            with patch.object(calendar_app, "CMP_SCRIPT_URL", "https://cmp.example/loader.js"):
                with_cmp = self.client.get("/france/2026").get_data(as_text=True)
                legal = self.client.get("/privacy-policy").get_data(as_text=True)

        self.assertNotIn("adsbygoogle", without_cmp)
        self.assertIn("adsbygoogle", with_cmp)
        self.assertIn('src="https://cmp.example/loader.js"', with_cmp)
        self.assertIn("data-open-consent", with_cmp)
        # The ad script itself is injected by static/site.js only after consent.
        self.assertNotIn("googlesyndication", with_cmp)
        self.assertNotIn("adsbygoogle", legal)

    def test_production_rejects_placeholder_configuration_when_ads_enabled(self):
        with patch.object(calendar_app, "APP_ENV", "production"), \
                patch.object(calendar_app, "ADS_ENABLED", True), \
                patch.object(calendar_app, "SITE_URL", "https://example.fr"):
            with self.assertRaises(RuntimeError) as context:
                calendar_app.validate_production_config()

        self.assertIn("ADSENSE_CLIENT_ID", str(context.exception))
        self.assertIn("CMP_SCRIPT_URL", str(context.exception))
        self.assertIn("ads.txt", str(context.exception))

    def test_production_without_ads_skips_ad_checks_but_requires_site_url(self):
        with patch.object(calendar_app, "APP_ENV", "production"), \
                patch.object(calendar_app, "ADS_ENABLED", False):
            with patch.object(calendar_app, "SITE_URL", "https://example.fr"):
                calendar_app.validate_production_config()
            with patch.object(calendar_app, "SITE_URL", ""):
                with self.assertRaises(RuntimeError) as context:
                    calendar_app.validate_production_config()

        self.assertEqual(str(context.exception), "Invalid production configuration: SITE_URL is not set")

    def test_development_allows_placeholder_configuration(self):
        calendar_app.validate_production_config()

    def test_ads_disabled_loads_no_ad_consent_or_measurement_code(self):
        with patch.object(calendar_app, "ADS_ENABLED", False), \
                patch.object(calendar_app, "ADSENSE_CLIENT_ID", "ca-pub-1234567890"), \
                patch.object(calendar_app, "CMP_SCRIPT_URL", "https://cmp.example/loader.js"):
            html = self.client.get("/france/2026").get_data(as_text=True)
            ads_txt = self.client.get("/ads.txt")
            metrics = self.client.post(
                "/api/metrics/revenue",
                data=json.dumps({"pageType": "calendar-home", "eventType": "page_view", "status": "viewed"}),
                content_type="application/json",
            )
            with patch.object(calendar_app, "METRICS_TOKEN", "secret"):
                summary = self.client.get("/api/metrics/revenue/summary", headers={"X-Metrics-Token": "secret"})

        self.assertNotIn("cmp.example", html)
        self.assertNotIn("data-open-consent", html)
        self.assertNotIn("adsbygoogle", html)
        self.assertIn('data-ads-enabled="0"', html)
        self.assertIn('data-cmp-enabled="0"', html)
        self.assertEqual((ads_txt.status_code, metrics.status_code, summary.status_code), (404, 404, 404))
        self.assertEqual(calendar_app.REVENUE_EVENT_COUNTS, {})


class MetricsEndpointTests(SiteTestCase):
    def setUp(self):
        super().setUp()
        ads_enabled = patch.object(calendar_app, "ADS_ENABLED", True)
        ads_enabled.start()
        self.addCleanup(ads_enabled.stop)

    def post_event(self, payload, **kwargs):
        return self.client.post("/api/metrics/revenue", data=json.dumps(payload), content_type="application/json", **kwargs)

    def test_accepts_known_event(self):
        response = self.post_event(
            {"pageType": "calendar-home", "eventType": "page_view", "status": "viewed"}
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(calendar_app.REVENUE_EVENT_COUNTS[("calendar-home", "page_view", "none", "viewed")], 1)

    def test_rejects_unknown_event_type_and_malformed_fields(self):
        base = {"pageType": "calendar-home", "eventType": "page_view", "status": "viewed"}
        for override in (
            {"eventType": "<script>"},
            {"status": "weird"},
            {"pageType": "Bad Page!"},
            {"slot": "x" * 100},
        ):
            self.assertEqual(self.post_event({**base, **override}).status_code, 400, override)
        self.assertEqual(calendar_app.REVENUE_EVENT_COUNTS, {})

    def test_distinct_keys_are_capped(self):
        with patch.object(calendar_app, "METRICS_MAX_DISTINCT_KEYS", 1):
            first = self.post_event({"pageType": "a", "eventType": "page_view", "status": "viewed"})
            second = self.post_event({"pageType": "b", "eventType": "page_view", "status": "viewed"})
            repeat = self.post_event({"pageType": "a", "eventType": "page_view", "status": "viewed"})

        self.assertEqual((first.status_code, second.status_code, repeat.status_code), (202, 400, 202))

    def test_rate_limit_returns_429(self):
        payload = {"pageType": "calendar-home", "eventType": "page_view", "status": "viewed"}
        with patch.object(calendar_app, "METRICS_RATE_LIMIT", 2):
            codes = [self.post_event(payload).status_code for _ in range(3)]

        self.assertEqual(codes, [202, 202, 429])

    def test_summary_requires_token(self):
        self.post_event({"pageType": "calendar-home", "eventType": "page_view", "status": "viewed"})

        self.assertEqual(self.client.get("/api/metrics/revenue/summary").status_code, 404)
        with patch.object(calendar_app, "METRICS_TOKEN", "secret"):
            self.assertEqual(self.client.get("/api/metrics/revenue/summary").status_code, 404)
            wrong = self.client.get("/api/metrics/revenue/summary", headers={"X-Metrics-Token": "nope"})
            right = self.client.get("/api/metrics/revenue/summary", headers={"X-Metrics-Token": "secret"})

        self.assertEqual(wrong.status_code, 404)
        self.assertEqual(right.status_code, 200)
        self.assertEqual(right.get_json()[0]["count"], 1)


class FrenchDateTests(unittest.TestCase):
    def test_formats_weekday_and_first_of_month(self):
        self.assertEqual(calendar_app.format_french_date("2026-01-01"), "jeudi 1er janvier 2026")
        self.assertEqual(calendar_app.format_french_date("2026-12-25"), "vendredi 25 décembre 2026")
        self.assertEqual(calendar_app.format_french_date("2026-08-02", with_weekday=False), "2 août 2026")


class HomePageTests(SiteTestCase):
    def test_home_page_links_to_crawlable_year_pages(self):
        html = self.client.get("/").get_data(as_text=True)

        self.assertIn('href="/france/2030"', html)
        self.assertIn('href="/france/2026/school-holidays/C"', html)
        self.assertNotIn('href="/france/2030/school-holidays/C"', html)
        self.assertIn('id="calendar-days"', html)
        self.assertNotIn('aria-label="Année"', html)
        self.assertNotIn('id="year-select"', html)
        self.assertNotIn('id="zone-select"', html)
        self.assertIn('id="banner-prev-year"', html)
        self.assertIn('id="banner-next-year"', html)
        for key, pressed in (("public", "true"), ("A", "false"), ("B", "false"), ("C", "false")):
            self.assertIn(f'data-filter-toggle="{key}" aria-pressed="{pressed}"', html)

    def test_school_holidays_api_includes_autumn_and_christmas_across_years(self):
        for zone in "ABC":
            starts_2026 = [e["start"] for e in self.client.get(f"/api/school-holidays/FR/2026?zone={zone}").get_json()]
            self.assertIn("2026-10-17", starts_2026)
            self.assertIn("2026-12-19", starts_2026)
            self.assertIn("2025-12-20", starts_2026)

        events_2027 = self.client.get("/api/school-holidays/FR/2027?zone=A").get_json()
        self.assertIn(("2026-12-19", "2027-01-03"), [(e["start"], e["end"]) for e in events_2027])
        self.assertEqual(self.client.get("/api/school-holidays/FR/2028?zone=A").status_code, 400)

    def test_school_holidays_api_exposes_zone_for_colour_bands(self):
        events = self.client.get("/api/school-holidays/FR/2026?zone=B").get_json()

        self.assertTrue(events)
        self.assertTrue(all(e["zone"] == "B" and e["holidayType"] == "school" for e in events))


if __name__ == "__main__":
    unittest.main()
