import argparse
import sys
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from pypdf import PdfReader, PdfWriter
from docx import Document


def dms_to_decimal(dms, ref):
    """Convert (degrees, minutes, seconds) into a decimal number."""
    degrees, minutes, seconds = [float(x) for x in dms]
    value = degrees + minutes / 60 + seconds / 3600
    if ref in ("S", "W"):
        value = -value
    return value


def check_photo(path):
    print("--- Photo metadata ---")
    exif = Image.open(path).getexif()
    if not exif:
        print("No metadata found. Looks clean!")
        return

    interesting = ["Make", "Model", "Software", "Artist", "Copyright"]
    for tag_id, value in exif.items():
        name = TAGS.get(tag_id, tag_id)
        if name in interesting:
            print(f"{name}: {value}")

    taken = exif.get_ifd(0x8769).get(0x9003)  # DateTimeOriginal
    if taken:
        print(f"Date taken: {taken}")

    gps = exif.get_ifd(0x8825)
    if gps and 2 in gps and 4 in gps:
        lat = dms_to_decimal(gps[2], gps.get(1, "N"))
        lon = dms_to_decimal(gps[4], gps.get(3, "E"))
        print("\n!! WARNING: This photo contains GPS location data !!")
        print(f"Coordinates: {lat:.5f}, {lon:.5f}")
        print(f"Map: https://www.google.com/maps?q={lat},{lon}")
    else:
        print("\nNo GPS data found.")


def check_pdf(path):
    print("--- PDF metadata ---")
    info = PdfReader(path).metadata
    if not info:
        print("No metadata found. Looks clean!")
        return
    for key, value in info.items():
        print(f"{key.lstrip('/')}: {value}")


def check_docx(path):
    print("--- DOCX metadata ---")
    p = Document(path).core_properties
    print(f"Author: {p.author}")
    print(f"Last modified by: {p.last_modified_by}")
    print(f"Title: {p.title}")
    print(f"Created: {p.created}")
    print(f"Modified: {p.modified}")

def clean_photo(path, out):
    img = Image.open(path)
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    clean.save(out)


def clean_pdf(path, out):
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    writer.write(out)


def clean_docx(path, out):
    doc = Document(path)
    p = doc.core_properties
    p.author = ""
    p.last_modified_by = ""
    p.title = ""
    p.subject = ""
    p.keywords = ""
    p.comments = ""
    doc.save(out)

SUPPORTED = {".jpg", ".jpeg", ".pdf", ".docx"}


def process_file(path, clean_mode):
    ext = path.suffix.lower()
    checkers = {".jpg": check_photo, ".jpeg": check_photo,
                ".pdf": check_pdf, ".docx": check_docx}
    cleaners = {".jpg": clean_photo, ".jpeg": clean_photo,
                ".pdf": clean_pdf, ".docx": clean_docx}

    print(f"\n==== {path.name} ====")
    try:
        checkers[ext](path)
        if clean_mode:
            out = path.with_name(path.stem + "_clean" + path.suffix)
            cleaners[ext](path, out)
            print(f"Cleaned copy saved as: {out.name}")
        return True
    except Exception as e:
        print(f"Could not process this file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Metadata Privacy Checker: find and remove hidden metadata."
    )
    parser.add_argument("paths", nargs="+", help="files or folders to check")
    parser.add_argument("--clean", action="store_true",
                        help="save a cleaned copy of each file")
    args = parser.parse_args()

    files = []
    for p in args.paths:
        p = Path(p)
        if p.is_dir():
            files += [f for f in sorted(p.iterdir())
                      if f.suffix.lower() in SUPPORTED
                      and not f.stem.endswith("_clean")]
        elif p.is_file() and p.suffix.lower() in SUPPORTED:
            files.append(p)
        else:
            print(f"Skipping (not found or unsupported): {p}")

    if not files:
        print("No supported files to check.")
        return

    ok = sum(process_file(f, args.clean) for f in files)
    print(f"\nDone. Processed {ok} of {len(files)} file(s).")


main()
