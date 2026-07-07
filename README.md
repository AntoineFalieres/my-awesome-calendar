# 🗓️ My Awesome Calendar

A comprehensive, interactive holiday and school calendar application that displays public holidays and regional school holidays for 200+ countries and their subdivisions.

## ✨ Features

- 🌍 **200+ Countries Supported** - View public holidays for countries worldwide
- 🗺️ **Regional Subdivisions** - Select state/province/regional holidays (US states, Canadian provinces, German Bundesländer, etc.)
- 🏫 **French School Holidays** - Dedicated support for French school holidays by zone (A, B, C)
- 📅 **Flexible Views** - Switch between Month and Week calendar views
- 🌞 **Monday Start** - Calendar weeks start on Monday
- ⚡ **Real-time Updates** - Dynamically load holidays based on country/region/year selection
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Bootstrap Styling** - Clean, modern UI with Bootstrap 5

## 🚀 Quick Start

### Requirements
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AntoineFalieres/my-awesome-calendar.git
   cd my-awesome-calendar
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python3 app.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:5000`

## 📖 Usage

### Basic Workflow

1. **Select a Country** - Choose from the dropdown list (200+ countries)
2. **Choose a Year** - Select the year (2020-2030 by default)
3. **Pick a Subdivision** (if available) - For countries with regions:
   - **France**: Select Zone A, B, or C for school holidays
   - **US**: Select a state (CA, NY, TX, etc.)
   - **Canada**: Select a province (ON, QC, BC, etc.)
   - **Other countries**: Select your region to filter holidays
4. **View Calendar** - Holidays appear marked on the calendar
5. **Switch Views** - Use Month/Week buttons in the toolbar

### Calendar Features

- **Month View**: Overview of all holidays in a month
- **Week View**: Detailed daily breakdown of the week
- **Navigation**: Use Previous/Next buttons to move between periods
- **Today Button**: Jump back to current month/week

## 🔧 Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: FullCalendar.js v6.1.15
- **Styling**: Bootstrap 5.3.3
- **Holiday Data**: Python `holidays` library (200+ countries)
- **Database**: None (stateless, data-driven)

## 📚 API Documentation

### Endpoints

#### GET `/api/countries`
Returns all supported countries with their names.

**Response:**
```json
{
  "US": "United States",
  "CA": "Canada",
  "FR": "France",
  ...
}
```

#### GET `/api/subdivisions/<country_code>`
Returns available subdivisions for a country (states, provinces, etc.).

**Example:** `GET /api/subdivisions/US`

**Response:**
```json
{
  "AL": "Alabama",
  "AK": "Alaska",
  "AZ": "Arizona",
  ...
}
```

#### GET `/api/holidays/<country_code>/<year>`
Returns public holidays for a country and year. Optionally filter by subdivision.

**Parameters:**
- `country_code` (required): 2-3 letter country code (e.g., "US", "FR")
- `year` (required): Year (1900-2200)
- `subdiv` (optional): Subdivision code (state, province, etc.)

**Example:** `GET /api/holidays/US/2026?subdiv=CA`

**Response:**
```json
[
  {
    "title": "New Year's Day",
    "start": "2026-01-01"
  },
  {
    "title": "Independence Day",
    "start": "2026-07-04"
  },
  ...
]
```

#### GET `/api/school-holidays/<country_code>/<year>`
Returns school holidays for France by zone.

**Parameters:**
- `country_code` (required): Must be "FR" (France only)
- `year` (required): Year (2025-2026 supported)
- `zone` (optional): Zone A, B, or C (default: A)

**Example:** `GET /api/school-holidays/FR/2026?zone=A`

**Response:**
```json
[
  {
    "title": "School holidays (Zone A)",
    "start": "2026-02-14",
    "end": "2026-03-02",
    "backgroundColor": "#ff6b6b"
  },
  ...
]
```

#### GET `/mentions-legales`
Returns the legal notice page with production-ready metadata/content.

#### GET `/privacy-policy`
Returns the privacy policy page with production-ready metadata/content.

#### GET `/france`
Redirects to the current year France landing page.

#### GET `/france/<year>`
Returns a server-rendered SEO landing page for the selected France year.

#### GET `/france/<year>/public-holidays`
Returns a server-rendered list page of France public holidays for the selected year.

#### GET `/france/<year>/school-holidays/<zone>`
Returns a server-rendered list page of school holidays for zone `A`, `B`, or `C`.

#### POST `/api/metrics/revenue`
Collects page-type and ad initialization revenue tracking events.

#### GET `/api/metrics/revenue/summary`
Returns in-memory aggregated revenue tracking counters.

## ⚙️ Ad Configuration

AdSense values are now environment-driven:

- `ADSENSE_CLIENT_ID` (example: `ca-pub-1234567890`)
- `ADSENSE_SLOT_HEADER`
- `ADSENSE_SLOT_INLINE`
- `ADSENSE_SLOT_FOOTER`

If not provided, safe placeholder defaults are used.

## 🤖 Planning Docs Automation

Merged pull requests can automatically update managed sections in:

- `ROADMAP.md`
- `TODO.md`
- `CHANGELOG.md`

Automation uses deterministic role ownership tags (`PM`, `SEO`, `UX/UI`,
`Full-Stack`, `Ad Ops`) from merged PR metadata and opens a dedicated follow-up
PR with only generated doc updates.

Manual trigger is available via GitHub Actions workflow:

- `Roadmap/TODO/Changelog Auto Update`

## 🗃️ Project Structure

```
my-awesome-calendar/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   ├── index.html        # Main frontend (FullCalendar + Bootstrap)
│   ├── mentions_legales.html       # Legal notice page
│   ├── privacy_policy.html         # Privacy policy page
│   ├── france_year_landing.html    # France yearly SEO landing page
│   ├── france_public_holidays.html # France public holidays SEO page
│   └── france_school_holidays.html # France school holidays SEO page
└── SETUP.md             # Detailed setup instructions
```

## 🇫🇷 French School Holidays - Zone Information

France divides school holidays into 3 zones to stagger vacations:

- **Zone A**: Regions like Burgundy, Brittany, Normandy, etc.
- **Zone B**: Regions like Ile-de-France, Corsica, etc.
- **Zone C**: Regions like Provence-Alpes, Côte d'Azur, etc.

Each zone has different vacation dates for:
- Winter holidays (February)
- Spring holidays (April)
- Summer holidays (July-August)

## 🌍 Supported Countries by Region

### Europe
France, Germany, Italy, Spain, UK, Poland, Netherlands, Belgium, Switzerland, Austria, Sweden, Norway, Denmark, Finland, and 50+ more

### Americas
United States, Canada, Mexico, Brazil, Argentina, Chile, Colombia, and 20+ more

### Asia-Pacific
Japan, China, India, Australia, New Zealand, South Korea, Singapore, Thailand, and 30+ more

### Africa
South Africa, Egypt, Kenya, Nigeria, Ghana, and 20+ more

### Middle East
Saudi Arabia, United Arab Emirates, Israel, Turkey, and 10+ more

*For complete list, run the application and check the country dropdown.*

## 🔄 Calendar Updates

The holiday data is automatically fetched from the `holidays` Python library, which is regularly updated to reflect:
- New public holidays
- Holiday changes by country
- Daylight saving time adjustments

To update the library:
```bash
pip install --upgrade holidays
```

## 🛠️ Development

### Running in Debug Mode
The app runs in Flask's debug mode by default, which provides:
- Auto-reload on file changes
- Interactive debugger
- Detailed error pages

### Extending the Application

To add more features:

1. **Add new API endpoints** in `app.py`
2. **Update the UI** in `templates/index.html`
3. **Add new styles** in the `<style>` section

### Adding More Years for French School Holidays

Edit the `FR_SCHOOL_HOLIDAYS_ZONES` dictionary in `app.py` to add more years.

## 📝 License

Licensed under the MIT License. See `LICENSE` file for details.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues or questions:
- Check existing GitHub issues
- Open a new issue with detailed description
- Include your browser console logs if it's a frontend issue

## 🎯 Roadmap

- [ ] Add more school holiday zones for other countries
- [ ] Export calendar to iCal format
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Advanced filtering (holiday type, religious holidays, etc.)
- [ ] Calendar sharing functionality
- [ ] Mobile app version

## 🎉 Acknowledgments

- [FullCalendar.js](https://fullcalendar.io/) - Calendar display
- [Python holidays](https://github.com/vacanza/python-holidays) - Holiday data
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Flask](https://flask.palletsprojects.com/) - Web framework
