from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from pypdf import PdfReader, PdfWriter
from docx import Document

SUPPORTED = {".jpg", ".jpeg", ".pdf", ".docx"}

HIGH = {"GPS"}
MEDIUM = {"Make", "Model", "Software", "Artist", "Copyright",
          "Author", "Last modified by", "Creator"}


def dms_to_decimal(dms, ref):
    d, m, s = [float(x) for x in dms]
    value = d + m / 60 + s / 3600
    return -value if ref in ("S", "W") else value


def read_photo(path):
    fields = []
    exif = Image.open(path).getexif()
    for tag_id, value in exif.items():
        name = TAGS.get(tag_id, tag_id)
        if name in ("Make", "Model", "Software", "Artist", "Copyright"):
            fields.append((name, str(value)))
    taken = exif.get_ifd(0x8769).get(0x9003)
    if taken:
        fields.append(("Date taken", str(taken)))
    gps = exif.get_ifd(0x8825)
    if gps and 2 in gps and 4 in gps:
        lat = dms_to_decimal(gps[2], gps.get(1, "N"))
        lon = dms_to_decimal(gps[4], gps.get(3, "E"))
        fields.append(("GPS", f"{lat:.5f}, {lon:.5f}"))
    return fields


def read_pdf(path):
    info = PdfReader(path).metadata
    if not info:
        return []
    return [(k.lstrip("/"), str(v)) for k, v in info.items() if v]


def read_docx(path):
    p = Document(path).core_properties
    pairs = [("Author", p.author), ("Last modified by", p.last_modified_by),
             ("Title", p.title), ("Created", p.created), ("Modified", p.modified)]
    return [(k, str(v)) for k, v in pairs if v]


def get_risk(fields):
    """Return (level, reasons) based on what the file leaks."""
    names = {name for name, _ in fields}
    if names & HIGH:
        return "HIGH", ["Contains GPS location"]
    found = sorted(names & MEDIUM)
    if found:
        return "MEDIUM", ["Reveals: " + ", ".join(found)]
    return "LOW", ["No sensitive metadata found"]


def analyze(path):
    path = Path(path)
    ext = path.suffix.lower()
    readers = {".jpg": read_photo, ".jpeg": read_photo,
               ".pdf": read_pdf, ".docx": read_docx}
    if ext not in readers:
        raise ValueError("Unsupported file type")
    fields = readers[ext](path)
    level, reasons = get_risk(fields)
    return {"fields": fields, "risk": level, "reasons": reasons}


def clean(path):
    path = Path(path)
    ext = path.suffix.lower()
    out = path.with_name(path.stem + "_clean" + path.suffix)
    if ext in (".jpg", ".jpeg"):
        img = Image.open(path)
        new = Image.new(img.mode, img.size)
        new.paste(img)
        new.save(out)
    elif ext == ".pdf":
        reader, writer = PdfReader(path), PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({})
        writer.write(out)
    elif ext == ".docx":
        doc = Document(path)
        p = doc.core_properties
        p.author = p.last_modified_by = p.title = ""
        p.subject = p.keywords = p.comments = ""
        doc.save(out)
    return out
