from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from src.erp.logo_erp import LogoERP

from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
)

import os
from dotenv import load_dotenv


@ui.page('/veri-kaynagi')
def render_data_source() -> None:
    if not require_authentication():
        return
    
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

        ui.button('ERP Verilerini Yenile', on_click=refresh).classes('bg-cyan-500 text-white')

def refresh():
    load_dotenv()
    db_config = {
        "server": os.getenv("DB_SERVER"),
        "database": os.getenv("DB_NAME"),
        "username": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }
    table_config = {
        "schema": os.getenv("SCHEMA"),
        "invoice_table": os.getenv("INVOICE"),
        "stockline_table": os.getenv("STOCKLINE"),
    }
    erp = LogoERP(table_config)
    erp.refresh_features(db_config)
    ui.notify('Müşteri özellikleri yenilendi.', type='positive')