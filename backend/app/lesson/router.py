# app/lesson/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.lesson.service import (
    generate_lesson,
    get_lesson,
    BookNotFoundError,
    DuplicateLessonError,
    LessonGenerationError,
    LessonNotFoundError,
)

router = APIRouter(prefix="/lessons", tags=["lessons"])


class GenerateLessonRequest(BaseModel):
    book_id: int
    page_from: int
    page_to: int


def _serialize_lesson(lesson):
    return {
        "lesson_id": lesson.id,
        "heading": lesson.heading,
        "objectives": lesson.objectives,
        "principles": lesson.principles,
        "rules": lesson.rules,
        "examples": lesson.examples,
    }


@router.post("/generate")
def generate_lesson_route(
    request: GenerateLessonRequest,
    db: Session = Depends(get_db),
):
    try:
        lesson = generate_lesson(
            db=db,
            book_id=request.book_id,
            page_from=request.page_from,
            page_to=request.page_to,
        )
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateLessonError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except LessonGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return _serialize_lesson(lesson)


@router.get("/{lesson_id}")
def get_lesson_route(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    try:
        lesson = get_lesson(db=db, lesson_id=lesson_id)
    except LessonNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return _serialize_lesson(lesson)