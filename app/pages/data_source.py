from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from src.erp.logo_erp import LogoERP
from src.erp.db_connection import create_connection

from app.services.result_storage import service

from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
)

import os
from dotenv import load_dotenv
from datetime import timedelta, date, datetime


def render_data() -> None:
    apply_theme()
    with ui.column().classes('w-full gap-2'):
        ui.label('VERİ KAYNAĞI').classes(EYEBROW)
        ui.label('ERP Veri Yapılandırması').classes(PAGE_TITLE)

        render_source_status()
        render_analysis_range()

def render_source_status():
    if not service.is_connected or service.table_config is None:
        with ui.card().classes('w-full p-5'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('warning').classes('text-warning')
                ui.label('ERP bağlantısı henüz yapılandırılmadı.')
        return

    config = service.table_config
    with ui.card().classes('w-full p-5 gap-4'):
        # Connection Status
        with ui.row().classes('w-full items-center justify-between'):
            ui.label('Veri Kaynağı Durumu').classes('text-lg font-semibold')
            with ui.row().classes('items-center gap-2'):
                    ui.icon('check_circle').classes('text-positive')
                    ui.label('Bağlı')
        ui.separator()

        # Config details
        with ui.row().classes('w-full gap-10'):
            with ui.column().classes('gap-1'):
                ui.label("Şema").classes(MUTED)
                ui.label(config['schema'])

            with ui.column().classes('gap-1'):
                ui.label("Firma").classes(MUTED)
                ui.label(config['firm'])

            with ui.column().classes('gap-1'):
                ui.label("Kullanılabilir Dönem").classes(MUTED)
                ui.label(f"{len(config['periods'])}")

def render_analysis_range():
    if not service.is_connected or service.table_config is None:
        return
    erp = LogoERP(service.table_config)
    conn = create_connection(service.db_config)

    try:
        earliest_date, latest_date = erp.get_date_range(conn)
    finally:
        conn.close()

    if isinstance(earliest_date, datetime):
        earliest_date = earliest_date.date()

    if isinstance(latest_date, datetime):
        latest_date = latest_date.date()
    
    default_end = latest_date
    default_start = earliest_date

    with ui.card().classes('w-full p-5 gap-4'):
        ui.label("Analiz Aralığı").classes('text-lg font-semibold')
        ui.label(f'Mevcut veri aralığı: 'f'{earliest_date.strftime("%d.%m.%Y")} - 'f'{latest_date.strftime("%d.%m.%Y")}').classes(MUTED)

        with ui.row().classes('w-full gap-6'):
            with ui.column().classes('flex-1 gap-1'):
                with ui.input('Başlangıç Tarihi', value=default_start.isoformat(),) as start_input:
                    with start_input.add_slot('append'):
                        ui.icon('event').classes('cursor-pointer').on('click',lambda: start_menu.open())

                    with ui.menu() as start_menu:
                        start_date_input = ui.date(value=default_start.isoformat()).bind_value(start_input)

            with ui.column().classes('flex-1 gap-1'):
                with ui.input('Bitiş Tarihi', value=default_end.isoformat(),) as end_input:
                    with end_input.add_slot('append'):
                        ui.icon('event').classes('cursor-pointer').on('click',lambda: end_menu.open())

                    with ui.menu() as end_menu:
                        end_date_input = ui.date(value=default_end.isoformat()).bind_value(end_input)

    def refresh_erp_data():
        start_date = date.fromisoformat(start_input.value)
        end_date = date.fromisoformat(end_input.value)
        if not service.is_connected or service.table_config is None:
            ui.notify('Önce ERP veri kaynağını yapılandırın.', type='warning')
            return

        if start_date > end_date:
            ui.notify('Başlangıç tarihi bitiş tarihinden sonra olamaz.', type='warning')
            return
        service.set_analysis_config({
            'start_date': start_date,
            'end_date': end_date,
        })

        
        erp.refresh_features(start_date, end_date, db_config= service.db_config)
        ui.notify('Müşteri özellikleri yenilendi.', type='positive')

    ui.button('ERP Verilerini Yenile', on_click=refresh_erp_data).classes('bg-cyan-500 text-white')



def refresh():
    # load_dotenv()
    erp = LogoERP(service.table_config)
    erp.refresh_features(service.db_config)
    ui.notify('Müşteri özellikleri yenilendi.', type='positive')