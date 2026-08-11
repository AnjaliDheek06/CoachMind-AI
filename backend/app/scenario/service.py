# app/scenario/service.py
import json
import re

from sqlalchemy.orm import Session

from app.lesson.model import Lesson
from app.scenario.model import Scenario
from app.scenario.prompt import build_scenario_prompt
from app.ai.orchestrator import generate_content, GeminiAPIError


class LessonNotFoundError(Exception):
    pass


class ScenarioGenerationError(Exception):
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


def generate_scenario(db: Session, lesson_id: int) -> tuple[Scenario, bool]:
    """
    Orchestrates scenario generation for a given lesson.
    If an unfinished scenario already exists for this lesson, it is
    returned instead of generating a new one.

    Returns:
        (scenario, is_resumed) — is_resumed is True if an existing
        unfinished scenario was returned instead of a freshly generated one.
    """

    # 1. Load the lesson
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise LessonNotFoundError(f"Lesson with ID {lesson_id} not found.")

    # 2. Check for an unfinished scenario — resume it if found, skip Gemini entirely
    active_scenario = (
        db.query(Scenario)
        .filter(
            Scenario.lesson_id == lesson_id,
            Scenario.is_completed == False,  # noqa: E712
        )
        .first()
    )
    if active_scenario is not None:
        return active_scenario, True

    # 3. Build the AI prompt
    prompt = build_scenario_prompt(lesson)

    # 4. Call the AI orchestrator
    try:
        raw_response = generate_content(prompt)
    except GeminiAPIError as e:
        raise ScenarioGenerationError(f"Failed to generate scenario: {e}")

    # 5. Parse the response
    cleaned_response = _strip_markdown_fence(raw_response)

    try:
        parsed = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ScenarioGenerationError(f"AI response was not valid JSON: {e}")

    try:
        title = parsed["title"]
        context = parsed["context"]
        objective = parsed["objective"]
    except KeyError as e:
        raise ScenarioGenerationError(f"AI response missing expected field: {e}")

    # 6. Save the new Scenario
    scenario = Scenario(
        lesson_id=lesson_id,
        title=title,
        context=context,
        objective=objective,
        is_completed=False,
    )

    db.add(scenario)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise ScenarioGenerationError(f"Failed to save the generated scenario: {e}")

    db.refresh(scenario)

    return scenario, False