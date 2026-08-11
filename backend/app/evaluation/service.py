# app/evaluation/service.py
import json
import re

from sqlalchemy.orm import Session

from app.response.model import Response
from app.evaluation.model import Evaluation
from app.evaluation.prompt import build_evaluation_prompt
from app.ai.orchestrator import generate_content, GeminiAPIError


class ResponseNotFoundError(Exception):
    pass


class EvaluationGenerationError(Exception):
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


def generate_evaluation(db: Session, response_id: int) -> Evaluation:
    """
    Orchestrates evaluation generation for a given response.
    If an evaluation already exists for this response, it is returned
    instead of generating a new one.

    Steps:
    1. Load the response (and, through it, the scenario and lesson).
    2. Check for an existing evaluation — return it if found.
    3. Build the AI prompt.
    4. Call the AI orchestrator.
    5. Parse the response.
    6. Save the new Evaluation.
    """

    # 1. Load the response
    response = db.query(Response).filter(Response.id == response_id).first()
    if response is None:
        raise ResponseNotFoundError(f"Response with ID {response_id} not found.")

    scenario = response.scenario
    lesson = scenario.lesson

    # 2. Check for an existing evaluation — resume it, skip Gemini entirely
    if response.evaluation is not None:
        return response.evaluation

    # 3. Build the AI prompt
    prompt = build_evaluation_prompt(lesson, scenario, response)

    # 4. Call the AI orchestrator
    try:
        raw_response = generate_content(prompt)
    except GeminiAPIError as e:
        raise EvaluationGenerationError(f"Failed to generate evaluation: {e}")

    # 5. Parse the response
    cleaned_response = _strip_markdown_fence(raw_response)

    try:
        parsed = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise EvaluationGenerationError(f"AI response was not valid JSON: {e}")

    try:
        lesson_objective_status = parsed["lesson_objective_status"]
        communication_analysis = parsed["communication_analysis"]
        language_analysis = parsed["language_analysis"]
        communication_improvements = parsed["communication_improvements"]
        grammar_corrections = parsed["grammar_corrections"]
        micro_improvements = parsed["micro_improvements"]
    except KeyError as e:
        raise EvaluationGenerationError(f"AI response missing expected field: {e}")

    # 6. Save the new Evaluation
    evaluation = Evaluation(
        response_id=response_id,
        lesson_objective_status=lesson_objective_status,
        communication_analysis=communication_analysis,
        language_analysis=language_analysis,
        communication_improvements=communication_improvements,
        grammar_corrections=grammar_corrections,
        micro_improvements=micro_improvements,
    )

    db.add(evaluation)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise EvaluationGenerationError(f"Failed to save the evaluation: {e}")

    db.refresh(evaluation)
    return evaluation