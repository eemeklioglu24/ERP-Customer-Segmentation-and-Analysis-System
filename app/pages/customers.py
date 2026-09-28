from nicegui import ui, app

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

def render_customers() -> None:
    apply_theme()
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
                    service.results["selected_customer_id"] = selected_row["Müşteri ID"]
                    ui.notify(f'Müşteri seçildi: {service.results.get("selected_customer_id")}')
                    render_customer_context.refresh()

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
            page_size = app.storage.user.get("table_page_size", 20,)

            table = ui.table(
                columns=columns,
                rows=rows,
                row_key='Müşteri ID',
                selection='single',
                on_select=handle_selection,
                pagination={"rowsPerPage": page_size,},
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

        
@ui.refreshable
def arender_customer_context(container: Element):
    container.clear()
    with container:
        if service.results is None:
            ui.label('Henüz segmentasyon çalıştırılmadı.')
            return
        if service.results.get("selected_customer_id") is None:
            ui.label('Detaylarını görüntülemek için bir müşteri seçin.').classes(MUTED)
            return

        features = service.results["features"]
        K = service.results["K"]

        customers = features.copy()
        customers = customers.reset_index()
        customers = customers.round(2)
        customers = customers.rename(columns={"customer_id": "Müşteri ID"})
        customer = customers[customers["Müşteri ID"] == service.results.get("selected_customer_id")].iloc[0]

        ui.label(f'Müşteri {service.results.get("selected_customer_id")}').classes(PAGE_TITLE)
        ui.badge(f'Küme {int(customer["cluster"])}')

        metrics = [
            ("SON ALIŞVERİŞ", f"{customer["recency"]:.0f}", ""),
            ("TOPLAM HARCAMA", f"{customer["monetary"]:.2f}", ""),
            ("İŞLEM SAYISI", f"{customer["transaction_count"]:.0f}", ""),
            ("ÜRÜN SAYISI", f"{customer["product_count"]:.0f}", ""),
            ("TOPLAM MİKTAR", f"{customer["total_quantity"]:.0f}", ""),
            ("ORT. SİPARİŞ DEĞERİ", f"{customer["avg_order_value"]:.2f}", ""),
        ]

        cluster_id = int(customer["cluster"])
        interpretation = service.results.get("cluster_insights")[cluster_id]

        with ui.row().classes('w-full gap-4 flex-wrap'):
            for title, value, unit in metrics:
                customer_metric_card(title, f"{value}", unit)
            for key, value in interpretation.items():
                customer_metric_card(f"{key}", f"{value}", "")

@ui.refreshable
def render_customer_context(container: Element):
    container.clear()

    with container:

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if service.results is None:
            ui.label(
                "Henüz segmentasyon çalıştırılmadı."
            ).classes(MUTED)
            return

        selected_customer_id = service.results.get(
            "selected_customer_id"
        )

        if selected_customer_id is None:
            with ui.column().classes(
                "w-full items-center justify-center py-16 gap-3"
            ):
                ui.icon(
                    "person_search"
                ).classes(
                    "text-5xl text-slate-600"
                )

                ui.label(
                    "Henüz müşteri seçilmedi"
                ).classes(
                    "text-lg font-semibold"
                )

                ui.label(
                    "Detaylarını görüntülemek için "
                    "müşteri listesinden bir müşteri seçin."
                ).classes(MUTED)

            return

        # -------------------------------------------------
        # Customer data
        # -------------------------------------------------

        features = service.results["features"]

        customers = features.reset_index()

        customer_rows = customers[
            customers["customer_id"] == selected_customer_id
        ]

        if customer_rows.empty:
            ui.label(
                "Seçilen müşteri mevcut sonuçlarda bulunamadı."
            ).classes(MUTED)
            return

        customer = customer_rows.iloc[0]

        cluster_id = int(customer["cluster"])

        # User-facing cluster number.
        # Internally cluster_id remains zero-based.
        display_cluster_id = cluster_id + 1

        cluster_customers = customers[
            customers["cluster"] == cluster_id
        ]

        cluster_medians = cluster_customers[
            [
                "recency",
                "monetary",
                "transaction_count",
                "product_count",
                "total_quantity",
                "avg_order_value",
            ]
        ].median()

        cluster_size = len(cluster_customers)
        total_customers = len(customers)

        cluster_share = (
            cluster_size / total_customers * 100
            if total_customers
            else 0
        )

        interpretation = service.results[
            "cluster_insights"
        ][cluster_id]

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        with ui.row().classes(
            "w-full items-start justify-between gap-4"
        ):

            with ui.column().classes("gap-1"):

                ui.label(
                    "MÜŞTERİ DETAYI"
                ).classes(EYEBROW)

                ui.label(
                    f"Müşteri {selected_customer_id}"
                ).classes(PAGE_TITLE)

                ui.label(
                    "Müşteri davranışları ve ait olduğu "
                    "küme içerisindeki konumu."
                ).classes(MUTED)

            with ui.column().classes(
                "items-end gap-2"
            ):

                ui.badge(
                    f"Küme {display_cluster_id}"
                ).props(
                    "outline"
                ).classes(
                    "text-sm px-3 py-1"
                )

                ui.label(
                    f"{cluster_size} müşteri · "
                    f"%{cluster_share:.1f}"
                ).classes(
                    "text-xs text-slate-500"
                )

        # -------------------------------------------------
        # Customer metrics
        # -------------------------------------------------

        ui.label(
            "Müşteri Özeti"
        ).classes(
            "text-lg font-semibold mt-4"
        )

        ui.label(
            "Seçili müşterinin temel satın alma göstergeleri."
        ).classes(MUTED)

        with ui.element("div").classes(
            "w-full grid "
            "grid-cols-1 "
            "md:grid-cols-2 "
            "xl:grid-cols-3 "
            "gap-4 mt-2"
        ):

            customer_metric_card(
                title="SON ALIŞVERİŞ",
                value=customer["recency"],
                icon="schedule",
                cluster_median=cluster_medians["recency"],
                suffix=" gün",
            )

            customer_metric_card(
                title="TOPLAM HARCAMA",
                value=customer["monetary"],
                icon="payments",
                cluster_median=cluster_medians["monetary"],
                decimals=2,
                prefix="₺",
            )

            customer_metric_card(
                title="İŞLEM SAYISI",
                value=customer["transaction_count"],
                icon="receipt_long",
                cluster_median=cluster_medians[
                    "transaction_count"
                ],
                suffix=" işlem",
            )

            customer_metric_card(
                title="ÜRÜN SAYISI",
                value=customer["product_count"],
                icon="inventory_2",
                cluster_median=cluster_medians[
                    "product_count"
                ],
                suffix=" ürün",
            )

            customer_metric_card(
                title="TOPLAM MİKTAR",
                value=customer["total_quantity"],
                icon="shopping_cart",
                cluster_median=cluster_medians[
                    "total_quantity"
                ],
                suffix=" adet",
            )

            customer_metric_card(
                title="ORT. SİPARİŞ DEĞERİ",
                value=customer["avg_order_value"],
                icon="calculate",
                cluster_median=cluster_medians[
                    "avg_order_value"
                ],
                decimals=2,
                prefix="₺",
            )

        # -------------------------------------------------
        # Cluster context
        # -------------------------------------------------

        with ui.card().classes(
            "w-full p-5 gap-4 mt-4 "
            "border border-slate-800 "
            "bg-slate-900/30"
        ):

            with ui.row().classes(
                "w-full items-center gap-3"
            ):
                ui.icon(
                    "groups"
                ).classes(
                    "text-xl text-slate-400"
                )

                with ui.column().classes("gap-0"):
                    ui.label(
                        "Küme Profili"
                    ).classes(
                        "text-lg font-semibold"
                    )

                    ui.label(
                        f"Müşteri, Küme {display_cluster_id} "
                        "davranış profili içerisinde yer alıyor."
                    ).classes(MUTED)

            ui.separator().classes(
                "bg-slate-800"
            )

            with ui.element("div").classes(
                "w-full grid "
                "grid-cols-1 "
                "md:grid-cols-2 "
                "xl:grid-cols-3 "
                "gap-x-8 gap-y-4"
            ):

                for key, value in interpretation.items():

                    with ui.column().classes("gap-1"):
                        ui.label(
                            str(key)
                        ).classes(
                            "text-xs uppercase "
                            "tracking-wide text-slate-500"
                        )

                        ui.label(
                            str(value)
                        ).classes(
                            "font-medium"
                        )

def format_tr_number(value: float, decimals: int = 0) -> str:
    formatted = f"{value:,.{decimals}f}"
    return (
        formatted
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )


def customer_metric_card(
    title: str,
    value: float,
    icon: str,
    cluster_median: float,
    decimals: int = 0,
    prefix: str = "",
    suffix: str = "",
) -> None:

    formatted_value = (
        f"{prefix}{format_tr_number(value, decimals)}{suffix}"
    )

    formatted_median = (
        f"{prefix}{format_tr_number(cluster_median, decimals)}{suffix}"
    )

    with ui.card().classes(
        "w-full p-4 gap-2 "
        "border border-slate-800 "
        "bg-slate-900/40"
    ):
        with ui.row().classes(
            "w-full items-center justify-between"
        ):
            ui.label(title).classes(
                "text-xs font-semibold tracking-wide text-slate-400"
            )

            ui.icon(icon).classes(
                "text-lg text-slate-500"
            )

        ui.label(formatted_value).classes(
            "text-2xl font-semibold"
        )

        ui.label(
            f"Küme medyanı: {formatted_median}"
        ).classes(
            "text-xs text-slate-500"
        )


        
        
