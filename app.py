#!/usr/bin/env python3
"""
Flask Web Application for PDF to TIFF Conversion
Allows users to upload multiple PDF files and download a combined multi-page TIFF file
"""

import os
import glob
import tempfile
import shutil
import subprocess
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PIL import Image

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


def _resolve_poppler_path():
    """Return the directory containing poppler utilities, if it can be located."""
    env_path = os.environ.get("POPPLER_PATH")
    if env_path and os.path.exists(os.path.join(env_path, "pdfinfo")):
        return env_path

    for candidate in ("/usr/bin", "/usr/local/bin", "/opt/homebrew/bin"):
        if os.path.exists(os.path.join(candidate, "pdfinfo")):
            return candidate

    return None


POPPLER_PATH = _resolve_poppler_path()


def _log_poppler_version():
    """Log poppler availability to aid in deployment diagnostics."""
    pdfinfo_executable = "pdfinfo"
    if POPPLER_PATH:
        pdfinfo_executable = os.path.join(POPPLER_PATH, "pdfinfo")

    try:
        result = subprocess.run(
            [pdfinfo_executable, "-v"],
            check=False,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            message = result.stdout.strip() or result.stderr.strip() or "pdfinfo available"
            app.logger.info("Poppler detected: %s", message.splitlines()[0])
        else:
            stderr = result.stderr.strip() or result.stdout.strip() or "unknown error"
            app.logger.warning(
                "Poppler check returned non-zero exit (%s): %s",
                result.returncode,
                stderr.splitlines()[0]
            )
    except FileNotFoundError:
        app.logger.warning(
            "Poppler utilities not found (pdfinfo missing). Install poppler-utils to enable conversion."
        )
    except Exception:
        app.logger.exception("Unexpected error while checking for poppler utilities")


if POPPLER_PATH:
    app.logger.info("Using poppler path: %s", POPPLER_PATH)
else:
    app.logger.warning("Poppler path could not be resolved; falling back to PATH lookups")

_log_poppler_version()

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB per file
DEFAULT_DPI = 200
COMPRESSION = "tiff_deflate"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB total


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_pdfs_to_tiff(pdf_files, output_path, dpi=DEFAULT_DPI):
    """
    Convert multiple PDF files to a single multi-page TIFF

    Parameters:
        pdf_files: List of PDF file paths
        output_path: Path for output TIFF file
        dpi: Resolution for conversion

    Returns:
        Tuple of (success, message, page_count)
    """
    if not pdf_files:
        return False, "No PDF files provided", 0

    all_images = []
    total_pages = 0

    # Sort files alphabetically for consistent ordering
    pdf_files.sort()

    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            # Convert PDF pages to images
            convert_kwargs = {"dpi": dpi}
            if POPPLER_PATH:
                convert_kwargs["poppler_path"] = POPPLER_PATH

            images = convert_from_path(pdf_file, **convert_kwargs)

            # Add each page to collection
            for image in images:
                all_images.append(image)
                total_pages += 1

        except Exception as e:
            app.logger.exception("Failed to process PDF '%s'", os.path.basename(pdf_file))
            return False, f"Error processing {os.path.basename(pdf_file)}: {str(e)}", 0

    if not all_images:
        return False, "No pages were extracted from PDF files", 0

    try:
        # Save all images as multi-page TIFF
        all_images[0].save(
            output_path,
            save_all=True,
            append_images=all_images[1:],
            compression=COMPRESSION,
            dpi=(dpi, dpi)
        )

        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        message = f"Successfully created TIFF with {total_pages} pages ({file_size_mb:.2f} MB)"
        return True, message, total_pages

    except Exception as e:
        app.logger.exception("Failed to create TIFF output at '%s'", output_path)
        return False, f"Error creating TIFF file: {str(e)}", 0


def cleanup_temp_files(file_paths):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass


@app.route('/', methods=['GET'])
def index():
    """Display upload form"""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Handle PDF upload and conversion"""
    # Check if files were uploaded
    if 'pdf_files' not in request.files:
        flash('No files selected', 'error')
        return redirect(url_for('index'))

    files = request.files.getlist('pdf_files')

    if not files or files[0].filename == '':
        flash('No files selected', 'error')
        return redirect(url_for('index'))

    # Get DPI setting from form
    try:
        dpi = int(request.form.get('dpi', DEFAULT_DPI))
        if dpi < 72 or dpi > 600:
            dpi = DEFAULT_DPI
    except (ValueError, TypeError):
        dpi = DEFAULT_DPI

    # Validate and save uploaded files
    saved_files = []
    temp_dir = tempfile.mkdtemp()

    try:
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if filename:
                    file_path = os.path.join(temp_dir, filename)
                    file.save(file_path)
                    saved_files.append(file_path)

        if not saved_files:
            flash('No valid PDF files uploaded', 'error')
            shutil.rmtree(temp_dir, ignore_errors=True)
            return redirect(url_for('index'))

        # Generate output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'combined_{timestamp}.tiff'
        output_path = os.path.join(temp_dir, output_filename)

        # Convert PDFs to TIFF
        app.logger.info(
            "Starting conversion for %d file(s) at %d DPI", len(saved_files), dpi
        )
        success, message, page_count = convert_pdfs_to_tiff(saved_files, output_path, dpi)

        if success:
            # Read file into memory before sending to avoid cleanup issues
            with open(output_path, 'rb') as f:
                file_data = f.read()

            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)

            app.logger.info(
                "Conversion succeeded: %d page(s) written to %s (%.2f MB)",
                page_count,
                output_filename,
                len(file_data) / (1024 * 1024)
            )

            # Send file from memory
            return send_file(
                BytesIO(file_data),
                as_attachment=True,
                download_name=output_filename,
                mimetype='image/tiff'
            )
        else:
            app.logger.error("Conversion failed: %s", message)
            flash(f'Conversion failed: {message}', 'error')
            shutil.rmtree(temp_dir, ignore_errors=True)
            return redirect(url_for('index'))

    except Exception as e:
        app.logger.exception("Unhandled error during conversion request")
        flash(f'An error occurred: {str(e)}', 'error')
        shutil.rmtree(temp_dir, ignore_errors=True)
        return redirect(url_for('index'))


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Azure"""
    return {'status': 'healthy'}, 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash('Files too large. Maximum total size is 200MB', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
