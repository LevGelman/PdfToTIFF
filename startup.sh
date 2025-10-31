#!/bin/bash

# Azure Web App startup script for PDF to TIFF Converter

echo "Installing system dependencies..."
apt-get update
apt-get install -y poppler-utils

echo "Starting Gunicorn server..."
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 app:app
