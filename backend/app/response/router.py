# app/response/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.response.service import (
    submit_response,
    ScenarioNotFoundError,
    ResponseSubmissionError,
)

router = APIRouter(prefix="/responses", tags=["responses"])


class SubmitResponseRequest(BaseModel):
    scenario_id: int
    content: str


@router.post("/submit")
def submit_response_route(
    request: SubmitResponseRequest,
    db: Session = Depends(get_db),
):
    try:
        response = submit_response(
            db=db,
            scenario_id=request.scenario_id,
            content=request.content,
        )
    except ScenarioNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ResponseSubmissionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "response_id": response.id,
        "scenario_id": response.scenario_id,
        "content": response.content,
    }