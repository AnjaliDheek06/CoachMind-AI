# app/upload_book/router.py
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.upload_book.service import process_upload

router = APIRouter(prefix="/upload-book", tags=["upload-book"])


@router.post("/")
def upload_book(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        result = process_upload(db=db, file=file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    book = result["book"]

    return {
        "is_duplicate": result["is_duplicate"],
        "book_id": book.id,
        "file_name": book.file_name,
        "total_pages": book.total_pages,
    }