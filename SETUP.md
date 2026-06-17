# Flask Holiday Calendar - Setup Instructions

## Prerequisites
- Python 3.11 or higher installed on your system

## Setup Commands

### 1. Create Virtual Environment
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
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

## Next Steps

Once dependencies are installed, you can:
1. Create `app.py` with your Flask application
2. Start the development server with `flask run`
3. Build out your holiday calendar features
