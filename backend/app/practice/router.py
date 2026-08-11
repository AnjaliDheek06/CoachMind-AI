# app/practice/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.practice.service import (
    submit_practice,
    ResponseContentMismatchError,
)
from app.response.service import ScenarioNotFoundError, ResponseSubmissionError
from app.evaluation.service import EvaluationGenerationError
from app.coaching.service import CoachingGenerationError

router = APIRouter(prefix="/practice", tags=["practice"])


class SubmitPracticeRequest(BaseModel):
    scenario_id: int
    content: str


@router.post("/respond")
def submit_practice_route(
    request: SubmitPracticeRequest,
    db: Session = Depends(get_db),
):
    try:
        result = submit_practice(
            db=db,
            scenario_id=request.scenario_id,
            content=request.content,
        )
    except ScenarioNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ResponseContentMismatchError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except (ResponseSubmissionError, EvaluationGenerationError, CoachingGenerationError) as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result