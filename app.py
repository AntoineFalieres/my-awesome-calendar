from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, abort
import json
import os
import re
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import holidays
from holidays.registry import COUNTRIES as HOLIDAY_COUNTRIES

app = Flask(__name__)
NAGER_PUBLIC_HOLIDAYS_API = "https://date.nager.at/api/v3/PublicHolidays/{year}/FR"
FR_PUBLIC_HOLIDAYS_CACHE = {}
REVENUE_EVENT_COUNTS = {}
FRANCE_SEO_YEARS = tuple(range(2025, 2031))
ADSENSE_CLIENT_ID = os.getenv("ADSENSE_CLIENT_ID", "ca-pub-XXXXXXXXXXXXXXXX")
ADSENSE_SLOT_HEADER = os.getenv("ADSENSE_SLOT_HEADER", "1111111111")
ADSENSE_SLOT_INLINE = os.getenv("ADSENSE_SLOT_INLINE", "2222222222")
ADSENSE_SLOT_FOOTER = os.getenv("ADSENSE_SLOT_FOOTER", "3333333333")

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

# French school holidays by zone
FR_SCHOOL_HOLIDAYS_ZONES = {
    'A': {
        '2025': [
            ('2025-02-15', '2025-03-03'),
            ('2025-04-12', '2025-04-28'),
            ('2025-07-06', '2025-09-01'),
        ],
        '2026': [
            ('2026-02-14', '2026-03-02'),
            ('2026-04-11', '2026-04-27'),
            ('2026-07-05', '2026-08-31'),
        ],
    },
    'B': {
        '2025': [
            ('2025-02-01', '2025-02-17'),
            ('2025-04-05', '2025-04-21'),
            ('2025-07-06', '2025-09-01'),
        ],
        '2026': [
            ('2026-02-07', '2026-02-23'),
            ('2026-04-04', '2026-04-20'),
            ('2026-07-05', '2026-08-31'),
        ],
    },
    'C': {
        '2025': [
            ('2025-02-08', '2025-02-24'),
            ('2025-04-19', '2025-05-05'),
            ('2025-07-06', '2025-09-01'),
        ],
        '2026': [
            ('2026-02-21', '2026-03-09'),
            ('2026-04-18', '2026-05-04'),
            ('2026-07-05', '2026-08-31'),
        ],
    },
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


def get_ad_config():
    """Return ad configuration for template rendering."""
    return {
        "client_id": ADSENSE_CLIENT_ID,
        "slot_header": ADSENSE_SLOT_HEADER,
        "slot_inline": ADSENSE_SLOT_INLINE,
        "slot_footer": ADSENSE_SLOT_FOOTER,
    }


def get_france_school_holidays_for_zone(year, zone):
    """Return normalized France school-holiday events for a specific zone and year."""
    year_str = str(year)
    if year_str not in FR_SCHOOL_HOLIDAYS_ZONES.get(zone, {}):
        raise ValueError(f"School holidays data not available for {year}")

    events = []
    for start_str, end_str in FR_SCHOOL_HOLIDAYS_ZONES[zone][year_str]:
        events.append(
            {
                "title": f"School holidays (Zone {zone})",
                "start": start_str,
                "end": end_str,
                "backgroundColor": "#ff6b6b",
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

    if not isinstance(event_type, str) or not event_type.strip():
        raise ValueError("eventType must be a non-empty string")
    if not isinstance(page_type, str) or not page_type.strip():
        raise ValueError("pageType must be a non-empty string")

    key = (page_type.strip(), event_type.strip(), str(slot_name), str(status))
    REVENUE_EVENT_COUNTS[key] = REVENUE_EVENT_COUNTS.get(key, 0) + 1


@app.route('/')
def index():
    """Serve the main index.html template."""
    current_year = min(max(date.today().year, FRANCE_SEO_YEARS[0]), FRANCE_SEO_YEARS[-1])
    return render_template(
        'index.html',
        ad_config=get_ad_config(),
        page_type="calendar-home",
        canonical_url=request.base_url,
        current_year=current_year,
    )


@app.route('/mentions-legales')
def mentions_legales():
    """Serve the Mentions Légales page."""
    return render_template(
        'mentions_legales.html',
        ad_config=get_ad_config(),
        page_type="legal-notice",
        canonical_url=request.base_url,
    )


@app.route('/privacy-policy')
def privacy_policy():
    """Serve the Privacy Policy page."""
    return render_template(
        'privacy_policy.html',
        ad_config=get_ad_config(),
        page_type="privacy-policy",
        canonical_url=request.base_url,
    )


@app.route('/france')
def france_root():
    """Redirect to the current year France landing page."""
    current_year = min(max(date.today().year, FRANCE_SEO_YEARS[0]), FRANCE_SEO_YEARS[-1])
    return redirect(url_for('france_year_landing', year=current_year))


@app.route('/france/<int:year>')
def france_year_landing(year):
    """Render a crawlable France year landing page."""
    year = get_supported_france_year(year)
    year_links = [year_value for year_value in FRANCE_SEO_YEARS if year_value != year]
    return render_template(
        'france_year_landing.html',
        year=year,
        year_links=year_links,
        canonical_url=request.base_url,
        page_type="france-year-landing",
        ad_config=get_ad_config(),
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

    return render_template(
        'france_public_holidays.html',
        year=year,
        public_holidays=public_holidays,
        error_message=error_message,
        canonical_url=request.base_url,
        page_type="france-public-holidays",
        ad_config=get_ad_config(),
    )


@app.route('/france/<int:year>/school-holidays/<zone>')
def france_school_holidays_page(year, zone):
    """Render a server-side France school holidays page for one zone."""
    year = get_supported_france_year(year)
    zone = zone.upper()
    if zone not in {'A', 'B', 'C'}:
        abort(404)

    error_message = None
    school_holidays = []
    try:
        school_holidays = get_france_school_holidays_for_zone(year, zone)
    except ValueError as error:
        error_message = str(error)

    return render_template(
        'france_school_holidays.html',
        year=year,
        zone=zone,
        school_holidays=school_holidays,
        error_message=error_message,
        canonical_url=request.base_url,
        page_type="france-school-holidays",
        ad_config=get_ad_config(),
    )


@app.route('/ads.txt')
def ads_txt():
    """Serve ads.txt from the repository root."""
    return send_from_directory(app.root_path, 'ads.txt', mimetype='text/plain')


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
    """Expose in-memory revenue event counters for diagnostics."""
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


if __name__ == '__main__':
    app.run(debug=True)
