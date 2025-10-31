FROM python:3.11-slim

# Install system dependencies including poppler-utils
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY templates/ templates/

# Create temp directory with proper permissions
RUN mkdir -p /tmp && chmod 1777 /tmp

# Set environment variables
ENV FLASK_APP=app.py \
    PORT=8000 \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application with gunicorn
# Using 1 worker for free tier (512MB RAM) - change to 2 for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "--workers", "1", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
