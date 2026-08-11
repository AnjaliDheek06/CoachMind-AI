# app/scenario/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.scenario.service import (
    generate_scenario,
    LessonNotFoundError,
    ScenarioGenerationError,
)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


class GenerateScenarioRequest(BaseModel):
    lesson_id: int


@router.post("/generate")
def generate_scenario_route(
    request: GenerateScenarioRequest,
    db: Session = Depends(get_db),
):
    try:
        scenario, is_resumed = generate_scenario(
            db=db,
            lesson_id=request.lesson_id,
        )
    except LessonNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScenarioGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "scenario_id": scenario.id,
        "lesson_id": scenario.lesson_id,
        "title": scenario.title,
        "context": scenario.context,
        "objective": scenario.objective,
        "is_resumed": is_resumed,
    }