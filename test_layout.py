from app.layout_builder import (
    build_comic_layout
)


def test_build_comic_layout_matches_panels():

    outline = [

        {
            "panel_number": 1,
            "title": "Start",
            "scene_description": "A",
            "image_prompt": "image A",
        },

        {
            "panel_number": 2,
            "title": "Next",
            "scene_description": "B",
            "image_prompt": "image B",
        },

    ]


    story = [

        {
            "panel_number": 1,
            "title": "Start",
            "caption": "Boom",
            "narration": "Run!",
            "dialogue": "Go!",
        },

        {
            "panel_number": 2,
            "title": "Next",
            "caption": "Whoosh",
            "narration": "They run.",
            "dialogue": "",
        },

    ]


    result = build_comic_layout(

        outline,

        story,

        [
            "/static/panels/a.png",
            "/static/panels/b.png"
        ]
    )


    assert (
        result[0]["panel_number"]
        == 1
    )


    assert (
        result[1]["image_path"]
        .endswith("b.png")
    )