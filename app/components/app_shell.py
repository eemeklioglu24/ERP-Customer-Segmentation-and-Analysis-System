from collections.abc import Callable

from nicegui import ui

from app.styles.tokens import (
    EYEBROW,
    MUTED,
    SECTION_TITLE,
)

from app.state.auth_state import logout

def render_app_shell(
    routes: dict[str, Callable[[], None]],
) -> None:

    nav_buttons = {}

    with ui.column().classes(
        "w-full min-h-screen bg-slate-950 text-slate-100 gap-0"
    ):

        # Üst bilgi çubuğu
        with ui.row().classes(
            "w-full h-16 px-5 "
            "items-center justify-between "
            "border-b border-slate-800 "
            "bg-slate-950"):

            with ui.row().classes("items-center gap-3"):
                ui.icon("hub",size="26px",).classes("text-cyan-400")

                with ui.column().classes("gap-0"):
                    ui.label("Müşteri Analitiği").classes("text-sm font-bold tracking-widest")

            with ui.row().classes("items-center gap-4"):
                def handle_logout() -> None:
                    logout()
                    ui.navigate.to('/giris')

                
                ui.badge("YEREL",color="secondary",)

                with ui.row().classes("items-center gap-2"):
                    ui.icon("database",size="18px",).classes("text-emerald-400")

                    ui.label("Veritabanı bağlı").classes("text-sm text-slate-300")

                    ui.button('Çıkış Yap',icon='logout',on_click=handle_logout,).props('flat').classes('text-slate-300')

        # Ana uygulama alanı
        with ui.row().classes(
            "w-full flex-1 "
            "items-stretch gap-0"
        ):

            # Sol navigasyon alanı
            with ui.column().classes(
                "w-20 "
                "border-r border-slate-800 "
                "bg-slate-950 "
                "items-center py-5 gap-3"
            ):

                nav_buttons['/genel-bakis'] = navigation_button(
                    icon='space_dashboard',
                    tooltip='Genel Bakış',
                    target='/genel-bakis',
                )

                nav_buttons['/segmentasyon'] = navigation_button(
                    icon='scatter_plot',
                    tooltip='Segmentasyon',
                    target='/segmentasyon',
                )

                nav_buttons['/musteriler'] = navigation_button(
                    icon='groups',
                    tooltip='Müşteriler',
                    target='/musteriler',
                )

                nav_buttons['/veri-kaynagi'] = navigation_button(
                    icon='storage',
                    tooltip='Veri Kaynağı',
                    target='/veri-kaynagi',
                )

                ui.space()

                nav_buttons['/ayarlar'] = navigation_button(
                    icon='settings',
                    tooltip='Ayarlar',
                    target='/ayarlar',
                )

            # Ana çalışma alanı
            with ui.column().classes(
                "flex-1 min-w-0 "
                "p-6 gap-6 "
                "bg-slate-950"
            ):
                ui.sub_pages(routes).classes('w-full')

            # Sağ bağlam paneli
            with ui.column().classes(
                "w-72 "
                "border-l border-slate-800 "
                "bg-slate-900/40 "
                "p-5 gap-6"
            ):

                ui.label("ANALİZ DURUMU").classes(EYEBROW)

                with ui.column().classes("gap-4"):

                    context_item("Küme Sayısı","5",)

                    context_item("Müşteri Sayısı","12.482",)

                    context_item("Model","K-Means",)

                ui.separator().classes("bg-slate-800")

                ui.label("Mevcut Çalışma").classes(SECTION_TITLE)

                ui.label("Henüz gerçek analiz verisi bağlanmadı. Bu panel daha sonra seçilen veri ve model bilgilerini gösterecek.").classes(MUTED)

    def update_navigation(path: str) -> None:
        path = path.split('?', 1)[0]

        for target, button in nav_buttons.items():
            if path == target:
                button.classes(add='bg-cyan-500/15 text-cyan-400',remove='text-slate-400',)
            else:
                button.classes(add='text-slate-400', remove='bg-cyan-500/15 text-cyan-400',)

    router = ui.context.client.sub_pages_router

    router.on_path_changed(update_navigation)
    update_navigation(router.current_path)



def navigation_button(
    icon: str,
    tooltip: str,
    target: str,
    active: bool = False,
) -> None:

    button_classes = (
        "w-11 h-11 rounded-xl "
        "flex items-center justify-center "
        "transition-colors "
        "text-slate-400 "
        "hover:bg-slate-800 "
        "hover:text-slate-100"
    )

    button = (
        ui.button(
            icon=icon,
            on_click=lambda: ui.navigate.to(target),
        )
        .props('flat round')
        .classes(button_classes)
    )

    button.tooltip(tooltip)

    return button


def context_item(
    label: str,
    value: str,
) -> None:

    with ui.column().classes("gap-1"):
        ui.label(label).classes("text-xs text-slate-500")

        ui.label(value).classes("text-sm font-medium text-slate-200")
