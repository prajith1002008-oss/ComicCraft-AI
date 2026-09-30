def build_comic_layout(
    outline: list[dict],
    story: list[dict],
    image_paths: list[str]
) -> list[dict]:

    """
    Match each generated image with
    its outline and story information.
    """

    story_by_number = {
        item["panel_number"]: item
        for item in story
    }

    layout = []

    sorted_outline = sorted(
        outline,
        key=lambda x: x["panel_number"]
    )

    for index, panel in enumerate(
        sorted_outline
    ):

        number = panel[
            "panel_number"
        ]

        story_panel = story_by_number.get(
            number,
            {}
        )

        layout.append({

            "panel_number": number,

            "title": panel["title"],

            "image_path": image_paths[index],

            "scene_description":
                panel["scene_description"],

            "image_prompt":
                panel["image_prompt"],

            "caption":
                story_panel.get(
                    "caption",
                    ""
                ),

            "narration":
                story_panel.get(
                    "narration",
                    ""
                ),

            "dialogue":
                story_panel.get(
                    "dialogue",
                    ""
                ),
        })

    return layout