from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
)


@ui.page('/veri-kaynagi')
def render_data_source() -> None:
    apply_theme()

    render_app_shell(
        render_content,
        active_page='veri-kaynagi',
    )


def render_content() -> None:

    with ui.column().classes('w-full gap-2'):

        ui.label(
            'VERİ KAYNAĞI'
        ).classes(EYEBROW)

        ui.label(
            'ERP Veri Yapılandırması'
        ).classes(PAGE_TITLE)

        ui.label(
            'Firma, dönem, tablolar ve analiz veri aralığı '
            'bu alanda yapılandırılacak.'
        ).classes(MUTED)