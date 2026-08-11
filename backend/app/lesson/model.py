# app/lesson/model.py
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import JSON

from app.database.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    __table_args__ = (
        UniqueConstraint("book_id", "page_from", "page_to", name="uq_lesson_book_pages"),
    )

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(
        Integer,
        ForeignKey("uploaded_books.id"),
        nullable=False
    )

    page_from = Column(Integer, nullable=False)
    page_to = Column(Integer, nullable=False)

    heading = Column(String, nullable=False)

    objectives = Column(JSON, nullable=False)
    principles = Column(JSON, nullable=False)
    rules = Column(JSON, nullable=False)
    examples = Column(JSON, nullable=False)

    book = relationship(
        "UploadedBook",
        back_populates="lessons"
    )

    scenarios = relationship(
        "Scenario",
        back_populates="lesson",
        cascade="all, delete"
    )