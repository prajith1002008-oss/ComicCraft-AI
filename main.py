from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"


app = FastAPI(

    title="ComicCraft - AI Comic Story Creator",

    description=(
        "Generate five-panel AI comics "
        "using Gemini and Stable Diffusion."
    ),

    version="1.0.0",
)


app.mount(

    "/static",

    StaticFiles(
        directory=str(STATIC_DIR)
    ),

    name="static",
)


app.include_router(router)


@app.get(
    "/health",
    tags=["health"]
)
async def health():

    return {
        "status": "ok",
        "service": "ComicCraft"
    }