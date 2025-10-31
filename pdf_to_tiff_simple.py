#!/usr/bin/env python3
"""
Simple PDF to Multi-page TIFF Converter
Usage: Modify the INPUT_FOLDER and OUTPUT_FILE variables, then run the script
"""

import os
import glob
from pdf2image import convert_from_path
from PIL import Image

# ============= CONFIGURATION =============
# Modify these paths according to your needs
INPUT_FOLDER = "./pdf_files"  # Folder containing your PDF files
OUTPUT_FILE = "./combined_output.tiff"  # Output TIFF file path
DPI = 200  # Resolution (200 is good balance of quality and file size)
COMPRESSION = "tiff_deflate"  # Options: "none", "tiff_lzw", "tiff_deflate", "jpeg"
# =========================================

# Get all PDF files
pdf_files = glob.glob(os.path.join(INPUT_FOLDER, "*.pdf"))
pdf_files.sort()  # Sort alphabetically

if not pdf_files:
    print(f"No PDF files found in {INPUT_FOLDER}")
    print("Please create the folder and add PDF files, then run again")
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
    exit(1)

print(f"Found {len(pdf_files)} PDF file(s):")
for pdf in pdf_files:
    print(f"  - {os.path.basename(pdf)}")

# Collect all pages from all PDFs
all_pages = []
total_pages = 0

for pdf_file in pdf_files:
    print(f"\nProcessing: {os.path.basename(pdf_file)}")
    
    try:
        # Convert PDF to images
        pages = convert_from_path(pdf_file, dpi=DPI)
        
        # Add to collection
        for i, page in enumerate(pages, 1):
            print(f"  Page {i}/{len(pages)}")
            all_pages.append(page)
            total_pages += 1
            
    except Exception as e:
        print(f"  ERROR: {e}")
        continue

if not all_pages:
    print("\nNo pages were extracted!")
    exit(1)

print(f"\nTotal pages collected: {total_pages}")
print(f"Creating TIFF file: {OUTPUT_FILE}")

# Save as multi-page TIFF
all_pages[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=all_pages[1:],
    compression=COMPRESSION,
    dpi=(DPI, DPI)
)

# Display results
file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"\n✓ Success! Created: {OUTPUT_FILE}")
print(f"  Total pages: {total_pages}")
print(f"  File size: {file_size_mb:.2f} MB")
print(f"  Resolution: {DPI} DPI")
print(f"  Compression: {COMPRESSION}")
