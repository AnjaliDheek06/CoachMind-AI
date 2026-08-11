# app/upload_book/pdf_handler.py
from pathlib import Path
import hashlib
import fitz
import io
import pytesseract
from PIL import Image

# Windows only — point pytesseract at your Tesseract install.

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


from fastapi import UploadFile

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB


def read_pdf(file: UploadFile):
    """
    Validate uploaded file metadata, check size, read its bytes,
    and generate SHA-256 hash. Does NOT save the file. Does NOT parse
    PDF structure (see open_pdf_from_bytes).
    """
    if not file.filename:
        raise ValueError("No file was uploaded.")

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed.")

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File is too large ({size / (1024 * 1024):.1f} MB). "
            f"Maximum allowed size is {MAX_FILE_SIZE_BYTES / (1024 * 1024):.0f} MB."
        )

    file_bytes = file.file.read()

    if len(file_bytes) == 0:
        raise ValueError("Uploaded file is empty.")

    file_hash = hashlib.sha256(file_bytes).hexdigest()

    file.file.seek(0)

    return file_bytes, file_hash, file.filename


def open_pdf_from_bytes(file_bytes: bytes):
    """
    Parse PDF structure directly from memory (no disk I/O).
    Validates it's not encrypted and has pages.
    Caller is responsible for closing the returned document.
    """
    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Invalid or corrupted PDF: {e}")

    if document.needs_pass:
        document.close()
        raise ValueError("PDF is password protected.")

    if document.page_count == 0:
        document.close()
        raise ValueError("PDF contains no pages.")

    return document


def validate_page_range(page_from: int, page_to: int, total_pages: int) -> None:
    if page_from < 1:
        raise ValueError("page_from must be greater than or equal to 1.")
    if page_to > total_pages:
        raise ValueError(f"page_to cannot be greater than {total_pages}.")
    if page_from > page_to:
        raise ValueError("page_from cannot be greater than page_to.")


def _ocr_page(page) -> str:
    """
    Runs OCR on a single fitz page by rendering it to an image first.
    Used as a fallback when a page has no extractable embedded text
    (i.e. it's a scanned image, not real text).
    """
    pixmap = page.get_pixmap(dpi=300)
    image = Image.open(io.BytesIO(pixmap.tobytes("png")))
    return pytesseract.image_to_string(image)


def extract_text_from_document(document, page_from: int, page_to: int) -> str:
    """
    Extract text from the selected pages.

    Uses normal PDF text extraction first. If the selected pages contain
    no usable text, falls back to OCR for those pages.
    """
    start = page_from - 1
    end = page_to

    text = []

    for page_number in range(start, end):
        page = document.load_page(page_number)
        page_text = page.get_text().strip()

        if page_text:
            text.append(page_text)

    extracted_text = "\n".join(text).strip()

    # Normal text PDF — return the extracted text.
    if extracted_text:
        return extracted_text

    # Scanned/image-based PDF — OCR the selected pages.
    ocr_text = []

    for page_number in range(start, end):
        page = document.load_page(page_number)
        page_text = _ocr_page(page).strip()

        if page_text:
            ocr_text.append(page_text)

    return "\n".join(ocr_text).strip()


def save_pdf(file_bytes: bytes, file_hash: str) -> str:
    file_path = UPLOAD_FOLDER / f"{file_hash}.pdf"

    with open(file_path, "wb") as pdf_file:
        pdf_file.write(file_bytes)

    return str(file_path)


def get_pdf_info(file_path: str):
    """
    Read metadata for an already-saved PDF on disk.
    Used for post-save lookups (e.g. fetching info for an existing book),
    NOT for the upload validation flow — see open_pdf_from_bytes for that.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with fitz.open(file_path) as document:
            if document.needs_pass:
                raise ValueError("PDF is password protected.")
            total_pages = document.page_count
            if total_pages == 0:
                raise ValueError("PDF contains no pages.")
            return total_pages
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Invalid or corrupted PDF: {e}")