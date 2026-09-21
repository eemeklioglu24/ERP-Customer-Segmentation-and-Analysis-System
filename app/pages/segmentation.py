from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    CARD,
    SECTION_TITLE
)


@ui.page('/segmentasyon')
def render_segmentation() -> None:
    if not require_authentication():
        return

    apply_theme()

    render_app_shell(
        render_content,
        active_page='segmentasyon',
    )


def render_content() -> None:
    with ui.column().classes('w-full gap-6'):
        with ui.column().classes('gap-1'):

            ui.label('SEGMENTASYON').classes(EYEBROW)

            ui.label('Segmentasyon Stüdyosu').classes(PAGE_TITLE)

            ui.label('Model yapılandırması, küme analizi ve model değerlendirme araçları bu alanda yer alacak.').classes(MUTED)

        with ui.tabs() as tabs:
            overview = ui.tab(
                'overview',
                label='Genel Bakış',
                icon='dashboard',
            ).classes('w-full text-slate-400').props(
                'active-color=primary '
                'indicator-color=primary '
                'align=left '
                'narrow-indicator'
            )

            clusters = ui.tab(
                'clusters',
                label= 'Kümeler',
                icon= 'category'
            ).classes('w-full text-slate-400').props(
                'active-color=primary '
                'indicator-color=primary '
                'align=left '
                'narrow-indicator'
            )

            model = ui.tab(
                'model',
                label= 'Model Tanımlama',
                icon= 'monitor_heart'
            ).classes('w-full text-slate-400').props(
                'active-color=primary '
                'indicator-color=primary '
                'align=left '
                'narrow-indicator'
            )

            pca = ui.tab(
                'pca',
                label= 'PCA',
                icon= 'scatter_plot'
            ).classes('w-full text-slate-400').props(
                'active-color=primary '
                'indicator-color=primary '
                'align=left '
                'narrow-indicator'
            )
            
        with ui.tab_panels(tabs,value=overview).classes('w-full bg-transparent'):

            with ui.tab_panel(overview):
                with ui.column().classes('w-full gap-6'):
                    with ui.row().classes('w-full gap-4'):
                        metric_card(
                            'MÜŞTERİ SAYISI',
                            '12.482',
                            'Analize dahil edilen müşteri',
                        )
                        metric_card(
                            'KÜME SAYISI',
                            '5',
                            'Mevcut model yapılandırması',
                        )
                        metric_card(
                            'SİLHOUETTE SKORU',
                            '0,41',
                            'Mevcut kümeleme kalitesi',
                        )
                        metric_card(
                            'ÖZELLİK SAYISI',
                            '6',
                            'Modelde kullanılan müşteri özellikleri',
                        )

                    with ui.card().classes(CARD + ' w-full'):
                        ui.label('Analiz Özeti').classes(SECTION_TITLE)
                        with ui.row().classes('w-full gap-8 mt-3'):
                            with ui.column().classes('gap-1'):
                                ui.label('MODEL').classes('text-xs text-slate-500')
                                ui.label('K-Means').classes('text-sm font-medium')

                            with ui.column().classes('gap-1'):
                                ui.label('KULLANILAN VERi').classes('text-xs text-slate-500')
                                ui.label('ERP SATIŞ VERİLERİ').classes('text-sm font-medium')

                            with ui.column().classes('gap-1'):
                                ui.label('DURUM').classes('text-xs text-slate-500')
                                ui.label('HAZIR').classes('text-sm font-medium')

                    with ui.card().classes(CARD + ' w-full'):
                        ui.label('Segment Dağılımı').classes(SECTION_TITLE)
                        ui.label(' Mevcut analizdeki müşteri kümelerinin örnek dağılımı.').classes(EYEBROW)
                        with ui.row().classes('w-full justify-between items-center'):
                            ui.label('Küme 0')
                            ui.label('2.314 müşteri').classes(MUTED)

                        with ui.row().classes('w-full justify-between items-center'):
                            ui.label('Küme 1')
                            ui.label('2.314 müşteri').classes(MUTED)

                        with ui.row().classes('w-full justify-between items-center'):
                            ui.label('Küme 2')
                            ui.label('2.314 müşteri').classes(MUTED)

                        with ui.row().classes('w-full justify-between items-center'):
                            ui.label('Küme 3')
                            ui.label('2.314 müşteri').classes(MUTED)
                            
                        with ui.row().classes('w-full justify-between items-center'):
                            ui.label('Küme 4')
                            ui.label('2.314 müşteri').classes(MUTED)

            with ui.tab_panel(clusters):
                ui.label('Küme analizi içeriği')

            with ui.tab_panel(model):
                ui.label('Model tanılama içeriği')

            with ui.tab_panel(pca):
                ui.label('Ana bileşenler analizi içeriği')

def metric_card(title: str, value: str, description: str) -> None:
    with ui.card().classes(
        CARD + ' flex-1'
    ):
        ui.label(title).classes(EYEBROW)

        ui.label(value).classes(
            'text-3xl font-semibold tracking-tight'
        )

        ui.label(description).classes(MUTED)