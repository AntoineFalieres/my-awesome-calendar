from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, abort, Response
import hmac
import json
import os
import re
import time
from datetime import date, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from xml.sax.saxutils import escape as xml_escape

import holidays
from holidays.registry import COUNTRIES as HOLIDAY_COUNTRIES

app = Flask(__name__)
NAGER_PUBLIC_HOLIDAYS_API = "https://date.nager.at/api/v3/PublicHolidays/{year}/FR"
FR_NAME_DAYS_SOURCE_URL = (
    "https://raw.githubusercontent.com/xnekv03/nameday-api/"
    "8b1c18b8e0914c75bd8f0aa096b958755ac3e200/json/namedays.json"
)
FR_PUBLIC_HOLIDAYS_CACHE = {}
FR_NAMEDAYS_CACHE = {}
FR_NAME_DAYS_SOURCE_CACHE = None
REVENUE_EVENT_COUNTS = {}
FRANCE_SEO_YEARS = tuple(range(2025, 2031))
SITE_NAME = "Calendrier France"
SITE_URL = os.getenv("SITE_URL", "").rstrip("/")
APP_ENV = os.getenv("APP_ENV", "development").lower()
ADSENSE_CLIENT_ID = os.getenv("ADSENSE_CLIENT_ID", "ca-pub-XXXXXXXXXXXXXXXX")
ADSENSE_SLOT_INLINE = os.getenv("ADSENSE_SLOT_INLINE", "2222222222")
ADSENSE_SLOT_FOOTER = os.getenv("ADSENSE_SLOT_FOOTER", "3333333333")
# Script URL of the certified TCF consent management platform (CMP).
CMP_SCRIPT_URL = os.getenv("CMP_SCRIPT_URL", "")
METRICS_TOKEN = os.getenv("METRICS_TOKEN", "")
METRICS_RATE_LIMIT = 60
METRICS_RATE_WINDOW_SECONDS = 60
METRICS_MAX_DISTINCT_KEYS = 500
METRICS_FIELD_MAX_LENGTH = 64
METRICS_EVENT_TYPES = {"page_view", "ad_init"}
METRICS_STATUSES = {"viewed", "success", "failed", "none"}
METRICS_REQUEST_LOG = {}
ADS_TXT_PLACEHOLDER_MARKER = "XXXX"

# Mapping of country codes to human-readable country names

def _humanize_entity_name(entity_name):
    return re.sub(r"(?<!^)(?=[A-Z])", " ", entity_name)

AUTO_COUNTRY_NAMES = {
    code: _humanize_entity_name(entity_tuple[0])
    for entity_tuple in HOLIDAY_COUNTRIES.values()
    for code in entity_tuple[1:]
    if 2 <= len(code) <= 3
}

COUNTRY_NAMES = {
    **AUTO_COUNTRY_NAMES,
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AL': 'Albania', 'AM': 'Armenia',
    'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia',
    'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'BE': 'Belgium',
    'BG': 'Bulgaria', 'BN': 'Brunei', 'BO': 'Bolivia', 'BR': 'Brazil',
    'BS': 'Bahamas', 'BW': 'Botswana', 'BY': 'Belarus', 'BZ': 'Belize',
    'CA': 'Canada', 'CH': 'Switzerland', 'CL': 'Chile', 'CN': 'China',
    'CO': 'Colombia', 'CR': 'Costa Rica', 'CU': 'Cuba', 'CY': 'Cyprus',
    'CZ': 'Czechia', 'DE': 'Germany', 'DJ': 'Djibouti', 'DK': 'Denmark',
    'DO': 'Dominican Republic', 'DZ': 'Algeria', 'EC': 'Ecuador', 'EE': 'Estonia',
    'EG': 'Egypt', 'ES': 'Spain', 'ET': 'Ethiopia', 'FI': 'Finland',
    'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom', 'GE': 'Georgia',
    'GH': 'Ghana', 'GI': 'Gibraltar', 'GR': 'Greece', 'GT': 'Guatemala',
    'GY': 'Guyana', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HR': 'Croatia',
    'HT': 'Haiti', 'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland',
    'IL': 'Israel', 'IM': 'Isle of Man', 'IN': 'India', 'IS': 'Iceland',
    'IT': 'Italy', 'JE': 'Jersey', 'JM': 'Jamaica', 'JP': 'Japan',
    'KE': 'Kenya', 'KR': 'South Korea', 'KZ': 'Kazakhstan', 'LI': 'Liechtenstein',
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MA': 'Morocco',
    'MD': 'Moldova', 'MG': 'Madagascar', 'MH': 'Marshall Islands', 'MK': 'North Macedonia',
    'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 'NG': 'Nigeria',
    'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NZ': 'New Zealand',
    'PA': 'Panama', 'PE': 'Peru', 'PH': 'Philippines', 'PK': 'Pakistan',
    'PL': 'Poland', 'PT': 'Portugal', 'PY': 'Paraguay', 'RO': 'Romania',
    'RS': 'Serbia', 'RU': 'Russia', 'SA': 'Saudi Arabia', 'SE': 'Sweden',
    'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia', 'SN': 'Senegal',
    'TH': 'Thailand', 'TN': 'Tunisia', 'TR': 'Turkey', 'TW': 'Taiwan',
    'UA': 'Ukraine', 'US': 'United States', 'UY': 'Uruguay', 'VE': 'Venezuela',
    'VN': 'Vietnam', 'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe',
}

# French school holidays by zone: (first day off, last day off), source data.education.gouv.fr
FR_SCHOOL_HOLIDAYS_ZONES = {
    'A': [
        ('2025-02-22', '2025-03-09'),
        ('2025-04-19', '2025-05-04'),
        ('2025-07-05', '2025-08-31'),
        ('2025-10-18', '2025-11-02'),
        ('2025-12-20', '2026-01-04'),
        ('2026-02-07', '2026-02-22'),
        ('2026-04-04', '2026-04-19'),
        ('2026-07-04', '2026-08-31'),
        ('2026-10-17', '2026-11-01'),
        ('2026-12-19', '2027-01-03'),
        ('2027-02-13', '2027-02-28'),
        ('2027-04-10', '2027-04-25'),
        ('2027-07-03', '2027-09-01'),
    ],
    'B': [
        ('2025-02-08', '2025-02-23'),
        ('2025-04-05', '2025-04-21'),
        ('2025-07-05', '2025-08-31'),
        ('2025-10-18', '2025-11-02'),
        ('2025-12-20', '2026-01-04'),
        ('2026-02-14', '2026-03-01'),
        ('2026-04-11', '2026-04-26'),
        ('2026-07-04', '2026-08-31'),
        ('2026-10-17', '2026-11-01'),
        ('2026-12-19', '2027-01-03'),
        ('2027-02-20', '2027-03-07'),
        ('2027-04-17', '2027-05-02'),
        ('2027-07-03', '2027-09-01'),
    ],
    'C': [
        ('2025-02-15', '2025-03-02'),
        ('2025-04-12', '2025-04-27'),
        ('2025-07-05', '2025-08-31'),
        ('2025-10-18', '2025-11-02'),
        ('2025-12-20', '2026-01-04'),
        ('2026-02-21', '2026-03-08'),
        ('2026-04-18', '2026-05-03'),
        ('2026-07-04', '2026-08-31'),
        ('2026-10-17', '2026-11-01'),
        ('2026-12-19', '2027-01-03'),
        ('2027-02-06', '2027-02-21'),
        ('2027-04-03', '2027-04-18'),
        ('2027-07-03', '2027-09-01'),
    ],
}


def get_country_subdivisions(country_code):
    """Get subdivisions available for a country."""
    try:
        country_holidays = holidays.country_holidays(country_code, years=2026)
        if hasattr(country_holidays, 'subdivisions') and country_holidays.subdivisions:
            return dict(country_holidays.subdivisions)
        return {}
    except:
        return {}


def fetch_fr_public_holidays(year):
    """Fetch and normalize France public holidays from Nager.Date."""
    if year < 1900 or year > 2200:
        raise ValueError("Year must be between 1900 and 2200")

    cache_key = str(year)
    if cache_key in FR_PUBLIC_HOLIDAYS_CACHE:
        return FR_PUBLIC_HOLIDAYS_CACHE[cache_key]

    endpoint = NAGER_PUBLIC_HOLIDAYS_API.format(year=year)
    try:
        with urlopen(endpoint, timeout=10) as response:
            payload = response.read().decode("utf-8")
            upstream_holidays = json.loads(payload)
    except HTTPError as error:
        raise RuntimeError(f"Nager.Date returned HTTP {error.code}") from error
    except URLError as error:
        raise RuntimeError("Failed to reach Nager.Date API") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("Nager.Date returned invalid JSON payload") from error

    events = []
    for holiday in upstream_holidays:
        holiday_date = holiday.get("date")
        holiday_name = holiday.get("localName") or holiday.get("name")
        if not holiday_date or not holiday_name:
            continue

        events.append(
            {
                "title": holiday_name,
                "start": holiday_date,
                "holidayType": "public",
            }
        )

    FR_PUBLIC_HOLIDAYS_CACHE[cache_key] = events
    return events


def fetch_fr_name_days(year):
    """Return French name-day labels for every date in a year."""
    global FR_NAME_DAYS_SOURCE_CACHE

    if year < 1900 or year > 2200:
        raise ValueError("Year must be between 1900 and 2200")

    cache_key = str(year)
    if cache_key in FR_NAMEDAYS_CACHE:
        return FR_NAMEDAYS_CACHE[cache_key]

    if FR_NAME_DAYS_SOURCE_CACHE is None:
        try:
            with urlopen(FR_NAME_DAYS_SOURCE_URL, timeout=10) as response:
                payload = response.read().decode("utf-8")
            # The upstream calendar file contains JavaScript-style trailing commas.
            source_entries = json.loads(re.sub(r",\s*([}\]])", r"\1", payload))
        except HTTPError as error:
            raise RuntimeError(f"Name-day API returned HTTP {error.code}") from error
        except URLError as error:
            raise RuntimeError("Failed to reach the name-day API") from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise RuntimeError("Name-day API returned invalid JSON data") from error
        except TimeoutError as error:
            raise RuntimeError("Name-day API request timed out") from error

        if not isinstance(source_entries, list) or not source_entries:
            raise RuntimeError("Name-day API returned an invalid calendar")

        name_days = {}
        for entry in source_entries:
            if not isinstance(entry, dict):
                continue
            try:
                month = int(entry["month"])
                day = int(entry["day"])
                date(2000, month, day)
            except (KeyError, TypeError, ValueError):
                continue

            name = entry.get("fr")
            if isinstance(name, str) and name.strip().lower() != "n/a":
                name_days[(month, day)] = name.strip()

        if not name_days:
            raise RuntimeError("Name-day API returned no French name days")
        FR_NAME_DAYS_SOURCE_CACHE = name_days

    days = []
    current_day = date(year, 1, 1)
    last_day = date(year, 12, 31)
    while current_day <= last_day:
        days.append(
            {
                "date": current_day.isoformat(),
                "name": FR_NAME_DAYS_SOURCE_CACHE.get((current_day.month, current_day.day)),
            }
        )
        current_day += timedelta(days=1)

    FR_NAMEDAYS_CACHE[cache_key] = days
    return days


def is_placeholder_value(value):
    return not value or ADS_TXT_PLACEHOLDER_MARKER in value.upper()


def get_ad_config():
    """Return ad configuration for template rendering.

    Ads render only with a real AdSense client ID and a configured CMP, because
    ads must stay disabled until a consent signal can be honored.
    """
    return {
        "enabled": not is_placeholder_value(ADSENSE_CLIENT_ID) and bool(CMP_SCRIPT_URL),
        "client_id": ADSENSE_CLIENT_ID,
        "slot_inline": ADSENSE_SLOT_INLINE,
        "slot_footer": ADSENSE_SLOT_FOOTER,
    }


def validate_production_config():
    """Refuse to start in production with placeholder ad or consent settings."""
    if APP_ENV != "production":
        return

    problems = []
    if is_placeholder_value(ADSENSE_CLIENT_ID):
        problems.append("ADSENSE_CLIENT_ID is missing or a placeholder")
    if not CMP_SCRIPT_URL:
        problems.append("CMP_SCRIPT_URL is not set")
    if not SITE_URL:
        problems.append("SITE_URL is not set")
    try:
        with open(os.path.join(app.root_path, "ads.txt"), encoding="utf-8") as ads_file:
            if ADS_TXT_PLACEHOLDER_MARKER in ads_file.read().upper():
                problems.append("ads.txt still contains a placeholder publisher ID")
    except OSError:
        problems.append("ads.txt is missing")

    if problems:
        raise RuntimeError("Invalid production configuration: " + "; ".join(problems))


FR_WEEKDAYS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
FR_MONTHS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)
FR_SCHOOL_HOLIDAY_NAMES = {
    2: "Vacances d'hiver",
    4: "Vacances de printemps",
    7: "Vacances d'été",
    10: "Vacances de la Toussaint",
    12: "Vacances de Noël",
}


def format_french_date(value, with_weekday=True):
    """Format an ISO date string like 2026-01-01 as 'jeudi 1 janvier 2026'."""
    parsed = date.fromisoformat(value) if isinstance(value, str) else value
    label = f"{parsed.day}{'er' if parsed.day == 1 else ''} {FR_MONTHS[parsed.month - 1]} {parsed.year}"
    return f"{FR_WEEKDAYS[parsed.weekday()]} {label}" if with_weekday else label


app.add_template_filter(format_french_date, "fr_date")


def build_site_url(path):
    """Build an absolute URL, preferring the configured SITE_URL over the request host."""
    base = SITE_URL or request.url_root.rstrip("/")
    return f"{base}{path}"


def get_current_france_year():
    return min(max(date.today().year, FRANCE_SEO_YEARS[0]), FRANCE_SEO_YEARS[-1])


def get_school_holiday_years(zone="A"):
    """Return the SEO years that have school-holiday data."""
    return [
        year for year in FRANCE_SEO_YEARS
        if get_school_holiday_periods(year, zone)
    ]


def build_breadcrumb_jsonld(items):
    """Build BreadcrumbList JSON-LD from (name, path) pairs."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": position, "name": name, "item": build_site_url(path)}
            for position, (name, path) in enumerate(items, start=1)
        ],
    }


def build_events_jsonld(events):
    """Build Event JSON-LD for France holiday events."""
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Event",
                "name": event["name"],
                "startDate": event["start"],
                "endDate": event.get("end") or event["start"],
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": {
                    "@type": "Place",
                    "name": "France",
                    "address": {"@type": "PostalAddress", "addressCountry": "FR"},
                },
                "inLanguage": "fr",
            }
            for event in events
        ],
    }


@app.context_processor
def inject_site_context():
    return {
        "ad_config": get_ad_config(),
        "canonical_url": build_site_url(request.path),
        "site_name": SITE_NAME,
        "france_year": get_current_france_year(),
        "cmp_script_url": CMP_SCRIPT_URL,
    }


def get_school_holiday_periods(year, zone):
    """Return the (start, end) periods of a zone that overlap the given calendar year."""
    return [
        (start, end)
        for start, end in FR_SCHOOL_HOLIDAYS_ZONES.get(zone, [])
        if start[:4] <= str(year) <= end[:4]
    ]


def get_france_school_holidays_for_zone(year, zone):
    """Return normalized France school-holiday events for a specific zone and year."""
    periods = get_school_holiday_periods(year, zone)
    if not periods:
        raise ValueError(f"School holidays data not available for {year}")

    events = []
    for start_str, end_str in periods:
        events.append(
            {
                "title": f"School holidays (Zone {zone})",
                "start": start_str,
                "end": end_str,
                "backgroundColor": "#ff6b6b",
                "holidayType": "school",
                "zone": zone,
            }
        )
    return events


def get_supported_france_year(year):
    """Validate and normalize the year used by France SEO routes."""
    if year not in FRANCE_SEO_YEARS:
        abort(404)
    return year


def record_revenue_event(payload):
    """Track route/template-level revenue events by page type."""
    event_type = payload.get("eventType")
    page_type = payload.get("pageType")
    slot_name = payload.get("slot", "none")
    status = payload.get("status", "none")

    if event_type not in METRICS_EVENT_TYPES:
        raise ValueError("eventType is not supported")
    if status not in METRICS_STATUSES:
        raise ValueError("status is not supported")
    for field_name, value in (("pageType", page_type), ("slot", slot_name)):
        if (
            not isinstance(value, str)
            or not 0 < len(value) <= METRICS_FIELD_MAX_LENGTH
            or not re.fullmatch(r"[a-z0-9_-]+", value)
        ):
            raise ValueError(f"{field_name} is invalid")

    key = (page_type, event_type, slot_name, status)
    if key not in REVENUE_EVENT_COUNTS and len(REVENUE_EVENT_COUNTS) >= METRICS_MAX_DISTINCT_KEYS:
        raise ValueError("Too many distinct metric keys")
    REVENUE_EVENT_COUNTS[key] = REVENUE_EVENT_COUNTS.get(key, 0) + 1


def is_metrics_rate_limited(client_id):
    """Return True when a client exceeded the sliding-window metrics quota."""
    now = time.monotonic()
    if len(METRICS_REQUEST_LOG) > 10000:
        METRICS_REQUEST_LOG.clear()
    recent = [
        timestamp
        for timestamp in METRICS_REQUEST_LOG.get(client_id, [])
        if now - timestamp < METRICS_RATE_WINDOW_SECONDS
    ]
    if len(recent) >= METRICS_RATE_LIMIT:
        METRICS_REQUEST_LOG[client_id] = recent
        return True
    recent.append(now)
    METRICS_REQUEST_LOG[client_id] = recent
    return False


@app.route('/')
def index():
    """Serve the main index.html template."""
    return render_template(
        'index.html',
        page_type="calendar-home",
        current_year=get_current_france_year(),
        france_years=FRANCE_SEO_YEARS,
        school_years=get_school_holiday_years(),
    )


@app.route('/mentions-legales')
def mentions_legales():
    """Serve the Mentions Légales page."""
    return render_template('mentions_legales.html', page_type="legal-notice")


@app.route('/privacy-policy')
def privacy_policy():
    """Serve the Privacy Policy page."""
    return render_template('privacy_policy.html', page_type="privacy-policy")


@app.route('/france')
def france_root():
    """Redirect to the current year France landing page."""
    return redirect(url_for('france_year_landing', year=get_current_france_year()))


@app.route('/france/<int:year>')
def france_year_landing(year):
    """Render a crawlable France year landing page."""
    year = get_supported_france_year(year)
    year_links = [year_value for year_value in FRANCE_SEO_YEARS if year_value != year]
    return render_template(
        'france_year_landing.html',
        year=year,
        year_links=year_links,
        has_school_data=year in get_school_holiday_years(),
        page_type="france-year-landing",
        breadcrumb_jsonld=build_breadcrumb_jsonld(
            [("Accueil", "/"), (f"France {year}", f"/france/{year}")]
        ),
    )


@app.route('/france/<int:year>/public-holidays')
def france_public_holidays_page(year):
    """Render a server-side France public holidays page."""
    year = get_supported_france_year(year)
    error_message = None
    public_holidays = []
    try:
        public_holidays = fetch_fr_public_holidays(year)
    except RuntimeError as error:
        error_message = str(error)

    response = Response(
        render_template(
            'france_public_holidays.html',
            year=year,
            public_holidays=public_holidays,
            error_message=error_message,
            page_type="france-public-holidays",
            breadcrumb_jsonld=build_breadcrumb_jsonld(
                [
                    ("Accueil", "/"),
                    (f"France {year}", f"/france/{year}"),
                    ("Jours fériés", f"/france/{year}/public-holidays"),
                ]
            ),
            events_jsonld=build_events_jsonld(
                [{"name": holiday["title"], "start": holiday["start"]} for holiday in public_holidays]
            ) if public_holidays else None,
        )
    )
    if error_message:
        response.status_code = 503
    return response


@app.route('/france/<int:year>/school-holidays/<zone>')
def france_school_holidays_page(year, zone):
    """Render a server-side France school holidays page for one zone."""
    year = get_supported_france_year(year)
    if zone != zone.upper():
        return redirect(url_for('france_school_holidays_page', year=year, zone=zone.upper()), code=301)
    if zone not in {'A', 'B', 'C'}:
        abort(404)

    try:
        school_holidays = get_france_school_holidays_for_zone(year, zone)
    except ValueError:
        abort(404)

    periods = [
        {
            "name": FR_SCHOOL_HOLIDAY_NAMES.get(
                date.fromisoformat(holiday["start"]).month, "Vacances scolaires"
            ),
            "start": holiday["start"],
            "end": holiday["end"],
        }
        for holiday in school_holidays
    ]

    return render_template(
        'france_school_holidays.html',
        year=year,
        zone=zone,
        periods=periods,
        school_years=get_school_holiday_years(zone),
        page_type="france-school-holidays",
        breadcrumb_jsonld=build_breadcrumb_jsonld(
            [
                ("Accueil", "/"),
                (f"France {year}", f"/france/{year}"),
                (f"Zone {zone}", f"/france/{year}/school-holidays/{zone}"),
            ]
        ),
        events_jsonld=build_events_jsonld(
            [
                {
                    "name": f"{period['name']} {year} – zone {zone}",
                    "start": period["start"],
                    "end": period["end"],
                }
                for period in periods
            ]
        ),
    )


@app.route('/ads.txt')
def ads_txt():
    """Serve ads.txt from the repository root."""
    return send_from_directory(app.root_path, 'ads.txt', mimetype='text/plain')


@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt that keeps the JSON API out of search indexes."""
    body = "User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: " + build_site_url("/sitemap.xml") + "\n"
    return Response(body, mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap_xml():
    """Serve a sitemap of every crawlable page that has real content."""
    paths = ["/", "/mentions-legales", "/privacy-policy"]
    for year in FRANCE_SEO_YEARS:
        paths.append(f"/france/{year}")
        paths.append(f"/france/{year}/public-holidays")
    for zone in ("A", "B", "C"):
        for year in get_school_holiday_years(zone):
            paths.append(f"/france/{year}/school-holidays/{zone}")

    urls = "".join(f"<url><loc>{xml_escape(build_site_url(path))}</loc></url>" for path in paths)
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>"
    )
    return Response(body, mimetype='application/xml')


@app.route('/api/countries')
def get_countries():
    """Return all supported countries with their names."""
    supported_countries = holidays.list_supported_countries()
    
    countries_dict = {}
    for country_code in supported_countries:
        country_name = COUNTRY_NAMES.get(country_code, country_code)
        countries_dict[country_code] = country_name
    
    return jsonify(countries_dict)


@app.route('/api/subdivisions/<country_code>')
def get_subdivisions(country_code):
    """Return available subdivisions for a country."""
    supported_countries = holidays.list_supported_countries()
    
    if country_code not in supported_countries:
        return jsonify({'error': f'Invalid country code: {country_code}'}), 400
    
    subdivisions = get_country_subdivisions(country_code)
    return jsonify(subdivisions)


@app.route('/api/holidays/<country_code>/<int:year>')
def get_holidays(country_code, year):
    """Return holidays for a specific country and year in FullCalendar.js format."""
    subdiv = request.args.get('subdiv')
    supported_countries = holidays.list_supported_countries()
    
    if country_code not in supported_countries:
        return jsonify({'error': f'Invalid country code: {country_code}'}), 400
    
    if year < 1900 or year > 2200:
        return jsonify({'error': 'Year must be between 1900 and 2200'}), 400
    
    try:
        kwargs = {'years': year}
        if subdiv:
            kwargs['subdiv'] = subdiv
        
        country_holidays = holidays.country_holidays(country_code, **kwargs)
        
        events = []
        for holiday_date_obj, holiday_name in sorted(country_holidays.items()):
            events.append({
                'title': holiday_name,
                'start': holiday_date_obj.strftime('%Y-%m-%d')
            })
        
        return jsonify(events)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve holidays: {str(e)}'}), 400


@app.route('/api/holidays/france/<int:year>')
def get_france_holidays(year):
    """Return France public holidays from Nager.Date in FullCalendar format."""
    try:
        return jsonify(fetch_fr_public_holidays(year))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except RuntimeError as error:
        return jsonify({'error': str(error)}), 502


@app.route('/api/name-days/france/<int:year>')
def get_france_name_days(year):
    """Return French name-day labels for a calendar year."""
    try:
        return jsonify(fetch_fr_name_days(year))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except RuntimeError as error:
        return jsonify({'error': str(error)}), 502


@app.route('/api/school-holidays/<country_code>/<int:year>')
def get_school_holidays(country_code, year):
    """Return school holidays for a country and year."""
    zone = request.args.get('zone', 'A')
    
    if country_code != 'FR':
        return jsonify({'error': 'School holidays only available for France'}), 400
    
    if zone not in ['A', 'B', 'C']:
        return jsonify({'error': 'Zone must be A, B, or C'}), 400
    
    try:
        return jsonify(get_france_school_holidays_for_zone(year, zone))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@app.route('/api/metrics/revenue', methods=['POST'])
def track_revenue_event():
    """Collect route/template-level revenue tracking events."""
    if is_metrics_rate_limited(request.remote_addr or "unknown"):
        return jsonify({'error': 'Too many requests'}), 429

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        record_revenue_event(payload)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400

    return jsonify({'status': 'accepted'}), 202


@app.route('/api/metrics/revenue/summary')
def revenue_summary():
    """Expose in-memory revenue event counters for diagnostics, behind METRICS_TOKEN."""
    provided_token = request.headers.get('X-Metrics-Token', '')
    if not METRICS_TOKEN or not hmac.compare_digest(provided_token, METRICS_TOKEN):
        abort(404)

    summary = []
    for (page_type, event_type, slot_name, status), count in sorted(REVENUE_EVENT_COUNTS.items()):
        summary.append(
            {
                'pageType': page_type,
                'eventType': event_type,
                'slot': slot_name,
                'status': status,
                'count': count,
            }
        )
    return jsonify(summary)


validate_production_config()


if __name__ == '__main__':
    app.run(debug=True)
