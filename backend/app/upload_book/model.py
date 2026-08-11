# app/upload_book/model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class UploadedBook(Base):
    __tablename__ = "uploaded_books"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)          # original filename, e.g. "report.pdf"
    stored_file_name = Column(String, nullable=False)    # hash-based name on disk, e.g. "a1b2c3....pdf"
    file_hash = Column(String, nullable=False, unique=True)
    file_path = Column(String, nullable=False)
    total_pages = Column(Integer, nullable=False)

    lessons = relationship(
        "Lesson",
        back_populates="book",
        cascade="all, delete",
    )