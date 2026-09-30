import json

from google import genai
from google.genai import types

from .config import get_settings
from .schemas import ComicOutline, ComicStory


def _client() -> genai.Client:

    settings = get_settings()

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_story(
    outline: list[dict],
    character_name: str,
    tone: str
) -> list[dict]:

    """
    Expand the outline into captions,
    narration and dialogue.
    """

    settings = get_settings()

    client = _client()

    validated_outline = ComicOutline.model_validate(
        {
            "panels": outline
        }
    )

    prompt = f"""
Turn this five-panel comic outline into
a polished comic story.

Main character:
{character_name}

Tone:
{tone}

For every panel:

- Preserve the panel number.
- Preserve the panel title.
- Create a short caption.
- Create concise narration.
- Create natural dialogue.
- Maintain continuity.
- Keep the same characters.
- Do not add panels.
- If dialogue is unnecessary, return an empty string.

Return only structured data matching
the requested schema.

OUTLINE:

{validated_outline.model_dump_json(indent=2)}
"""

    response = client.models.generate_content(

        model=settings.gemini_pro_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=ComicStory,

            temperature=0.8,
        ),
    )

    parsed = getattr(
        response,
        "parsed",
        None
    )

    if parsed:

        story = parsed

        return [
            panel.model_dump()
            for panel in story.panels
        ]

    text = (
        response.text or ""
    ).strip()

    if not text:

        raise RuntimeError(
            "Gemini returned an empty story."
        )

    try:

        data = json.loads(text)

        story = ComicStory.model_validate(
            data
        )

        return [
            panel.model_dump()
            for panel in story.panels
        ]

    except Exception as exc:

        raise RuntimeError(
            f"Could not parse Gemini story JSON: {exc}"
        ) from exc