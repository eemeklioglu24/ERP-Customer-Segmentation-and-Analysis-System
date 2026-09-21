from nicegui import ui

from app.state.auth_state import (
    is_authenticated,
    login,
)
from app.styles.theme import apply_theme

@ui.page('/giris')
def render_login() -> None:
    apply_theme()
    if is_authenticated():
        ui.navigate.to('/genel-bakis')
        return
    with ui.column().classes(
    'w-full min-h-screen '
    'bg-slate-950 text-slate-100 '
    'items-center justify-center p-6'
    ):

        with ui.card().classes(
            'w-full max-w-md '
            'bg-slate-900 border border-slate-800 '
            'rounded-2xl p-8'
        ):
            ui.icon(
                'hub',
                size='42px',
            ).classes(
                'text-cyan-400'
            )
            ui.label("Müşteri Analitiği").classes('text-2xl font-semibold')
            ui.label("Müşteri segmentasyonu ve davranış analizi platformu").classes('text-sm text-slate-400')
            ui.separator().classes('bg-slate-800 my-3')

            def handle_login() -> None:
                login()
                ui.navigate.to("/genel-bakis")

            ui.button(
                'Geliştirme Girişi',
                icon='login',
                on_click=handle_login,
            ).classes('w-full').props('unelevated')
            ui.label(
                'Bu giriş yalnızca geliştirme ve test amacıyla kullanılmaktadır.'
            ).classes(
                'text-xs text-slate-500 text-center'
            )