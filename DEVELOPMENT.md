# Development Guide

This guide covers local development setup and workflows for the PDF to TIFF Converter project.

## Quick Setup

### Automatic Setup (Recommended)
```bash
./setup_venv.sh
```

This script will:
- Create the virtual environment
- Install all dependencies
- Check system requirements
- Run tests

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install system dependency
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler

# Run tests
python test_local.py
```

## Development Workflow

### 1. Activate Virtual Environment

Always activate the virtual environment before working:

```bash
source .venv/bin/activate
```

You'll see `(.venv)` in your terminal prompt.

### 2. Run the Application

#### Development Mode (with auto-reload)
```bash
python app.py
```

The app will run on http://localhost:5000 with debug mode enabled.

#### Production Mode (with Gunicorn)
```bash
gunicorn --bind 0.0.0.0:8000 --timeout 600 --workers 2 app:app
```

### 3. Testing Changes

#### Quick Test
```bash
python test_local.py
```

#### Manual Testing
1. Run the app: `python app.py`
2. Open http://localhost:5000
3. Upload test PDF files
4. Verify TIFF download works

## VS Code Setup

### First Time
1. Open project in VS Code
2. Install recommended extensions when prompted
3. Select Python interpreter: `.venv/bin/python`

### Running/Debugging
- Press `F5` to start debugging
- Choose "Flask: Run Application"
- Set breakpoints by clicking left of line numbers

## Project Structure

```
PdfToTIFF/
├── app.py                    # Main Flask application
├── templates/
│   └── index.html           # Web interface
├── pdf_to_tiff.py           # CLI script (full version)
├── pdf_to_tiff_simple.py    # CLI script (simple)
├── test_local.py            # Testing script
├── requirements.txt          # Dependencies
├── setup_venv.sh            # Setup automation
├── .venv/                   # Virtual environment (gitignored)
├── .vscode/                 # VS Code settings
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
└── README.md                # Main documentation
```

## Common Development Tasks

### Adding New Dependencies

```bash
# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt
```

### Code Style

This project uses:
- **Indentation**: 4 spaces (not tabs)
- **Line length**: Soft limit at 79 chars, hard limit at 120
- **No OOP**: Functional/procedural programming only
- **Comments**: Docstrings for functions

Example:
```python
def convert_pdfs_to_tiff(pdf_files, output_path, dpi=200):
    """
    Convert multiple PDF files to a single multi-page TIFF

    Parameters:
        pdf_files: List of PDF file paths
        output_path: Path for output TIFF file
        dpi: Resolution for conversion

    Returns:
        Tuple of (success, message, page_count)
    """
    # Implementation here
    pass
```

## Environment Variables

### Development
```bash
export SECRET_KEY="dev-secret-key-change-in-production"
export FLASK_ENV="development"
export FLASK_DEBUG="1"
```

### Production
```bash
export SECRET_KEY="your-secure-random-key"
export FLASK_ENV="production"
export PORT="8000"
```

Generate secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Debugging Tips

### Application won't start
```bash
# Check if port is already in use
lsof -i :5000

# Kill process using port
kill -9 <PID>
```

### Import errors
```bash
# Verify virtual environment is activated
which python
# Should show: /path/to/project/.venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### PDF conversion fails
```bash
# Check poppler is installed
which pdfinfo
pdfinfo -v

# Test with small PDF first
# Check file permissions
ls -l your-file.pdf
```

### Memory errors
- Reduce DPI setting
- Process fewer/smaller PDFs
- Check available system memory: `free -h`

## Docker Development

### Build and run locally
```bash
docker-compose up --build
```

### Access logs
```bash
docker-compose logs -f
```

### Stop container
```bash
docker-compose down
```

## Testing Before Deployment

### 1. Run Local Tests
```bash
python test_local.py
```

### 2. Test with Sample PDFs
- Test single PDF
- Test multiple PDFs
- Test different DPI settings
- Test large files (~50MB)

### 3. Check Performance
- Monitor memory usage: `htop`
- Check conversion time
- Test concurrent uploads

### 4. Docker Test
```bash
docker-compose up
# Test on http://localhost:5000
```

## Git Workflow

### Before committing
```bash
# Check status
git status

# Add files
git add .

# Commit with message
git commit -m "Description of changes"
```

### Ignored files
The following are gitignored:
- `.venv/` - Virtual environment
- `*.pyc`, `__pycache__/` - Python cache
- `*.tiff`, `*.pdf` - Test files
- `*.log` - Log files

## Useful Commands

### Virtual Environment
```bash
# Activate
source .venv/bin/activate

# Deactivate
deactivate

# Delete and recreate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Flask
```bash
# Run with specific port
python app.py
# Edit PORT in app.py or:
export PORT=8080 && python app.py

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

### Package Management
```bash
# List installed packages
pip list

# Show package info
pip show flask

# Check outdated packages
pip list --outdated
```

## Troubleshooting

### Issue: VS Code not finding imports
**Solution**:
1. Ctrl+Shift+P → "Python: Select Interpreter"
2. Choose `.venv/bin/python`

### Issue: Port 5000 already in use
**Solution**:
```bash
# Find process
lsof -i :5000

# Kill it
kill -9 <PID>
```

### Issue: poppler not found
**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### Issue: Permission denied on .sh files
**Solution**:
```bash
chmod +x setup_venv.sh
chmod +x startup.sh
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pdf2image Documentation](https://github.com/Belval/pdf2image)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## Getting Help

1. Check this guide
2. Review [README.md](README.md)
3. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
4. Run `python test_local.py` to diagnose problems
