# app/upload_book/service.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.upload_book.model import UploadedBook
from app.upload_book.pdf_handler import (
    read_pdf,
    open_pdf_from_bytes,
    save_pdf,
)


def process_upload(db: Session, file):
    """
    Orchestrates the PDF upload workflow.

    Responsibilities:
    1. Read the uploaded PDF (filename check + hash).
    2. Check for a duplicate book — return the existing one if found.
    3. Validate PDF structure (not corrupted, not encrypted, has pages).
    4. Save the PDF to disk.
    5. Create and persist the UploadedBook record.

    Does NOT extract text or handle page ranges — see lesson/service.py.
    """

    # 1. Read uploaded PDF (filename check + hash)
    file_bytes, file_hash, file_name = read_pdf(file)

    # 2. Check for duplicate book — return existing, don't re-process
    existing_book = (
        db.query(UploadedBook)
        .filter(UploadedBook.file_hash == file_hash)
        .first()
    )
    if existing_book is not None:
        return {"is_duplicate": True, "book": existing_book}

    # 3. Validate PDF structure (corrupted / encrypted / empty) and get page count
    document = open_pdf_from_bytes(file_bytes)
    total_pages = document.page_count
    document.close()

    # 4. Save to disk (only after validation has passed)
    file_path = save_pdf(file_bytes=file_bytes, file_hash=file_hash)

    # 5. Persist the new book
    book = UploadedBook(
        file_name=file_name,
        stored_file_name=f"{file_hash}.pdf",
        file_hash=file_hash,
        file_path=file_path,
        total_pages=total_pages,
    )

    db.add(book)
    try:
        db.commit()
    except IntegrityError:
        # Race condition: another request inserted the same file_hash
        # between our check (step 2) and this commit.
        db.rollback()
        existing_book = (
            db.query(UploadedBook)
            .filter(UploadedBook.file_hash == file_hash)
            .first()
        )
        return {"is_duplicate": True, "book": existing_book}

    db.refresh(book)
    return {"is_duplicate": False, "book": book}