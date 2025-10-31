# PDF to Multi-Page TIFF Converter

A Flask web application that converts multiple PDF files into a single multi-page TIFF file. Upload PDFs through a modern web interface and download the combined TIFF file. Ready for deployment to Azure Web App.

## Live Demo

Upload multiple PDFs → Get a single multi-page TIFF file

## Features

### Web Application
- 🌐 Modern, responsive web interface
- 📤 Drag-and-drop file upload
- 📥 Instant download of converted TIFF
- ⚙️ Configurable DPI settings
- 📊 Real-time file list management
- 🔒 Secure file handling
- ☁️ Ready for Azure Web App deployment

### PDF to TIFF Conversion
- ✅ Convert multiple PDF files to a single TIFF
- ✅ Preserve all pages from all PDFs
- ✅ Configurable image resolution (DPI: 150-400)
- ✅ Efficient compression (tiff_deflate)
- ✅ Progress tracking during conversion
- ✅ Error handling for corrupted PDFs
- ✅ Files processed in alphabetical order
- ✅ No OOP - simple procedural Python code

## Requirements

### Python Packages
- Python 3.6 or higher
- pdf2image >= 1.16.3
- Pillow >= 10.2.0

### System Dependencies
- **poppler-utils** (required by pdf2image)

## Installation

### Step 1: Install Python Packages

```bash
pip install pdf2image Pillow
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Install Poppler

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

#### macOS:
```bash
brew install poppler
```

#### Windows:
1. Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the archive
3. Add the `bin` folder to your system PATH

#### Fedora/RedHat:
```bash
sudo dnf install poppler-utils
```

## Quick Start

### Running the Web Application Locally

1. **Install dependencies:**
```bash
pip install -r requirements.txt

# Install poppler (required system dependency)
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler
```

2. **Run the Flask app:**
```bash
python app.py
```

3. **Open your browser:**
   - Navigate to `http://localhost:5000`
   - Upload PDF files
   - Choose DPI quality
   - Click "Convert to TIFF"
   - Download your multi-page TIFF file

### Running with Docker

```bash
# Build and run
docker-compose up

# Visit http://localhost:5000
```

### Command-Line Usage (Original Scripts)

The original command-line scripts are still available:

**Simple version** ([pdf_to_tiff_simple.py](pdf_to_tiff_simple.py)):
```bash
# Edit configuration in the file, then run:
python pdf_to_tiff_simple.py
```

**Full version** ([pdf_to_tiff.py](pdf_to_tiff.py)):
```bash
python pdf_to_tiff.py
```

### Advanced Usage (Full Version)

The full version (`pdf_to_tiff.py`) provides two methods:

#### Method 1: Convert All PDFs in a Folder

```python
from pdf_to_tiff import convert_pdfs_to_multipage_tiff

# Convert all PDFs in a folder
success = convert_pdfs_to_multipage_tiff(
    pdf_folder_path="./my_pdfs",
    output_tiff_path="./combined.tiff",
    dpi=200
)
```

#### Method 2: Convert Specific PDF Files

```python
from pdf_to_tiff import process_specific_files

# Convert specific files
pdf_list = [
    "./document1.pdf",
    "./document2.pdf",
    "./report.pdf"
]

success = process_specific_files(
    pdf_file_list=pdf_list,
    output_tiff_path="./selected_files.tiff",
    dpi=200
)
```

### Direct Script Execution

Run the full version directly:

```bash
python pdf_to_tiff.py
```

This will:
1. Look for PDFs in `./pdf_files` folder
2. Create the folder if it doesn't exist
3. Convert all PDFs found to `./output_combined.tiff`

## Configuration Options

### DPI (Resolution)
- **100-150**: Lower quality, smaller file size
- **200**: Recommended - good balance (default)
- **300**: High quality, larger file size
- **400+**: Very high quality, very large files

### Compression Types
- **"tiff_deflate"**: Best compression, lossless (default)
- **"tiff_lzw"**: Good compression, lossless
- **"jpeg"**: Lossy compression, smaller files
- **"none"**: No compression, largest files

### Example Configuration

```python
# High quality scan-like output
DPI = 300
COMPRESSION = "tiff_lzw"

# Space-saving configuration
DPI = 150
COMPRESSION = "jpeg"

# Maximum quality archival
DPI = 400
COMPRESSION = "none"
```

## File Processing Order

PDFs are processed in alphabetical order. Pages are added in this sequence:
1. All pages from first PDF (alphabetically)
2. All pages from second PDF
3. And so on...

Example:
- `report_01.pdf` (3 pages)
- `report_02.pdf` (2 pages)
- `report_03.pdf` (4 pages)

Results in a TIFF with 9 pages in that exact order.

## Output

The script provides detailed progress information:

```
Found 3 PDF file(s):
  - document1.pdf
  - document2.pdf
  - document3.pdf

Processing file 1/3: document1.pdf
  - Extracting page 1 of 5
  - Extracting page 2 of 5
  ...

Total pages extracted: 15
Creating multi-page TIFF file: output.tiff
✓ Successfully created multi-page TIFF: output.tiff
  File size: 12.45 MB
```

## Troubleshooting

### "No module named 'pdf2image'"
Install the required package:
```bash
pip install pdf2image
```

### "pdf2image.exceptions.PDFInfoNotInstalledError"
Install poppler-utils:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### "Permission denied" errors
Ensure you have write permissions in the output directory:
```bash
chmod 755 ./output_directory
```

### Large file sizes
- Reduce DPI (try 150 instead of 200)
- Use compression: "jpeg" for smallest files
- Consider splitting into multiple TIFFs if needed

### Memory errors with large PDFs
For very large PDFs or many files, you may need to:
- Process files in batches
- Reduce DPI
- Increase system swap space

## Examples

### Example 1: Convert Research Papers
```python
# For text-heavy documents
convert_pdfs_to_multipage_tiff(
    pdf_folder_path="./research_papers",
    output_tiff_path="./all_papers.tiff",
    dpi=150  # Lower DPI is fine for text
)
```

### Example 2: Convert Scanned Documents
```python
# For scanned/image-heavy PDFs
convert_pdfs_to_multipage_tiff(
    pdf_folder_path="./scans",
    output_tiff_path="./scans_archive.tiff",
    dpi=300  # Higher DPI for quality
)
```

### Example 3: Batch Processing
```python
import os

folders = ["./batch1", "./batch2", "./batch3"]

for folder in folders:
    output_name = f"{os.path.basename(folder)}_combined.tiff"
    convert_pdfs_to_multipage_tiff(
        pdf_folder_path=folder,
        output_tiff_path=output_name,
        dpi=200
    )
    print(f"Completed: {output_name}")
```

## Performance Tips

1. **File System**: Use local drives instead of network drives for better performance
2. **DPI Setting**: Start with 200 DPI and adjust based on your needs
3. **Compression**: Use "tiff_deflate" for best balance of size and quality
4. **Memory**: Close other applications when processing large batches
5. **Disk Space**: Ensure sufficient space - TIFFs can be large

## Limitations

- Requires all PDFs to be readable (not encrypted/password-protected)
- Memory usage scales with number of pages and DPI
- TIFF file size can be very large for many pages at high DPI
- Processing time increases with file size and DPI

## Deployment to Azure Web App

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions including:
- Deploy via Azure Portal (GUI)
- Deploy via Azure CLI
- Deploy with Docker
- Configuration and troubleshooting
- Cost optimization tips

**Quick deployment steps:**
1. Create Azure Web App (Python 3.11, Linux)
2. Set SECRET_KEY in Application Settings
3. Deploy code via Git or Docker
4. Install poppler-utils
5. Access your app at `https://your-app-name.azurewebsites.net`

## Project Structure

```
PdfToTIFF/
├── app.py                    # Flask web application
├── templates/
│   └── index.html           # Web interface
├── pdf_to_tiff.py           # Original CLI script (full version)
├── pdf_to_tiff_simple.py    # Original CLI script (simple version)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Local Docker setup
├── startup.sh               # Azure startup script
├── web.config               # Azure Web App configuration
├── .deployment              # Azure deployment configuration
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── DEPLOYMENT.md           # Detailed deployment guide
```

## License

This project is provided as-is for educational and commercial use.

## Support

### Documentation
- [Deployment Guide](DEPLOYMENT.md) - Complete Azure deployment instructions
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure Web Apps](https://docs.microsoft.com/azure/app-service/)

### Troubleshooting
1. Check the troubleshooting section in [DEPLOYMENT.md](DEPLOYMENT.md)
2. Ensure all requirements are installed
3. Verify PDF files are not corrupted
4. Try with a single small PDF first
5. Check application logs for errors

## Version History

- **2.0.0** - Web Application Release
  - Flask web interface with drag-and-drop upload
  - Real-time file management
  - Azure Web App deployment support
  - Docker containerization
  - Responsive design

- **1.0.0** - Initial Release
  - Command-line PDF to TIFF conversion
  - Multiple PDF to single TIFF conversion
  - Configurable DPI and compression
  - Batch processing support
  - Error handling
