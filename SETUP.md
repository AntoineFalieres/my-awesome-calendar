# Flask Holiday Calendar - Setup Instructions

## Prerequisites
- Python 3.11 or higher installed on your system
- `uv` installed (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Setup Commands

### 1. Create Virtual Environment with uv
```bash
uv venv
```

### 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install -r requirements.txt
```

Or install all in one command:
```bash
uv sync
```

## Verification

To verify the installation was successful, run:
```bash
python -c "import flask; import holidays; print('Flask and holidays installed successfully!')"
```

## Deactivating Virtual Environment

When finished working on the project:
```bash
deactivate
```

## Running the Application

Once dependencies are installed, start the Flask development server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /` - Serve the holiday calendar UI
- `GET /api/countries` - Return all supported countries
- `GET /api/holidays/<country_code>/<year>` - Return holidays for a specific country and year
