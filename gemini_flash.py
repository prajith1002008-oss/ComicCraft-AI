import json

from google import genai
from google.genai import types

from .config import get_settings
from .schemas import ComicOutline, PromptRequest


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


def generate_outline(
    request: PromptRequest
) -> list[dict]:

    """
    Generate exactly five comic panels.
    """

    settings = get_settings()

    client = _client()

    prompt = f"""
Create a coherent five-panel comic outline.

User story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

1. Exactly 5 panels.
2. Number panels from 1 to 5.
3. Keep the same main character throughout.
4. Maintain story continuity.
5. Each panel must have:
   - panel_number
   - title
   - scene_description
   - image_prompt
6. The image prompt must describe:
   - characters
   - action
   - environment
   - lighting
   - composition
   - camera angle
   - requested art style
7. Make the story engaging.
8. Do not add extra panels.
9. Do not include explicit sexual content.
10. Return only the requested structured data.
"""

    response = client.models.generate_content(

        model=settings.gemini_flash_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=ComicOutline,

            temperature=0.9,
        ),
    )

    parsed = getattr(
        response,
        "parsed",
        None
    )

    if parsed:

        outline = parsed

        return [
            panel.model_dump()
            for panel in outline.panels
        ]

    text = (
        response.text or ""
    ).strip()

    if not text:

        raise RuntimeError(
            "Gemini returned an empty outline."
        )

    try:

        data = json.loads(text)

        outline = ComicOutline.model_validate(
            data
        )

        return [
            panel.model_dump()
            for panel in outline.panels
        ]

    except Exception as exc:

        raise RuntimeError(
            f"Could not parse Gemini outline JSON: {exc}"
        ) from exc