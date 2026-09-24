from nicegui import ui

from app.state.auth_state import (
    is_authenticated,
    login,
)
from app.styles.theme import apply_theme
from app.services.result_storage import service
from src.erp.db_connection import create_connection, test_connection

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

            server_input = ui.input("Sunucu").props('outlined dense').classes('w-full')
            database_input = ui.input("Veritabanı").props('outlined dense').classes('w-full')
            user_input = ui.input("Kullanıcı Adı").props('outlined dense').classes('w-full')
            password_input = ui.input("Şifre", password= True, password_toggle_button= True).props('outlined dense').classes('w-full')

            def test_db_connection():
                db_config = {
                                "server": server_input.value,
                                "database": database_input.value,
                                "username": user_input.value,
                                "password": password_input.value
                            }
                service.set_db_config(db_config)
                service.is_connected = test_connection(service.db_config)

                if service.is_connected:
                    ui.notify('Bağlantı başarılı.', type='positive')
                else:
                    ui.notify('Bağlantı kurulamadı.', type='negative')

            ui.button('Bağlantıyı Test Et', icon='login', on_click=test_db_connection,).classes('w-full').props('unelevated')



def handle_login() -> None:
    login()
    ui.navigate.to("/genel-bakis")