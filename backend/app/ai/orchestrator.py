from app.ai import gemini_client


class GeminiAPIError(Exception):
    pass


def generate_content(prompt: str) -> str:
    """
    Accepts a prompt, calls the Gemini client, and returns the raw response.
    """
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        response = gemini_client.call_gemini(prompt)
    except Exception as e:
        raise GeminiAPIError(f"Gemini API call failed: {e}")

    return response