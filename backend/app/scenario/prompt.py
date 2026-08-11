# app/scenario/prompt.py

SCENARIO_PROMPT_TEMPLATE = """You are an expert communication coach designing a short, scannable practice drill — not a short story. Learners read this in under 15 seconds before writing.

Generate exactly ONE realistic professional communication scenario the learner can practice against. The scenario must exercise the lesson's objective — not just mention it.

The scenario must be set in a professional context such as: workplace, client meeting, interview, leadership, or public speaking.

Return ONLY a JSON object in exactly this structure:

{{
  "title": "",
  "context": "",
  "objective": ""
}}

Field descriptions and STRICT length limits:
- "title": a short, specific name for the scenario (max 8 words).
- "context": the situation the learner is in, in 2-3 SHORT sentences MAXIMUM (max 40 words total). State only: who they're talking to, what's happening, what's at stake. Cut all backstory that isn't essential to acting right now. Style: "You've been answering client emails late every night for months. It's affecting your health. Today you have a 1:1 with Maya, a mentor you trust." Not one long paragraph mixing history and context.
- "objective": the communication GOAL the learner must achieve — not a specific action or tactic. ONE goal only, never stack multiple goals in one sentence. End with a response-length constraint. Style: "Explain your stress and ask for one concrete boundary. Respond in 3-5 sentences." Not: "Decompress by sharing your struggles, gather feedback on performance, and define healthy limits without compromising your reputation."

Rules:
- Base the scenario on the lesson content below. Do not hallucinate unrelated content.
- Generate a fresh and realistic scenario. Avoid generic or repetitive situations whenever possible.
- The objective must describe a single goal, not a prescribed action, and not multiple goals stacked together. Do not tell the learner what to say or which strategy to use — only what to accomplish and how long their response should be.
- Every field must be short enough to read in one glance. If you find yourself writing a paragraph, cut it down to the single most important point.
- Return ONLY valid JSON. Do not include markdown code fences, explanations, or any text outside the JSON object.

Lesson heading:
{heading}

Lesson objectives:
{objectives}

Lesson principles:
{principles}

Lesson rules:
{rules}
"""


def build_scenario_prompt(lesson) -> str:
    """
    Builds the full prompt sent to Gemini for scenario generation,
    using the lesson's stored content.
    """
    return SCENARIO_PROMPT_TEMPLATE.format(
        heading=lesson.heading,
        objectives="\n".join(f"- {o}" for o in lesson.objectives),
        principles="\n".join(f"- {p}" for p in lesson.principles),
        rules="\n".join(f"- {r}" for r in lesson.rules),
    )