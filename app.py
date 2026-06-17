from flask import Flask, render_template, jsonify
import holidays

app = Flask(__name__)

# Mapping of country codes to human-readable country names
COUNTRY_NAMES = {
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
    supported_countries = holidays.list_supported_countries()
    
    if country_code not in supported_countries:
        return jsonify({'error': f'Invalid country code: {country_code}'}), 400
    
    if year < 1900 or year > 2200:
        return jsonify({'error': 'Year must be between 1900 and 2200'}), 400
    
    try:
        country_holidays = holidays.country_holidays(country_code, years=year)
        
        events = []
        for date, holiday_name in sorted(country_holidays.items()):
            events.append({
                'title': holiday_name,
                'start': date.strftime('%Y-%m-%d')
            })
        
        return jsonify(events)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve holidays: {str(e)}'}), 400


if __name__ == '__main__':
    app.run(debug=True)
