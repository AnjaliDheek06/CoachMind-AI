import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Please check your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

DEFAULT_MODEL = "gemini-3.5-flash"


def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the raw text response.
    Does not catch exceptions — callers (e.g. ai/orchestrator.py)
    are responsible for handling failures.
    """
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
    )

    return response.text