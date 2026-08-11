# app/lesson/prompt.py

LESSON_PROMPT_TEMPLATE = """You are an expert communication coach designing a short, scannable lesson — not a textbook chapter. Learners read this on a screen in under 30 seconds.

Read the following text and generate a lesson based ONLY on its content. Do not add information not present in the text.

Return ONLY a JSON object in exactly this structure:

{{
  "heading": "",
  "objectives": [],
  "principles": [],
  "rules": [],
  "examples": []
}}

Field descriptions and STRICT length limits:
- "heading": a short, punchy title (max 6 words). Style: "Remove Blame, Keep Power" — not "Understanding How to Communicate Without Blame."
- "objectives": exactly ONE short sentence (max 15 words) stating the single goal of this lesson.
- "principles": 2-3 bullets MAXIMUM. Each bullet is a short phrase (max 6 words), not a sentence. Style: "Speak from your perspective." not "It's important to speak from your own perspective rather than making assumptions."
- "rules": 2-3 bullets MAXIMUM. Each bullet is a short, concrete instruction (max 8 words). Style: "Avoid 'You always...'" not a paragraph explaining why.
- "examples": 2-3 pairs MAXIMUM, each pair showing a WRONG phrase and a CORRECT phrase, both under 12 words, in this exact format: "❌ \\"<wrong phrase>\\" → ✅ \\"<correct phrase>\\"". Do not write descriptive sentences about examples — show the actual phrases side by side.

Rules:
- Never exceed the maximum bullet counts above. Fewer is better than more — pick only the 2-3 most important items.
- Every bullet must be short enough to read in under 3 seconds. If a bullet needs more than one breath to say out loud, shorten it.
- Return ONLY valid JSON. Do not include markdown code fences, explanations, or any text outside the JSON object.

Text:
------------------
{text}
------------------
"""


def build_lesson_prompt(text: str) -> str:
    """
    Builds the full prompt sent to Gemini for lesson generation,
    by inserting the extracted PDF text into the fixed instruction template.
    """
    if not text.strip():
        raise ValueError("Cannot build a lesson prompt from empty text.")

    return LESSON_PROMPT_TEMPLATE.format(text=text)