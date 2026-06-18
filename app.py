from flask import Flask, render_template, jsonify
import re

import holidays
from holidays.registry import COUNTRIES as HOLIDAY_COUNTRIES

app = Flask(__name__)

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


@app.route('/')
def index():
    """Serve the main index.html template."""
    return render_template('index.html')




# French school holidays by zone (https://www.education.gouv.fr/calendrier-scolaire)
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

@app.route('/api/countries')
def get_countries():
    """Return all supported countries with their names."""
    supported_countries = holidays.list_supported_countries()
    
    countries_dict = {}
    for country_code in supported_countries:
        country_name = COUNTRY_NAMES.get(country_code, country_code)
        countries_dict[country_code] = country_name
    
    return jsonify(countries_dict)


@app.route('/api/holidays/<country_code>/<int:year>')
def get_holidays(country_code, year):
    """Return holidays for a specific country and year in FullCalendar.js format."""
    from flask import request
    subdiv = request.args.get('subdiv')
    
    supported_countries = holidays.list_supported_countries()
    
    if country_code not in supported_countries:
        return jsonify({'error': f'Invalid country code: {country_code}'}), 400
    
    if year < 1900 or year > 2200:
        return jsonify({'error': 'Year must be between 1900 and 2200'}), 400
    
    try:
        country_holidays = holidays.country_holidays(country_code, years=year, subdiv=subdiv)
        
        events = []
        for holiday_date, holiday_name in sorted(country_holidays.items()):
            events.append({
                'title': holiday_name,
                'start': holiday_date.strftime('%Y-%m-%d')
            })
        
        return jsonify(events)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve holidays: {str(e)}'}), 400

@app.route('/api/school-holidays/<country_code>/<int:year>')
def get_school_holidays(country_code, year):
    """Return school holidays for a country and year."""
    from flask import request
    zone = request.args.get('zone', 'A')
    
    if country_code != 'FR':
        return jsonify({'error': 'School holidays only available for France'}), 400
    
    if zone not in ['A', 'B', 'C']:
        return jsonify({'error': 'Zone must be A, B, or C'}), 400
    
    year_str = str(year)
    if year_str not in FR_SCHOOL_HOLIDAYS_ZONES.get(zone, {}):
        return jsonify({'error': f'School holidays data not available for {year}'}), 400
    
    events = []
    for start_str, end_str in FR_SCHOOL_HOLIDAYS_ZONES[zone][year_str]:
        start_date = date.fromisoformat(start_str)
        end_date = date.fromisoformat(end_str)
        # Create a single event with duration or add daily events
        events.append({
            'title': f'School holidays (Zone {zone})',
            'start': start_str,
            'end': end_str,
            'backgroundColor': '#ff6b6b'
        })
    
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True)