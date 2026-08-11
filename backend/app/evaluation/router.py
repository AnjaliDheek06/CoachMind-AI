# app/evaluation/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.evaluation.service import (
    generate_evaluation,
    ResponseNotFoundError,
    EvaluationGenerationError,
)

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


class GenerateEvaluationRequest(BaseModel):
    response_id: int


@router.post("/generate")
def generate_evaluation_route(
    request: GenerateEvaluationRequest,
    db: Session = Depends(get_db),
):
    try:
        evaluation = generate_evaluation(
            db=db,
            response_id=request.response_id,
        )
    except ResponseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EvaluationGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "evaluation_id": evaluation.id,
        "response_id": evaluation.response_id,
        "lesson_objective_status": evaluation.lesson_objective_status,
        "communication_analysis": evaluation.communication_analysis,
        "language_analysis": evaluation.language_analysis,
        "communication_improvements": evaluation.communication_improvements,
        "grammar_corrections": evaluation.grammar_corrections,
        "micro_improvements": evaluation.micro_improvements,
    }