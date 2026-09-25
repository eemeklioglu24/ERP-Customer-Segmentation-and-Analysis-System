from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
)


def render_set() -> None:
    apply_theme()
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