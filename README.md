# Metadata Privacy Checker

A tool that finds hidden metadata in photos, PDFs, and Word documents, rates the privacy risk, and saves a cleaned copy.

## Features
- Reads metadata from JPG, PDF, and DOCX files
- Rates each file's risk as HIGH, MEDIUM, or LOW
- Warns when a photo contains GPS coordinates and gives a map link
- Creates cleaned copies (the original file is never changed)
- Three interfaces: a colorful terminal menu, a plain CLI, and a basic GUI

## Install
```bash
git clone https://github.com/nikhileshk0375-hash/metadata-checker.git
cd metadata-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

**Main tool (recommended):** a terminal menu with colors, a risk badge, and file/folder pickers.
```bash
python3 menu.py
```

**Plain CLI:** for scripting or automation.
```bash
python3 checker.py photo.jpg
python3 checker.py report.pdf --clean
python3 checker.py ~/Pictures --clean
```

**GUI (Tkinter window):**
```bash
python3 gui.py
```

## Risk levels
- **HIGH**: GPS location found in a photo
- **MEDIUM**: device, software, or author name found
- **LOW**: no sensitive metadata found

## Why this matters
Photos and documents often leak your location, device, name, and software without you knowing. This tool shows what is hidden and removes it before you share a file.

## Limitations
- Only JPG, PDF, and DOCX are supported
- Cleaned PDFs may still list the library name as Producer
- DOCX creation/modified dates are kept after cleaning

## Built with
Python, Pillow, pypdf, python-docx, colorama, pyfiglet, Tkinter
