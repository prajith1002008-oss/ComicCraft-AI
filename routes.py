from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    FileResponse,
    HTMLResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .schemas import PromptRequest


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)

templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)

router = APIRouter()


def _generate_comic(
    request_data: PromptRequest
):

    # Step 1:
    # Gemini Flash generates outline

    outline = generate_outline(
        request_data
    )

    # Step 2:
    # Gemini Pro generates story

    story = generate_story(
        outline,
        request_data.character_name,
        request_data.tone
    )

    # Step 3:
    # Generate images

    image_paths = []

    for panel in outline:

        image_path = generate_image(

            panel["image_prompt"],

            panel["panel_number"]
        )

        image_paths.append(
            image_path
        )

    # Step 4:
    # Build final layout

    layout = build_comic_layout(

        outline,

        story,

        image_paths
    )

    # Step 5:
    # Export PDF

    pdf_path = save_pdf(
        layout
    )

    return (
        outline,
        story,
        layout,
        pdf_path
    )


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={},
    )


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    data = PromptRequest(

        story_prompt=story_prompt,

        character_name=character_name,

        setting=setting,

        tone=tone,

        art_style=art_style,
    )

    try:

        (
            outline,
            story,
            layout,
            pdf_path
        ) = _generate_comic(data)

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={

                "error": str(exc),

                "form":
                    data.model_dump(),
            },

            status_code=500,
        )

    return templates.TemplateResponse(

        request=request,

        name="comic_preview.html",

        context={

            "layout": layout,

            "pdf_path": pdf_path,

            "request_data":
                data.model_dump(),
        },
    )


@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(
    data: PromptRequest
):

    try:

        (
            _,
            _,
            layout,
            pdf_path
        ) = _generate_comic(data)

        return {

            "success": True,

            "layout": layout,

            "pdf_path": pdf_path,
        }

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        ) from exc


@router.get(
    "/test-image"
)
async def test_image(

    prompt: str =
    (
        "a brave fox exploring "
        "an enchanted forest, "
        "comic book art"
    )
):

    try:

        image_path = generate_image(

            prompt,

            999
        )

        return {

            "success": True,

            "image_path":
                image_path,

            "prompt":
                prompt,
        }

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        ) from exc


@router.get(
    "/download/{filename}"
)
async def download_pdf(
    filename: str
):

    # Prevent path traversal.

    safe_name = Path(
        filename
    ).name

    pdf_path = (
        BASE_DIR /
        "static" /
        "exports" /
        safe_name
    )

    if (
        not pdf_path.exists()
        or
        pdf_path.suffix.lower()
        != ".pdf"
    ):

        raise HTTPException(

            status_code=404,

            detail="PDF not found."
        )

    return FileResponse(

        path=str(pdf_path),

        media_type="application/pdf",

        filename=safe_name,
    )


@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(

    request: Request,

    pdf_path: str = ""
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={
            "pdf_path": pdf_path
        },
    )