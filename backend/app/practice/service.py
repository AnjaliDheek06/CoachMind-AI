# app/practice/service.py
from sqlalchemy.orm import Session

from app.response.model import Response
from app.scenario.model import Scenario
from app.response.service import submit_response
from app.evaluation.service import generate_evaluation
from app.coaching.service import generate_coaching

COMPLETED_SCENARIOS_TO_FINISH_PRACTICE = 3


class ResponseContentMismatchError(Exception):
    pass


def submit_practice(db: Session, scenario_id: int, content: str) -> dict:
    """
    Orchestrates the full practice cycle for a single scenario attempt:
    Response -> Evaluation -> Coaching.

    Reuses an existing Response for this scenario if one already exists
    AND its content matches what was just submitted (a safe retry).
    If an existing Response has DIFFERENT content, this raises rather
    than silently evaluating stale content — the caller sent a rewrite,
    and today's contract (one Response per scenario) has no place to
    put it without either discarding the old one or the new one, neither
    of which should happen silently.

    scenario.is_completed is set to True inside generate_coaching(), only
    after coaching is successfully saved — this function does not set it
    directly.

    practice_complete reflects whether the learner has finished the full
    practice cycle for the LESSON (three completed scenarios), not just
    the current scenario.
    """

    # 1. Reuse an existing Response for this scenario only if the content
    #    actually matches — otherwise this is a rewrite, not a retry.
    response = db.query(Response).filter(Response.scenario_id == scenario_id).first()
    if response is not None and response.content != content:
        raise ResponseContentMismatchError(
            f"A response already exists for scenario {scenario_id} with "
            "different content. Rewrites are not yet supported."
        )
    if response is None:
        response = submit_response(db=db, scenario_id=scenario_id, content=content)

    # 2. Generate (or reuse) the evaluation for this response
    evaluation = generate_evaluation(db=db, response_id=response.id)

    # 3. Generate (or reuse) coaching for this evaluation
    #    — this is the step that marks scenario.is_completed = True
    coaching = generate_coaching(db=db, evaluation_id=evaluation.id)

    # 4. Derive practice_complete from how many scenarios under this
    #    lesson have actually been completed — not from this one scenario.
    scenario = response.scenario
    lesson_id = scenario.lesson_id

    completed_count = (
        db.query(Scenario)
        .filter(
            Scenario.lesson_id == lesson_id,
            Scenario.is_completed == True,  # noqa: E712
        )
        .count()
    )
    practice_complete = completed_count >= COMPLETED_SCENARIOS_TO_FINISH_PRACTICE

    return {
        "response": {
            "response_id": response.id,
            "scenario_id": response.scenario_id,
            "content": response.content,
        },
        "evaluation": {
            "evaluation_id": evaluation.id,
            "response_id": evaluation.response_id,
            "lesson_objective_status": evaluation.lesson_objective_status,
            "communication_analysis": evaluation.communication_analysis,
            "language_analysis": evaluation.language_analysis,
            "communication_improvements": evaluation.communication_improvements,
            "grammar_corrections": evaluation.grammar_corrections,
            "micro_improvements": evaluation.micro_improvements,
        },
        "coaching": {
            "coaching_id": coaching.id,
            "evaluation_id": coaching.evaluation_id,
            "key_improvements": coaching.key_improvements,
            "why_it_matters": coaching.why_it_matters,
            "next_scenario_focus": coaching.next_scenario_focus,
        },
        "practice_complete": practice_complete,
    }