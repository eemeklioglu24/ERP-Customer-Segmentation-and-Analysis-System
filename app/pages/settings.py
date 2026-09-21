from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
)


@ui.page('/ayarlar')
def render_settings() -> None:
    apply_theme()

    render_app_shell(
        render_content,
        active_page='ayarlar',
    )


def render_content() -> None:

    with ui.column().classes('w-full gap-2'):

        ui.label(
            'AYARLAR'
        ).classes(EYEBROW)

        ui.label(
            'Uygulama Ayarları'
        ).classes(PAGE_TITLE)

        ui.label(
            'Model varsayılanları ve uygulama tercihleri '
            'bu alanda yönetilecek.'
        ).classes(MUTED)