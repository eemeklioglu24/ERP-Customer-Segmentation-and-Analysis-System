from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication
from app.pages.segmentation import metric_card
from app.services.result_storage import service
from app.styles.tokens import (
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    CARD,
    SECTION_TITLE,
)

from nicegui.element import Element


@ui.page('/musteriler')
def render_customers() -> None:
    if not require_authentication():
        return

    apply_theme()

    render_app_shell(
        render_content,
        active_page='musteriler',
    )


def render_content() -> None:
    with ui.column().classes('w-full gap-2'):
        ui.label('MÜŞTERİLER').classes(EYEBROW)
        ui.label('Müşteri Keşfi').classes(PAGE_TITLE)

    with ui.tabs() as tabs:
        overview = ui.tab('overview', label='Genel Bakış', icon='dashboard').classes('w-full text-slate-400').props(
                        'active-color=primary '
                        'indicator-color=primary '
                        'align=left '
                        'narrow-indicator'
                    )
        customer_list = ui.tab('customer_list', label='Müşteri Listesi', icon='group').classes('w-full text-slate-400').props(
                                'active-color=primary '
                                'indicator-color=primary '
                                'align=left '
                                'narrow-indicator'
                            )
        customer_context = ui.tab('customer_context', label='Müşteri Detayı', icon='person_search').classes('w-full text-slate-400').props(
                                'active-color=primary '
                                'indicator-color=primary '
                                'align=left '
                                'narrow-indicator'
                            )
    
    with ui.tab_panels(tabs,value=overview).classes('w-full bg-transparent'):
        with ui.tab_panel(overview):
            overview_container = ui.column().classes('w-full gap-6')
            render_overview(overview_container)

        with ui.tab_panel(customer_list):
            customer_list_container = ui.column().classes('w-full gap-6')
            render_customer_list(customer_list_container)

        with ui.tab_panel(customer_context):
            customer_context_container = ui.column().classes('w-full gap-6')
            render_customer_context(customer_context_container)


def render_overview(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return
        X = service.results["X"]
        labels = service.results["memberships"]
        K = service.results["K"]
        
        with ui.row().classes('w-full gap-4'):
            cluster_sizes = [len(X[labels == c]) for c in range(K)]
            metric_card("TOPLAM MÜŞTERİ", f"{len(X)}", " ")
            metric_card("KÜME SAYISI", f"{K}", " ")
            metric_card("EN BÜYÜK KÜME", f"Küme {cluster_sizes.index(max(cluster_sizes))}", "")
            metric_card("EN KÜÇÜK KÜME", f"Küme {cluster_sizes.index(min(cluster_sizes))}", "")

        with ui.card().classes(CARD + ' w-full'):
                    ui.label('Segment Dağılımı').classes(SECTION_TITLE)
                    for i in range(K):
                            customer_count = int((labels == i).sum())
        
                            with ui.row().classes('w-full justify-between items-center'):
                                ui.label(f'Küme {i}')
                                ui.label(str(customer_count)).classes(MUTED)
            

def render_customer_list(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return

        features = service.results["features"]
        K = service.results["K"]

        customers = features.copy()
        customers = customers.reset_index()
        customers = customers.round(2)
        customers = customers.rename(columns={"customer_id": "Müşteri ID"})

        with ui.row().classes('w-full gap-4'):
            def handle_selection(e):
                if e.selection:
                    selected_row = e.selection[0]
                    service.selected_customer_id = selected_row["Müşteri ID"]
                    ui.notify(f'Müşteri seçildi: {service.selected_customer_id}')

            customer_search = ui.input(label='Müşteri Ara', placeholder='Müşteri ID')

            cluster_filter = ui.select(['Tümü'] + [f'Küme {i}' for i in range(K)], value='Tümü', label='Küme')

            columns = [
                {
                    'name': column,
                    'label': column,
                    'field': column,
                    'sortable': True,
                }
                for column in customers.columns
            ]
            rows = customers.to_dict('records')

            table = ui.table(
                columns=columns,
                rows=rows,
                row_key='Müşteri ID',
                pagination=10,
                selection='single',
                on_select=handle_selection,
            ).classes('w-full')

            def update_table():
                filtered = customers.copy()

                if cluster_filter.value != 'Tümü':
                    cluster_number = int(cluster_filter.value.split()[-1])
                    filtered = filtered[filtered["cluster"] == cluster_number]

                if customer_search.value:
                    search = str(customer_search.value).strip()
                    filtered = filtered[filtered["Müşteri ID"].astype(str).str.contains(search, case=False)]

                table.rows = filtered.to_dict('records')
                table.update()

            cluster_filter.on_value_change(lambda _: update_table())
            customer_search.on_value_change(lambda _: update_table())

        

def render_customer_context(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return
        
