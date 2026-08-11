# app/lesson/service.py
import json
import re

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.upload_book.model import UploadedBook
from app.upload_book.pdf_handler import extract_text_from_document, open_pdf_from_bytes
from app.lesson.model import Lesson
from app.lesson.prompt import build_lesson_prompt
from app.ai.orchestrator import generate_content, GeminiAPIError


class BookNotFoundError(Exception):
    pass


class DuplicateLessonError(Exception):
    pass


class LessonGenerationError(Exception):
    pass


class LessonNotFoundError(Exception):
    pass


def _strip_markdown_fence(raw: str) -> str:
    """
    Gemini sometimes wraps JSON responses in markdown code fences
    (```json ... ``` or ``` ... ```). Strip them before parsing.
    """
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def get_lesson(db: Session, lesson_id: int) -> Lesson:
    """
    Loads a lesson by ID. No AI, no PDF work — pure database read.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise LessonNotFoundError(f"Lesson with ID {lesson_id} not found.")

    return lesson


def generate_lesson(
    db: Session,
    book_id: int,
    page_from: int,
    page_to: int,
) -> Lesson:
    """
    Orchestrates lesson generation for a given book and page range.
    If a lesson for this (book_id, page_from, page_to) already exists,
    returns the existing lesson instead of generating a new one.
    """

    # 1. Load the uploaded book
    book = db.query(UploadedBook).filter(UploadedBook.id == book_id).first()
    if book is None:
        raise BookNotFoundError(f"Book with ID {book_id} not found.")

    # 2. Check for an existing lesson — return it if found (no error)
    existing_lesson = (
        db.query(Lesson)
        .filter(
            Lesson.book_id == book_id,
            Lesson.page_from == page_from,
            Lesson.page_to == page_to,
        )
        .first()
    )
    if existing_lesson is not None:
        return existing_lesson

    # 3. Read PDF text for the given page range
    with open(book.file_path, "rb") as f:
        file_bytes = f.read()

    document = open_pdf_from_bytes(file_bytes)
    try:
        text = extract_text_from_document(document, page_from, page_to)
    finally:
        document.close()

    # 4. Build the AI prompt
    prompt = build_lesson_prompt(text)

    # 5. Call the AI orchestrator
    try:
        raw_response = generate_content(prompt)
    except GeminiAPIError as e:
        raise LessonGenerationError(f"Failed to generate lesson content: {e}")

    # 6. Parse the response
    cleaned_response = _strip_markdown_fence(raw_response)

    try:
        parsed = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise LessonGenerationError(f"AI response was not valid JSON: {e}")

    try:
        heading = parsed["heading"]
        objectives = parsed["objectives"]
        principles = parsed["principles"]
        rules = parsed["rules"]
        examples = parsed["examples"]
    except KeyError as e:
        raise LessonGenerationError(f"AI response missing expected field: {e}")

    # 7. Save the new Lesson
    lesson = Lesson(
        book_id=book_id,
        page_from=page_from,
        page_to=page_to,
        heading=heading,
        objectives=objectives,
        principles=principles,
        rules=rules,
        examples=examples,
    )

    db.add(lesson)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_lesson = (
            db.query(Lesson)
            .filter(
                Lesson.book_id == book_id,
                Lesson.page_from == page_from,
                Lesson.page_to == page_to,
            )
            .first()
        )
        if existing_lesson is not None:
            return existing_lesson
        raise DuplicateLessonError(
            f"Lesson for book {book_id}, pages {page_from}-{page_to} already exists."
        )

    db.refresh(lesson)
    return lesson