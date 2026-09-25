from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from ui.graphs import get_bar
from app.styles.tokens import (
    BODY,
    CARD,
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    SECTION_TITLE,
)

from app.services.result_storage import service
import numpy as np

def render_dashboard_content() -> None:
    apply_theme()
    with ui.column().classes("w-full gap-6"):
         # Başlık
        with ui.column().classes('gap-1'):
            ui.label('GENEL BAKIŞ').classes(EYEBROW)
            ui.label('Müşteri Analitiği Özeti').classes(PAGE_TITLE)
            ui.label('Mevcut veri seti ve segmentasyon sonuçlarının genel görünümü.').classes(MUTED)

        # KPI değerleri
        results = service.results

        if results:
            X = results.get('X')
            memberships = results.get('memberships')

            customer_count = len(X) if X is not None else None
            cluster_count = (int(memberships.max()) + 1 if memberships is not None and len(memberships) > 0 else None)
            feature_count = (X.shape[1] if X is not None else None)

        else:
            customer_count = None
            cluster_count = None
            feature_count = None

        # KPI kartları
        with ui.row().classes('w-full gap-4'):

            dashboard_metric('MÜŞTERİ SAYISI', f'{customer_count:,}'.replace(',', '.') if customer_count is not None else '—','groups',)
            dashboard_metric('KÜME SAYISI', str(cluster_count) if cluster_count is not None else '—', 'scatter_plot',)
            dashboard_metric('ÖZELLİK SAYISI', str(feature_count) if feature_count is not None else '—', 'tune',)
            dashboard_metric('ZAMAN ARALIĞI', f"{service.analysis_config["start_date"]} / {service.analysis_config["end_date"]}" if service.analysis_config else '—', 'model_training',)

        memberships = service.results.get("memberships") if service.results else None

        # Bar Chart
        with ui.card().classes('w-full p-5 gap-4 ''bg-slate-900/60 border border-slate-800 shadow-none'):
            ui.label('Müşteri Dağılımı').classes(SECTION_TITLE)
            ui.label('Müşterilerin kümelere göre dağılımı.').classes(MUTED)

            if memberships is None or len(memberships) == 0:
                ui.label('Henüz segmentasyon çalıştırılmadı.').classes('text-sm text-slate-500')

            else:
                clusters, counts = np.unique(memberships, return_counts=True,)
                percentages = counts / counts.sum() * 100
                ui.plotly(get_bar(clusters, counts, percentages)).classes('w-full h-80')

        # Cluster Insights for the fifth bloody time
        cluster_insights = service.results.get("cluster_insights") if service.results else None

        with ui.column().classes('w-full gap-4'):

            ui.label('Segment Özeti').classes(SECTION_TITLE)
            ui.label('Kümelerin temel müşteri özelliklerine göre kısa özeti.').classes(MUTED)

            if not cluster_insights:
                ui.label('Henüz segmentasyon sonucu bulunmuyor.').classes('text-sm text-slate-500')

            else:
                with ui.row().classes('w-full gap-4 flex-wrap'):
                    for insight in cluster_insights:
                        cluster_id = insight["cluster"]
                        customer_count = insight["customer_count"]
                        monetary_share = insight["monetary_share"]
                        segment_name = insight["segment_name"]

                        with ui.card().classes('w-72 p-4 gap-3 ''bg-slate-900/60 ''border border-slate-800 ''shadow-none'):

                            with ui.row().classes('w-full items-start justify-between'):
                                with ui.column().classes('gap-0'):
                                    ui.label(f'Küme {cluster_id + 1}').classes('text-xs font-semibold ''tracking-wide text-cyan-400')
                                    ui.label(segment_name).classes('text-base font-semibold text-slate-100')

                                    ui.icon('groups', size='20px').classes('text-slate-500')

                            ui.separator().classes('bg-slate-800')

                            ui.label(f'{customer_count:,} müşteri'.replace(',', '.')).classes('text-sm text-slate-300')
                            ui.label(f'Toplam cironun %{monetary_share:.1f}\'i').classes('text-sm text-slate-400')

        # Buttons
        with ui.column().classes('w-full gap-4'):
            ui.label('Hızlı Erişim').classes(SECTION_TITLE)
            ui.label('Detaylı analiz ve veri yönetimi sayfalarına hızlıca geçin.').classes(MUTED)

            with ui.row().classes('w-full gap-4 flex-wrap'):

                ui.button('Segmentasyonu İncele',icon='scatter_plot',on_click=lambda: ui.navigate.to('/segmentasyon'),).props('outline').classes('px-5 py-3')

                ui.button('Müşterileri Görüntüle', icon='groups', on_click=lambda: ui.navigate.to('/musteriler'),).props('outline').classes('px-5 py-3')

                ui.button('Veri Kaynağını Yönet', icon='storage', on_click=lambda: ui.navigate.to('/veri-kaynagi'),).props('outline').classes('px-5 py-3')
        

def dashboard_metric(title: str, value: str, icon: str,) -> None:
    with ui.card().classes(
        'flex-1 min-w-48 '
        'p-5 gap-3 '
        'bg-slate-900/60 '
        'border border-slate-800 '
        'shadow-none'
    ):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(title).classes('text-xs font-medium tracking-wide text-slate-500')

            ui.icon(icon, size='20px').classes('text-cyan-400')

        ui.label(value).classes('text-2xl font-semibold text-slate-100')