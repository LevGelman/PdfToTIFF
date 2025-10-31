#!/usr/bin/env python3
"""
Quick test script to verify the application is working correctly
Run this before deploying to Azure
"""

import sys
import subprocess

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} - installed")
        return True
    except ImportError:
        print(f"✗ {package_name} - NOT installed")
        return False

def check_poppler():
    """Check if poppler is installed"""
    print("\nChecking system dependencies...")
    try:
        result = subprocess.run(['pdfinfo', '-v'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print("✓ poppler-utils - installed")
            return True
        else:
            print("✗ poppler-utils - NOT installed")
            return False
    except FileNotFoundError:
        print("✗ poppler-utils - NOT installed")
        print("  Install with:")
        print("    Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("    macOS: brew install poppler")
        return False
    except Exception as e:
        print(f"✗ Error checking poppler: {e}")
        return False

def check_flask_app():
    """Check if Flask app can be imported"""
    print("\nChecking Flask application...")
    try:
        import app
        print("✓ app.py - can be imported")
        if hasattr(app, 'app'):
            print("✓ Flask app object - found")
            return True
        else:
            print("✗ Flask app object - NOT found")
            return False
    except Exception as e:
        print(f"✗ Error importing app: {e}")
        return False

def main():
    print("=" * 50)
    print("PDF to TIFF Converter - Local Test")
    print("=" * 50)
    print()

    results = []

    # Check Python version
    results.append(check_python_version())

    # Check required packages
    print("\nChecking Python packages...")
    packages = ['flask', 'pdf2image', 'PIL', 'werkzeug']
    for package in packages:
        results.append(check_package(package))

    # Check poppler
    results.append(check_poppler())

    # Check Flask app
    results.append(check_flask_app())

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if all(results):
        print("\n✓ All checks passed! You're ready to run the app.")
        print("\nRun the app with:")
        print("  python app.py")
        print("\nThen visit: http://localhost:5000")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
