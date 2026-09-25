from nicegui import ui, app

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    SECTION_TITLE
)
from app.services.result_storage import service

def render_set() -> None:
    with ui.column().classes('w-full gap-6'):

        # Sayfa başlığı
        with ui.column().classes('gap-1'):
            ui.label('AYARLAR').classes(EYEBROW)

            ui.label(
                'Uygulama Ayarları'
            ).classes(PAGE_TITLE)

            ui.label(
                'Uygulamanın varsayılan davranışlarını ve yerel tercihlerini yönetin.'
            ).classes(MUTED)

        render_analysis_defaults()
        render_application_preferences()
        render_data_management()


def render_analysis_defaults() -> None:

    current_range = app.storage.user.get('default_analysis_range','all',)

    with ui.card().classes(
        'w-full p-5 gap-4 '
        'bg-slate-900/60 '
        'border border-slate-800 '
        'shadow-none'
    ):
        ui.label('Analiz Varsayılanları').classes(SECTION_TITLE)

        ui.label('Yeni bir analiz başlatıldığında kullanılacak başlangıç ayarları.').classes(MUTED)

        ui.separator().classes('bg-slate-800')

        with ui.row().classes('w-full items-center justify-between gap-6'):

            with ui.column().classes('gap-1'):
                ui.label('Varsayılan Analiz Aralığı').classes('text-sm font-medium text-slate-200')
                ui.label('Veri Kaynağı sayfası ilk açıldığında seçilecek tarih aralığı.').classes('text-xs text-slate-500')

            range_select = ui.select(
                {
                    'all': 'Tüm veri seti',
                    '12m': 'Son 12 ay',
                    '6m': 'Son 6 ay',
                }, value=current_range).classes('w-48')

            range_select.on('update:model-value', lambda e: app.storage.user.__setitem__('default_analysis_range',e.args,),)

def render_application_preferences() -> None:

    current_page_size = app.storage.user.get('table_page_size',50,)

    with ui.card().classes(
        'w-full p-5 gap-4 '
        'bg-slate-900/60 '
        'border border-slate-800 '
        'shadow-none'
    ):
        ui.label('Uygulama Tercihleri').classes(SECTION_TITLE)
        ui.label('Liste ve tabloların varsayılan görünümünü belirleyin.').classes(MUTED)

        ui.separator().classes('bg-slate-800')

        with ui.row().classes('w-full items-center justify-between gap-6'):

            with ui.column().classes('gap-1'):
                ui.label('Varsayılan Tablo Satır Sayısı').classes('text-sm font-medium text-slate-200')
                ui.label('Müşteri listelerinde bir sayfada gösterilecek kayıt sayısı.').classes('text-xs text-slate-500')

            page_size_select = ui.select(
                [25, 50, 100],
                value=current_page_size,
            ).classes('w-48')

            page_size_select.on('update:model-value', lambda e: app.storage.user.__setitem__('table_page_size',int(e.args),),)

def render_data_management() -> None:

    def clear_analysis_results() -> None:
        if service.results:
            service.results.clear()

        dialog.close()

        ui.notify('Analiz sonuçları temizlendi.',type='positive',)

    with ui.dialog() as dialog:
        with ui.card().classes('w-96 p-5 gap-4 ''bg-slate-900 border border-slate-800'):
            ui.label('Analiz sonuçlarını temizle').classes('text-lg font-semibold text-slate-100')
            ui.label('Mevcut segmentasyon sonuçları silinecek. ''Veritabanı bağlantısı ve veri kaynağı ayarları korunacaktır.').classes(MUTED)

            with ui.row().classes('w-full justify-end gap-2'):
                ui.button('İptal',on_click=dialog.close,).props('flat')
                ui.button('Temizle',icon='delete_outline', on_click=clear_analysis_results,).props('color=negative')

    with ui.card().classes(
        'w-full p-5 gap-4 '
        'bg-slate-900/60 '
        'border border-slate-800 '
        'shadow-none'
    ):
        ui.label('Oturum ve Veriler').classes(SECTION_TITLE)

        ui.label('Mevcut çalışma sırasında oluşturulan analiz sonuçlarını yönetin.').classes(MUTED)
        ui.separator().classes('bg-slate-800')

        with ui.row().classes('w-full items-center justify-between gap-6'):

            with ui.column().classes('gap-1'):
                ui.label('Analiz Sonuçlarını Temizle').classes('text-sm font-medium text-slate-200')
                ui.label('Kümeleme ve analiz sonuçlarını sıfırlar.').classes('text-xs text-slate-500')
            ui.button('Temizle', icon='delete_outline', on_click=dialog.open, ).props('outline color=negative')

