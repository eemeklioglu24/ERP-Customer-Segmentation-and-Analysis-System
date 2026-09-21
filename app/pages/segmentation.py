from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    CARD,
    SECTION_TITLE,
    BODY
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

            # Overview panel
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

            # Cluster Panel
            with ui.tab_panel(clusters):
                with ui.column().classes('w-full gap-4'):

                        ui.label('Küme Profilleri').classes(SECTION_TITLE)

                        ui.label('Her kümenin müşteri davranış özelliklerini ve genel yorumunu inceleyin.').classes(MUTED)

                        mock_clusters = [
                            {
                                'cluster_name': 'Küme 0',
                                'customer_count': '2.314 müşteri',
                                'recency': 'Yakın tarihli',
                                'monetary': 'Çok yüksek',
                                'avg_order_value': 'Yüksek',
                                'product_count': 'Orta',
                                'transaction_count': 'Yüksek',
                                'total_quantity': 'Çok yüksek',
                                'interpretation': (
                                    'Yakın zamanda işlem yapmış, yüksek harcama '
                                    've işlem hacmine sahip müşteri grubu.'
                                ),
                            }
                        ]
                        for cluster in mock_clusters:
                            cluster_card(
                                cluster_name=cluster['cluster_name'],
                                customer_count=cluster['customer_count'],
                                recency=cluster['recency'],
                                monetary=cluster['monetary'],
                                avg_order_value=cluster['avg_order_value'],
                                product_count=cluster['product_count'],
                                transaction_count=cluster['transaction_count'],
                                total_quantity=cluster['total_quantity'],
                                interpretation=cluster['interpretation'],
                            )

            # Model Panel
            with ui.tab_panel(model):
                with ui.column().classes('w-full gap-6'):
                    ui.label('Model Tanılama').classes(SECTION_TITLE)
                    ui.label('Küme sayısı seçimini, model kalitesini ve başlatma kararlılığını inceleyin.').classes(MUTED)
                    with ui.row().classes('w-full gap-4'):
                        metric_card('SEÇİLEN K','5','Mevcut küme sayısı',)

                        metric_card('SİLHOUETTE SKORU','0,41','Mevcut model skoru',)

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
                            ui.icon('show_chart',size='38px',).classes('text-slate-600')

                            ui.label('Elbow grafiği burada gösterilecek').classes(MUTED)

                    with ui.card().classes(CARD + ' w-full'):

                        ui.label('Silhouette Analizi').classes(SECTION_TITLE)

                        ui.label('Kümelerin birbirinden ayrışma ve kendi içinde tutarlılık düzeyini karşılaştırır.').classes(MUTED)

                        with ui.column().classes(
                            'w-full min-h-64 '
                            'items-center justify-center '
                            'border border-dashed border-slate-700 '
                            'rounded-xl mt-4'
                        ):
                            ui.icon('analytics',size='38px',).classes('text-slate-600')

                            ui.label('Silhouette grafiği burada gösterilecek').classes(MUTED)

                    with ui.card().classes(CARD + ' w-full'):

                        ui.label('Başlatma Sağlamlığı').classes(SECTION_TITLE)

                        ui.label('Farklı rastgele başlangıçlarla elde edilen kümeleme sonuçlarının tutarlılığını değerlendirir.').classes(MUTED)

                        with ui.row().classes('w-full gap-8 mt-4'):

                            with ui.column().classes('gap-1'):
                                ui.label('TEST SAYISI').classes('text-xs text-slate-500')

                                ui.label('10').classes('text-sm font-medium')

                            with ui.column().classes('gap-1'):
                                ui.label('DURUM').classes('text-xs text-slate-500')

                                ui.label('Kararlı').classes('text-sm font-medium text-emerald-400')
                                
            # PCA panel
            with ui.tab_panel(pca):
                with ui.column().classes('w-full gap-6'):

                    # Başlık
                    with ui.column().classes('gap-1'):
                        ui.label('PCA Görselleştirmesi').classes(SECTION_TITLE)

                        ui.label('Müşteri segmentlerinin ana bileşenler uzayındaki dağılımını inceleyin.').classes(MUTED)

                    # Görselleştirme kontrolleri
                    with ui.card().classes(CARD + ' w-full'):

                        ui.label('Görselleştirme Ayarları').classes(SECTION_TITLE)

                        with ui.row().classes('w-full items-end gap-6 mt-3'):

                            view_mode = ui.toggle(
                                {
                                    '2d': '2B',
                                    '3d': '3B',
                                },value='2d',)

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

                    # Grafik alanı
                    with ui.card().classes(CARD + ' w-full'):

                        ui.label('PCA Dağılımı').classes(SECTION_TITLE)

                        ui.label('Müşterilerin ana bileşenler uzayındaki dağılımı bu alanda gösterilecek.').classes(MUTED)

                        with ui.column().classes(
                            'w-full min-h-80 '
                            'items-center justify-center '
                            'border border-dashed border-slate-700 '
                            'rounded-xl mt-4'
                        ):

                            ui.icon('scatter_plot',size='42px',).classes('text-slate-600')

                            ui.label('PCA grafiği burada gösterilecek').classes(MUTED)

                    # Açıklanan varyans bilgileri
                    with ui.card().classes(CARD + ' w-full'):

                        ui.label('Görselleştirme Bilgisi').classes(SECTION_TITLE)

                        ui.label('Ana bileşenlerin veri üzerindeki açıklama oranlarını gösterir.').classes(MUTED)

                        with ui.grid(columns=3).classes('w-full gap-4 mt-4'):

                            with ui.column().classes('gap-1'):
                                ui.label('1. ANA BİLEŞEN').classes('text-xs text-slate-500')

                                ui.label('%42,6').classes('text-xl font-semibold')

                            with ui.column().classes('gap-1'):
                                ui.label('2. ANA BİLEŞEN').classes('text-xs text-slate-500')

                                ui.label('%23,8').classes('text-xl font-semibold')

                            with ui.column().classes('gap-1'):
                                ui.label('TOPLAM AÇIKLANAN VARYANS').classes('text-xs text-slate-500')

                                ui.label('%66,4').classes('text-xl font-semibold text-cyan-400')
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
    cluster_name: str, customer_count: str, recency: str,
    transaction_count: str, monetary: str, avg_order_value: str,
    product_count: str, total_quantity: str,interpretation: str,) -> None:

    with ui.card().classes(
        CARD + ' w-full'
    ):

        with ui.row().classes(
            'w-full justify-between items-start'
        ):
            with ui.column().classes('gap-1'):
                ui.label(cluster_name).classes(SECTION_TITLE)
                ui.label(customer_count).classes(MUTED)

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