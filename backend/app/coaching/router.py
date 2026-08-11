# app/coaching/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.coaching.service import (
    generate_coaching,
    EvaluationNotFoundError,
    CoachingGenerationError,
)

router = APIRouter(prefix="/coaching", tags=["coaching"])


class GenerateCoachingRequest(BaseModel):
    evaluation_id: int


@router.post("/generate")
def generate_coaching_route(
    request: GenerateCoachingRequest,
    db: Session = Depends(get_db),
):
    try:
        coaching = generate_coaching(
            db=db,
            evaluation_id=request.evaluation_id,
        )
    except EvaluationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CoachingGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "coaching_id": coaching.id,
        "evaluation_id": coaching.evaluation_id,
        "key_improvements": coaching.key_improvements,
        "why_it_matters": coaching.why_it_matters,
        "next_scenario_focus": coaching.next_scenario_focus,
    }