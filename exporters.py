from datetime import datetime
from pathlib import Path

from fpdf import FPDF


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
)

EXPORT_DIR = (
    BASE_DIR /
    "static" /
    "exports"
)

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def _find_font() -> str | None:

    candidates = [

        Path(
            "C:/Windows/Fonts/DejaVuSans.ttf"
        ),

        Path(
            "C:/Windows/Fonts/arial.ttf"
        ),

        Path(
            "/usr/share/fonts/"
            "truetype/dejavu/"
            "DejaVuSans.ttf"
        ),

        Path(
            "/usr/share/fonts/"
            "truetype/liberation2/"
            "LiberationSans-Regular.ttf"
        ),
    ]

    for path in candidates:

        if path.exists():

            return str(path)

    return None


def save_pdf(
    layout: list[dict],
    title: str = "ComicCraft Comic"
) -> str:

    filename = (
        "comic_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )
        + ".pdf"
    )

    output = (
        EXPORT_DIR /
        filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    font = _find_font()

    if font:

        pdf.add_font(
            "ComicFont",
            "",
            font
        )

        pdf.set_font(
            "ComicFont",
            size=12
        )

    else:

        pdf.set_font(
            "Helvetica",
            size=12
        )

    for panel in layout:

        pdf.add_page()

        pdf.set_font_size(18)

        pdf.multi_cell(
            0,
            10,
            (
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            ),
            align="C"
        )

        pdf.ln(3)

        image_url = panel[
            "image_path"
        ]

        relative_path = image_url.split(
            "/static/",
            1
        )[-1]

        image_file = (
            BASE_DIR /
            "static" /
            relative_path
        )

        if image_file.exists():

            max_w = 175
            max_h = 115

            x = (
                210 - max_w
            ) / 2

            pdf.image(
                str(image_file),
                x=x,
                w=max_w,
                h=max_h
            )

            pdf.ln(7)

        pdf.set_font_size(10)

        pdf.multi_cell(
            0,
            6,
            (
                "Scene: "
                + panel[
                    "scene_description"
                ]
            )
        )

        pdf.ln(2)

        pdf.multi_cell(
            0,
            6,
            (
                "Caption: "
                + panel[
                    "caption"
                ]
            )
        )

        pdf.ln(2)

        pdf.multi_cell(
            0,
            6,
            (
                "Narration: "
                + panel[
                    "narration"
                ]
            )
        )

        if panel.get("dialogue"):

            pdf.ln(2)

            pdf.multi_cell(
                0,
                6,
                (
                    "Dialogue: "
                    + panel[
                        "dialogue"
                    ]
                )
            )

    pdf.output(
        str(output)
    )

    return (
        f"/static/exports/{filename}"
    )