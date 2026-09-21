from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
)


@ui.page('/musteriler')
def render_customers() -> None:
    if not require_authentication():
        return

    apply_theme()

    render_app_shell(
        render_content,
        active_page='musteriler',
    )


def render_content() -> None:

    with ui.column().classes('w-full gap-2'):

        ui.label(
            'MÜŞTERİLER'
        ).classes(EYEBROW)

        ui.label(
            'Müşteri Keşfi'
        ).classes(PAGE_TITLE)

        ui.label(
            'Müşterileri filtreleme, arama ve segment bazında '
            'inceleme araçları bu alanda yer alacak.'
        ).classes(MUTED)