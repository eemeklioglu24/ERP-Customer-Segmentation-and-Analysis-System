from nicegui import ui

from app.components.app_shell import render_app_shell
from app.styles.theme import apply_theme
from app.styles.tokens import (
    BODY,
    CARD,
    EYEBROW,
    MUTED,
    PAGE_TITLE,
    SECTION_TITLE,
)

@ui.page('/genel-bakis')
def render_home() -> None:
    apply_theme()

    render_app_shell(
        render_dashboard_content,
        active_page='genel-bakis',
    )

def render_dashboard_content() -> None:

    with ui.column().classes(
        "w-full gap-6"
    ):

        # Sayfa başlığı
        with ui.column().classes(
            "gap-1"
        ):

            ui.label(
                "GENEL BAKIŞ"
            ).classes(EYEBROW)

            ui.label(
                "Müşteri Segmentasyonu"
            ).classes(PAGE_TITLE)

            ui.label(
                "Müşteri davranışlarını analiz edin, "
                "segmentleri inceleyin ve model sonuçlarını değerlendirin."
            ).classes(MUTED)

        # Analiz süreci
        with ui.card().classes(
            CARD + " w-full"
        ):

            ui.label(
                "Analiz Süreci"
            ).classes(SECTION_TITLE)

            ui.label(
                "Uygulama müşteri segmentasyonu sürecini "
                "beş temel aşamada yönetir."
            ).classes(BODY)

            with ui.row().classes(
                "w-full items-center gap-3 mt-4"
            ):

                workflow_step(
                    "01",
                    "Veri",
                    active=True,
                )

                workflow_arrow()

                workflow_step(
                    "02",
                    "Özellikler",
                )

                workflow_arrow()

                workflow_step(
                    "03",
                    "Model",
                )

                workflow_arrow()

                workflow_step(
                    "04",
                    "Yorumlama",
                )

                workflow_arrow()

                workflow_step(
                    "05",
                    "Keşif",
                )

        # Geçici içerik
        with ui.card().classes(
            CARD + " w-full min-h-72"
        ):

            ui.label(
                "Çalışma Alanı"
            ).classes(SECTION_TITLE)

            ui.label(
                "Gerçek analiz bileşenleri sonraki adımlarda "
                "bu alana yerleştirilecek."
            ).classes(MUTED)


def workflow_step(
    number: str,
    label: str,
    active: bool = False,
) -> None:

    if active:
        container_classes = (
            "border-cyan-500/50 "
            "bg-cyan-500/10"
        )

        number_classes = (
            "text-cyan-400"
        )
    else:
        container_classes = (
            "border-slate-800 "
            "bg-slate-900"
        )

        number_classes = (
            "text-slate-500"
        )

    with ui.column().classes(
        "flex-1 p-3 rounded-xl border gap-1 "
        + container_classes
    ):

        ui.label(
            number
        ).classes(
            "text-xs font-semibold "
            + number_classes
        )

        ui.label(
            label
        ).classes(
            "text-sm font-medium"
        )


def workflow_arrow() -> None:
    ui.icon(
        "arrow_forward",
        size="18px",
    ).classes(
        "text-slate-600"
    )