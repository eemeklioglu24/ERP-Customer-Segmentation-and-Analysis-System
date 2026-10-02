from nicegui import ui

from app.state.auth_state import (
    is_authenticated,
    login,
)
from app.styles.theme import apply_theme
from app.services.result_storage import service
from app.pages.data_source import refresh
from src.erp.db_connection import create_connection, test_connection
from src.erp.db_metadata import get_available_tables


import re

@ui.page('/giris')
def render_login() -> None:
    print('LOGIN PAGE RENDERED')
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
            ui.icon('hub',size='42px',).classes('text-cyan-400')

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
                    render_table_config(table_config_container)
                else:
                    ui.notify('Bağlantı kurulamadı.', type='negative')

            with ui.column().classes('w-full') as db_config_container:
                ui.label("Veritabanı Bağlantısı").classes('text-2xl font-semibold')
                ui.separator().classes('bg-slate-800 my-3')

                server_input = ui.input("Sunucu").props('outlined dense').classes('w-full')
                database_input = ui.input("Veritabanı").props('outlined dense').classes('w-full')
                user_input = ui.input("Kullanıcı Adı").props('outlined dense').classes('w-full')
                password_input = ui.input("Şifre", password= True, password_toggle_button= True).props('outlined dense').classes('w-full')

                ui.button('Bağlantıyı Test Et', icon='login', on_click=test_db_connection,).classes('w-full').props('unelevated')
                render_synth_button()

            with ui.column().classes('w-full') as table_config_container:
                pass




def handle_login() -> None:
    login()
    refresh()
    service.run(4)
    ui.navigate.to("/genel-bakis")

def render_synth_button():
    def generate_fake_data():
        service.set_fake_data()
        #refresh()
        handle_login()
    ui.separator()
    ui.button('Demo Verileriyle Devam Et', icon='login', on_click=generate_fake_data,).classes('w-full').props('unelevated')

def render_table_config(table_config_container):
    def confirm():
        firm = firm_input.value.strip()
        schema = schema_select.value
        if not schema or not firm:
            ui.notify('Şema ve firma numarası girilmelidir.', type='warning')
            return

        if not firm.isdigit():
            ui.notify('Firma numarası yalnızca rakamlardan oluşmalıdır.', type='warning')
            return

        firm = firm.zfill(3)
        pattern = re.compile(rf'^LG_{re.escape(firm)}_(\d{{2}})_(INVOICE|STLINE)$')
        periods = {}
        for table in tables:
            if table['schema'] != schema:
                continue

            match = pattern.match(table['table'])
            if match is None:
                continue

            period = match.group(1)
            table_type = match.group(2)
            if period not in periods:
                periods[period] = set()

            periods[period].add(table_type)

        valid_periods = sorted([period for period, table_types in periods.items() if {'INVOICE', 'STLINE'}.issubset(table_types)])

        if not valid_periods:
            ui.notify('Bu firma için uygun ERP tabloları bulunamadı.', type='negative')
            return

        table_config = {
            'schema': schema,
            'firm': firm,
            'periods': valid_periods,
        }

        service.set_table_config(table_config)

        ui.notify(f'Veri kaynağı doğrulandı. {len(valid_periods)} dönem bulundu.', type='positive')
        handle_login()
        

    table_config_container.clear()
    with table_config_container:
        tables = get_available_tables(service.db_config)
        schemas = sorted(set(table["schema"] for table in tables))
        schema_select = ui.select(schemas, label="Şema").props('outlined dense').classes('w-full')

        firm_input = ui.input('Firma Numarası').props('outlined dense maxlength=3').classes('w-full')

        ui.button("Yapılandırmayı Doğrula", on_click=confirm).classes('w-full').props('unelevated')
