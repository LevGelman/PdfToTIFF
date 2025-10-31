#!/bin/bash

# Setup script for PDF to TIFF Converter
# This script sets up the Python virtual environment and installs all dependencies

set -e  # Exit on error

echo "=================================================="
echo "PDF to TIFF Converter - Environment Setup"
echo "=================================================="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check for poppler-utils
echo
echo "Checking system dependencies..."
if command -v pdfinfo &> /dev/null; then
    echo "✓ poppler-utils is installed: $(pdfinfo -v | head -n 1)"
else
    echo "⚠️  poppler-utils is NOT installed"
    echo
    echo "To install poppler-utils:"
    echo "  Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "  macOS: brew install poppler"
    echo "  Fedora: sudo dnf install poppler-utils"
fi

# Run tests
echo
echo "Running tests..."
python test_local.py

echo
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo
echo "To run the application:"
echo "  python app.py"
echo
echo "Then visit: http://localhost:5000"
echo
