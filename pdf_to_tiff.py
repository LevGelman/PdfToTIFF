#!/usr/bin/env python3
"""
Convert multiple PDF files to a single multi-page TIFF file
"""

import os
import glob
from pdf2image import convert_from_path
from PIL import Image


def convert_pdfs_to_multipage_tiff(pdf_folder_path, output_tiff_path, dpi=200):
    """
    Convert all PDF files in a folder to a single multi-page TIFF file
    
    Parameters:
        pdf_folder_path: Path to folder containing PDF files
        output_tiff_path: Path for the output TIFF file
        dpi: Resolution for conversion (default: 200)
    """
    # Get all PDF files in the folder
    pdf_files = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))
    pdf_files.sort()  # Sort files alphabetically
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_folder_path}")
        return False
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    print("PDF files to process:")
    for pdf_file in pdf_files:
        print(f"  - {os.path.basename(pdf_file)}")
    
    # List to store all images from all PDFs
    all_images = []
    
    # Process each PDF file
    for pdf_idx, pdf_file in enumerate(pdf_files, 1):
        print(f"\nProcessing file {pdf_idx}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_file, dpi=dpi)
            
            # Add each page to our collection
            for page_idx, image in enumerate(images, 1):
                print(f"  - Extracting page {page_idx} of {len(images)}")
                all_images.append(image)
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            continue
    
    if not all_images:
        print("No pages were extracted from PDF files")
        return False
    
    print(f"\nTotal pages extracted: {len(all_images)}")
    print(f"Creating multi-page TIFF file: {output_tiff_path}")
    
    # Save all images as a multi-page TIFF
    # The first image is saved with all others appended
    all_images[0].save(
        output_tiff_path,
        save_all=True,
        append_images=all_images[1:],
        compression="tiff_deflate",  # Options: "none", "tiff_lzw", "tiff_deflate", "jpeg"
        dpi=(dpi, dpi)
    )
    
    print(f"✓ Successfully created multi-page TIFF: {output_tiff_path}")
    print(f"  File size: {os.path.getsize(output_tiff_path) / (1024*1024):.2f} MB")
    return True


def process_specific_files(pdf_file_list, output_tiff_path, dpi=200):
    """
    Convert a specific list of PDF files to a single multi-page TIFF file
    
    Parameters:
        pdf_file_list: List of PDF file paths
        output_tiff_path: Path for the output TIFF file
        dpi: Resolution for conversion (default: 200)
    """
    # Filter out non-existent files
    valid_files = []
    for pdf_file in pdf_file_list:
        if os.path.exists(pdf_file):
            valid_files.append(pdf_file)
        else:
            print(f"Warning: File not found - {pdf_file}")
    
    if not valid_files:
        print("No valid PDF files found")
        return False
    
    print(f"Found {len(valid_files)} valid PDF file(s)")
    
    # List to store all images
    all_images = []
    
    # Process each PDF file
    for pdf_idx, pdf_file in enumerate(valid_files, 1):
        print(f"\nProcessing file {pdf_idx}/{len(valid_files)}: {os.path.basename(pdf_file)}")
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_file, dpi=dpi)
            
            # Add each page to our collection
            for page_idx, image in enumerate(images, 1):
                print(f"  - Extracting page {page_idx} of {len(images)}")
                all_images.append(image)
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            continue
    
    if not all_images:
        print("No pages were extracted from PDF files")
        return False
    
    print(f"\nTotal pages extracted: {len(all_images)}")
    print(f"Creating multi-page TIFF file: {output_tiff_path}")
    
    # Save all images as a multi-page TIFF
    all_images[0].save(
        output_tiff_path,
        save_all=True,
        append_images=all_images[1:],
        compression="tiff_deflate",
        dpi=(dpi, dpi)
    )
    
    print(f"✓ Successfully created multi-page TIFF: {output_tiff_path}")
    print(f"  File size: {os.path.getsize(output_tiff_path) / (1024*1024):.2f} MB")
    return True


# Example usage
if __name__ == "__main__":
    print("PDF to Multi-page TIFF Converter")
    print("-" * 40)
    
    # Method 1: Convert all PDFs in a folder
    print("\nMethod 1: Convert all PDFs from a folder")
    
    # Configuration
    INPUT_FOLDER = "./pdf_files"  # Folder containing your PDF files
    OUTPUT_FILE = "./output_combined.tiff"  # Output TIFF file path
    DPI = 200  # Resolution (higher = better quality but larger file)
    
    # Create sample folder if it doesn't exist
    if not os.path.exists(INPUT_FOLDER):
        print(f"Creating folder: {INPUT_FOLDER}")
        os.makedirs(INPUT_FOLDER)
        print("Please place your PDF files in this folder and run the script again")
    else:
        # Run the conversion
        success = convert_pdfs_to_multipage_tiff(INPUT_FOLDER, OUTPUT_FILE, DPI)
        
        if not success:
            print("\nConversion failed. Please check the error messages above.")
    
    print("\n" + "=" * 40)
    
    # Method 2: Convert specific PDF files
    print("\nMethod 2: Convert specific PDF files")
    
    # Example with specific files
    specific_files = [
        "./document1.pdf",
        "./document2.pdf",
        "./document3.pdf"
    ]
    
    # Check if any of the example files exist
    existing_files = [f for f in specific_files if os.path.exists(f)]
    
    if existing_files:
        output_specific = "./specific_files_output.tiff"
        success = process_specific_files(existing_files, output_specific, DPI)
        
        if not success:
            print("\nConversion failed. Please check the error messages above.")
    else:
        print("No specific PDF files found for Method 2 demo")
        print(f"You can modify the 'specific_files' list to include your PDF file paths")
