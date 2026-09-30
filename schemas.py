

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        min_length=3,
        max_length=2000
    )

    character_name: str = Field(
        default="Alex",
        min_length=1,
        max_length=80
    )

    setting: str = Field(
        default="enchanted forest",
        min_length=1,
        max_length=120
    )

    tone: str = Field(
        default="dramatic",
        min_length=1,
        max_length=60
    )

    art_style: str = Field(
        default="comic book",
        min_length=1,
        max_length=80
    )


class PanelOutline(BaseModel):

    panel_number: int = Field(
        ge=1,
        le=5
    )

    title: str

    scene_description: str

    image_prompt: str


class ComicOutline(BaseModel):

    panels: list[PanelOutline] = Field(
        min_length=5,
        max_length=5
    )


class StoryPanel(BaseModel):

    panel_number: int = Field(
        ge=1,
        le=5
    )

    title: str

    caption: str

    narration: str

    dialogue: str


class ComicStory(BaseModel):

    panels: list[StoryPanel] = Field(
        min_length=5,
        max_length=5
    )