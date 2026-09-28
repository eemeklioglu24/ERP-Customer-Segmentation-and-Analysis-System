from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.services.result_storage import service
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    CARD,
    SECTION_TITLE,
    BODY
)

from main import main
from src.functions import test_robustness
import ui.graphs as gp
from nicegui.element import Element


def render_content() -> None:
    apply_theme()
    
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
            
        with ui.tab_panels(tabs,value=model).classes('w-full bg-transparent'):

            # Overview panel
            with ui.tab_panel(overview):
                overview_container = ui.column().classes('w-full gap-6')
                render_overview(overview_container)

            # Cluster Panel
            with ui.tab_panel(clusters):
                cluster_container = ui.column().classes('w-full gap-6')
                render_cluster(cluster_container)
                                
            # PCA panel
            with ui.tab_panel(pca):
                pca_container = ui.column().classes('w-full gap-6')
                render_pca(pca_container)

            # Model Panel
            with ui.tab_panel(model):
                model_container = ui.column().classes('w-full gap-6')
                render_model(model_container, overview_container, cluster_container, pca_container)

def metric_card(title: str, value: str, description: str) -> None:
    with ui.card().classes(
        CARD + ' flex-1'
    ):
        ui.label(title).classes(EYEBROW)

        ui.label(value).classes(
            'text-3xl font-semibold tracking-tight'
        )

        ui.label(description).classes(MUTED)

def cluster_card(
    cluster_name: str, recency: str,
    transaction_count: str, monetary: str, avg_order_value: str,
    product_count: str, total_quantity: str, interpretation: str,) -> None:

    with ui.card().classes(
        CARD + ' w-full'
    ):

        with ui.row().classes(
            'w-full justify-between items-start'
        ):
            with ui.column().classes('gap-1'):
                ui.label(cluster_name).classes(SECTION_TITLE)

            ui.badge(
                'KÜME',
                color='secondary',
            )

        ui.separator().classes(
            'bg-slate-800 my-2'
        )

        with ui.grid(columns=3).classes(
            'w-full gap-4'
        ):

            cluster_feature('Yakınlık', recency,)

            cluster_feature('Harcama',monetary,)

            cluster_feature('Ortalama Sipariş Değeri',avg_order_value,)

            cluster_feature('Ürün Sayısı',product_count,)

            cluster_feature('İşlem Sayısı',transaction_count,)

            cluster_feature('Toplam Miktar',total_quantity,)

        ui.label(interpretation).classes(BODY + ' mt-3')

def cluster_feature(
    label: str,
    value: str,
) -> None:

    with ui.column().classes('gap-1'):

        ui.label(label).classes(
            'text-xs text-slate-500'
        )

        ui.label(value).classes(
            'text-sm font-medium'
        )

def render_overview(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return

        with ui.row().classes('w-full gap-4'):
            metric_card(
                'MÜŞTERİ SAYISI',
                str(len(service.results.get("X"))),
                'Analize dahil edilen müşteri',
            )
            metric_card(
                'KÜME SAYISI',
                str(service.results.get("K")),
                'Mevcut model yapılandırması',
            )
            metric_card(
                'SİLHOUETTE SKORU',
                f"{service.results.get("silhouette_scores")[-1]:.2f}",
                'Mevcut kümeleme kalitesi',
            )

        with ui.card().classes(CARD + ' w-full'):
            ui.label('Segment Dağılımı').classes(SECTION_TITLE)
            for i in range(service.results["K"]):
                    customer_count = int((service.results["memberships"] == i).sum())

                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label(f'Küme {i}')
                        ui.label(str(customer_count)).classes(MUTED)

def render_cluster(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return

        with ui.column().classes('w-full gap-4'):
            ui.label('Küme Profilleri').classes(SECTION_TITLE)

            for insight in service.results["cluster_insights"]:
                cluster_card(
                    cluster_name= "Küme " + str(insight["cluster"]),
                    recency= insight["recency_level"],
                    transaction_count= insight['frequency_level'],
                    monetary= insight['monetary_level'],
                    avg_order_value= insight['avg_order_value_level'],
                    product_count= insight['product_count_level'],
                    total_quantity= insight['total_quantity_level'],
                    interpretation= insight['segment_name'],
                )

def render_model(container: Element, overview_container: Element, cluster_container: Element, pca_container: Element):
    container.clear()
    with container:
    
        with ui.column().classes('w-full gap-6'):
            ui.label('Model Tanılama').classes(SECTION_TITLE)
            with ui.column().classes(
                'w-full min-h-64 '
                'items-center justify-center '
                'rounded-xl mt-4'):
                k_label = ui.label().classes(EYEBROW)
                k_slider = ui.slider(min=2, max=10, value=4, step=1).classes('w-full')

                k_label.bind_text_from(k_slider, 'value', lambda value: f'K = {int(value)}')

                def run_segmentation():
                    k = int(k_slider.value)
                    service.run(k)
                    render_overview(overview_container)
                    render_cluster(cluster_container)
                    render_pca(pca_container)
                    render_model(container, overview_container, cluster_container, pca_container)

                ui.button('Segmentasyonu Çalıştır', on_click=run_segmentation,).classes('bg-cyan-500 text-white')

            if service.results is None:
                    ui.label('Henüz segmentasyon çalıştırılmadı.')
                    return

            with ui.row().classes('w-full gap-4'):
                metric_card('SİLHOUETTE SKORU', f"{service.results["silhouette_scores"][-1]:.2f}",'Mevcut model skoru',)

                metric_card('K ARALIĞI','2 – 10','Değerlendirilen küme sayıları',)

            with ui.card().classes(CARD + ' w-full'):
                ui.label('Elbow Analizi').classes(SECTION_TITLE)

                ui.label('Farklı K değerleri için küme içi hata değişimini gösterir.').classes(MUTED)
                with ui.column().classes(
                    'w-full min-h-64 '
                    'items-center justify-center '
                    'border border-dashed border-slate-700 '
                    'rounded-xl mt-4'
                ):
    
                    ui.plotly(gp.get_obj(service.results["objective_values"]))

            with ui.card().classes(CARD + ' w-full'):

                ui.label('Silhouette Analizi').classes(SECTION_TITLE)

                ui.label('Kümelerin birbirinden ayrışma ve kendi içinde tutarlılık düzeyini karşılaştırır.').classes(MUTED)

                with ui.column().classes(
                    'w-full min-h-64 '
                    'items-center justify-center '
                    'border border-dashed border-slate-700 '
                    'rounded-xl mt-4'
                ):

                    ui.plotly(gp.get_sil(service.results["silhouette_scores"]))

            with ui.card().classes(CARD + ' w-full'):

                ui.label('Başlatma Sağlamlığı').classes(SECTION_TITLE)

                ui.label('Farklı rastgele başlangıçlarla elde edilen kümeleme sonuçlarının tutarlılığını değerlendirir.').classes(MUTED)

                with ui.column().classes(
                    'w-full min-h-64 '
                    'items-center justify-center '
                    'border border-dashed border-slate-700 '
                    'rounded-xl mt-4'
                ):
                    robustness = test_robustness(service.results['X'], len(service.results['X']), service.results['K'], n_runs=20)
                    ui.plotly(gp.get_rob(robustness["silhouettes"], robustness["silhouette_min"], service.results['K']))
                    with ui.row().classes('w-full gap-8 mt-4'):
                            metric_card("Ortalama Siluet", f"{robustness["silhouette_mean"]:.3f}", "")
                            metric_card("Siluet Sapması", f"{robustness["silhouette_std"]:.3f}", "")
                            metric_card("Ortalama Amaç", f"{robustness["objective_mean"]:.2f}", "")
                            metric_card("Amaç Sapması", f"{robustness["objective_std"]:.2f}", "")

def render_pca(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return
    
        with ui.column().classes('w-full gap-6'):
            # Başlık
            with ui.column().classes('gap-1'):
                ui.label('PCA Görselleştirmesi').classes(SECTION_TITLE)

            # Görselleştirme kontrolleri
            with ui.card().classes(CARD + ' w-full'):

                ui.label('Görselleştirme Ayarları').classes(SECTION_TITLE)

                with ui.row().classes('w-full items-end gap-6 mt-3'):

                    view_mode = ui.toggle(
                        {
                            2: '2B',
                            3: '3B',
                        },value=2,)

                    x_axis = ui.select(
                        options=[
                            'PC1',
                            'PC2',
                            'PC3',
                        ],
                        value='PC1',
                        label='X Ekseni',
                    ).classes('w-40')

                    y_axis = ui.select(
                        options=[
                            'PC1',
                            'PC2',
                            'PC3',
                        ],
                        value='PC2',
                        label='Y Ekseni',
                    ).classes('w-40')

                    z_axis = ui.select(
                        options=[
                            'PC1',
                            'PC2',
                            'PC3',
                        ],
                        value='PC3',
                        label='Z Ekseni',
                    ).classes('w-40')

            # Grafik alanı
            with ui.card().classes(CARD + ' w-full'):

                ui.label('PCA Dağılımı').classes(SECTION_TITLE)

                graph_container = ui.column().classes(
                                    'w-full min-h-80 '
                                    'items-center justify-center '
                                    'border border-dashed border-slate-700 '
                                    'rounded-xl mt-4'
                                )
                
                component_map = {'PC1': 0,'PC2': 1,'PC3': 2}

                def update_graph():
                    graph_container.clear()

                    x_index = component_map[x_axis.value]
                    y_index = component_map[y_axis.value]
                    z_index = component_map[z_axis.value]

                    fig = gp.get_pca(service.results['X_pca'], service.results['memberships'], x_index, y_index, z_index, dimensions= view_mode.value)
                    with graph_container:
                        ui.plotly(fig)
                x_axis.on_value_change(lambda _: update_graph())
                y_axis.on_value_change(lambda _: update_graph())
                z_axis.on_value_change(lambda _: update_graph())
                view_mode.on_value_change(lambda _: update_graph())

                update_graph()

                

            # Açıklanan varyans bilgileri
            with ui.card().classes(CARD + ' w-full'):

                ui.label('Görselleştirme Bilgisi').classes(SECTION_TITLE)

                with ui.grid(columns=3).classes('w-full gap-4 mt-4'):

                    with ui.column().classes('gap-1'):
                        ui.label('1. ANA BİLEŞEN').classes('text-xs text-slate-500')

                        ui.label(f"{service.results['variance_explained'][0]:.2f}").classes('text-xl font-semibold')

                    with ui.column().classes('gap-1'):
                        ui.label('2. ANA BİLEŞEN').classes('text-xs text-slate-500')

                        ui.label(f"{service.results['variance_explained'][1]:.2f}").classes('text-xl font-semibold')

                    with ui.column().classes('gap-1'):
                                            ui.label('3. ANA BİLEŞEN').classes('text-xs text-slate-500')
                    
                                            ui.label(f"{service.results['variance_explained'][2]:.2f}").classes('text-xl font-semibold')

                    with ui.column().classes('gap-1'):
                        ui.label('TOPLAM AÇIKLANAN VARYANS').classes('text-xs text-slate-500')

                        ui.label(f"{service.results['variance_explained'].sum():.2f}").classes('text-xl font-semibold text-cyan-400')