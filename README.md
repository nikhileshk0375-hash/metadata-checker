# Metadata Privacy Checker tool

A CLI tool that finds hidden metadata in photos, PDFs, and Word documents, warns about privacy risks like GPS location, and saves a cleaned copy.

## Features
- Reads metadata from JPG, PDF, and DOCX files
- Warns when a photo contains GPS coordinates and gives a map link
- Creates cleaned copies (the original file is never changed)
- Checks single files, multiple files, or whole folders

## Installation
```bash
git clone https://github.com/nikhileshk0375-hash/metadata-checker.git
cd metadata-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python3 checker.py photo.jpg
python3 checker.py report.pdf --clean
python3 checker.py ~/Pictures --clean
```

## Why does this matters
Photos and documents often leak your location, device, name, and software without you knowing. This tool shows what is hidden and removes it before you share a file.

## Limitations
- Cleaned PDFs may still list the library name as Producer
- DOCX creation/modified dates are kept
- Only JPG, PDF, and DOCX are supported

## Built with using
Python, Pillow, pypdf, python-docx
