from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # ========================================================
    # GEMINI
    # ========================================================

    gemini_api_key: str = ""

    gemini_flash_model: str = "gemini-2.5-flash"

    gemini_pro_model: str = "gemini-2.5-pro"

    # ========================================================
    # IMAGE GENERATION
    # ========================================================

    image_backend: str = "placeholder"

    image_model: str = (
        "stable-diffusion-v1-5/stable-diffusion-v1-5"
    )

    image_width: int = 512

    image_height: int = 512

    image_steps: int = 20

    image_guidance_scale: float = 7.5

    image_seed: int | None = None

    # ========================================================
    # SERVER
    # ========================================================

    app_host: str = "127.0.0.1"

    app_port: int = 8000

    debug: bool = True

    # ========================================================
    # MODEL CACHE
    # ========================================================

    model_cache_dir: str = str(
        BASE_DIR / "model_cache"
    )

    model_config = SettingsConfigDict(

        env_file=".env",

        env_file_encoding="utf-8",

        case_sensitive=False,

        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:

    return Settings()