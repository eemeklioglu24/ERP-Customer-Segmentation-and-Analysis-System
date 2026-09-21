from nicegui import ui

from app.styles.tokens import (
    PRIMARY,
    SECONDARY,
    ACCENT,
    POSITIVE,
    NEGATIVE,
    WARNING,
    INFO
)

def apply_theme():
    ui.colors(
        primary=PRIMARY,
        secondary=SECONDARY,
        accent=ACCENT,
        positive=POSITIVE,
        negative=NEGATIVE,
        warning=WARNING,
        info=INFO,
    )
    ui.dark_mode().enable()

    ui.query("body").classes("bg-slate-950 text-slate-100")

    ui.query(".nicegui-content").classes("p-0")