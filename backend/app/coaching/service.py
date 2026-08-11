# app/coaching/service.py
import json
import re

from sqlalchemy.orm import Session

from app.evaluation.model import Evaluation
from app.coaching.model import Coaching
from app.coaching.prompt import build_coaching_prompt
from app.ai.orchestrator import generate_content, GeminiAPIError


class EvaluationNotFoundError(Exception):
    pass


class CoachingGenerationError(Exception):
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


def generate_coaching(db: Session, evaluation_id: int) -> Coaching:
    """
    Orchestrates coaching generation for a given evaluation.
    If coaching already exists for this evaluation, it is returned
    instead of generating new coaching.

    On successful generation, marks the underlying Scenario as
    completed — per the frozen Sprint 5 contract, this is the point
    at which a practice cycle (Response -> Evaluation -> Coaching)
    is considered finished.

    Steps:
    1. Load the evaluation (and, through it, the response, scenario, lesson).
    2. Check for existing coaching — return it if found.
    3. Build the AI prompt.
    4. Call the AI orchestrator.
    5. Parse the response.
    6. Save the new Coaching and mark the scenario completed.
    """

    # 1. Load the evaluation
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if evaluation is None:
        raise EvaluationNotFoundError(f"Evaluation with ID {evaluation_id} not found.")

    response = evaluation.response
    scenario = response.scenario
    lesson = scenario.lesson

    # 2. Check for existing coaching — resume it, skip Gemini entirely
    if evaluation.coaching is not None:
        return evaluation.coaching

    # 3. Build the AI prompt
    prompt = build_coaching_prompt(lesson, scenario, response, evaluation)

    # 4. Call the AI orchestrator
    try:
        raw_response = generate_content(prompt)
    except GeminiAPIError as e:
        raise CoachingGenerationError(f"Failed to generate coaching: {e}")

    # 5. Parse the response
    cleaned_response = _strip_markdown_fence(raw_response)

    try:
        parsed = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise CoachingGenerationError(f"AI response was not valid JSON: {e}")

    try:
        key_improvements = parsed["key_improvements"]
        why_it_matters = parsed["why_it_matters"]
        next_scenario_focus = parsed["next_scenario_focus"]
    except KeyError as e:
        raise CoachingGenerationError(f"AI response missing expected field: {e}")

    # 6. Save the new Coaching and mark the scenario completed —
    #    both changes land in the same transaction
    coaching = Coaching(
        evaluation_id=evaluation_id,
        key_improvements=key_improvements,
        why_it_matters=why_it_matters,
        next_scenario_focus=next_scenario_focus,
    )

    db.add(coaching)
    scenario.is_completed = True

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise CoachingGenerationError(f"Failed to save the coaching: {e}")

    db.refresh(coaching)
    return coaching