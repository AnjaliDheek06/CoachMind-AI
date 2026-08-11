# app/response/service.py
from sqlalchemy.orm import Session

from app.scenario.model import Scenario
from app.response.model import Response


class ScenarioNotFoundError(Exception):
    pass


class ResponseSubmissionError(Exception):
    pass


def submit_response(db: Session, scenario_id: int, content: str) -> Response:
    """
    Persists a learner's written response to a scenario.

    Does NOT mark the scenario as completed — completion is determined
    by the coaching workflow once the full practice cycle (evaluation,
    coaching, rewrites) has finished, not by submission alone.
    """

    # 1. Load the scenario
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if scenario is None:
        raise ScenarioNotFoundError(f"Scenario with ID {scenario_id} not found.")

    # 2. Validate content
    if not content.strip():
        raise ValueError("Response cannot be empty.")

    # 3. Save the response
    response = Response(
        scenario_id=scenario_id,
        content=content,
    )

    db.add(response)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise ResponseSubmissionError(f"Failed to save the response: {e}")

    db.refresh(response)
    return response