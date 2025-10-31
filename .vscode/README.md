# VS Code Setup

This directory contains VS Code workspace settings for the PDF to TIFF Converter project.

## What's Configured

### Python Interpreter
- **Virtual Environment**: `.venv/bin/python`
- Automatically activates when you open a terminal in VS Code
- Python 3.8+ required

### Extensions Recommended
1. **Python** (ms-python.python)
2. **Pylance** (ms-python.vscode-pylance)
3. **Python Debugger** (ms-python.debugpy)

VS Code will prompt you to install these when you open the project.

## Launch Configurations

Three debug configurations are available (press F5 or go to Run & Debug):

1. **Flask: Run Application**
   - Runs the Flask app in debug mode with hot reload
   - Includes Jinja template debugging
   - URL: http://localhost:5000

2. **Python: Run app.py**
   - Direct execution of app.py
   - Good for testing without Flask CLI

3. **Python: Test Script**
   - Runs test_local.py to verify setup

## First Time Setup

If you haven't set up the virtual environment yet:

```bash
# Run the setup script
./setup_venv.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Using the Virtual Environment

VS Code will automatically detect and use the `.venv` virtual environment.

To manually activate in terminal:
```bash
source .venv/bin/activate
```

## Running the Application

### From VS Code
1. Press `F5` or click "Run and Debug"
2. Select "Flask: Run Application"
3. Open browser to http://localhost:5000

### From Terminal
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the app
python app.py
```

## Troubleshooting

### "Python interpreter not found"
1. Open Command Palette (Ctrl+Shift+P or Cmd+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose `.venv/bin/python`

### Dependencies not found
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### poppler-utils not installed
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

## File Structure

```
.vscode/
├── settings.json       # Workspace settings
├── launch.json         # Debug configurations
├── extensions.json     # Recommended extensions
└── README.md          # This file
```
