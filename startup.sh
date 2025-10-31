#!/bin/bash
set -euo pipefail

LOG_PREFIX="[startup]"

echo "$LOG_PREFIX booting..."

if command -v pdfinfo >/dev/null 2>&1; then
  echo "$LOG_PREFIX poppler already installed: $(pdfinfo -v 2>&1 | head -n 1)"
else
  echo "$LOG_PREFIX pdfinfo not found; attempting to install poppler-utils"
  if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y poppler-utils
    echo "$LOG_PREFIX poppler installed: $(pdfinfo -v 2>&1 | head -n 1)"
  else
    echo "$LOG_PREFIX apt-get not available; cannot install poppler-utils" >&2
  fi
fi

echo "$LOG_PREFIX starting Gunicorn server"
exec gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 app:app
