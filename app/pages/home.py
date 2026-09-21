from nicegui import ui

from app.styles.tokens import (
    PAGE,
    CONTENT,
    CARD,
    CARD_INTERACTIVE,
    EYEBROW,
    PAGE_TITLE,
    SECTION_TITLE,
    BODY,
    MUTED,
    METRIC,
)


def render_home() -> None:

    with ui.column().classes(PAGE):

        with ui.column().classes(CONTENT + " gap-6"):

            # Sayfa başlığı
            with ui.column().classes("gap-1"):
                ui.label("MÜŞTERİ ANALİTİĞİ").classes(EYEBROW)

                ui.label(
                    "Tasarım Sistemi Önizlemesi"
                ).classes(PAGE_TITLE)

                ui.label(
                    "Bu sayfa uygulamanın görsel dilini "
                    "doğrulamak için hazırlanmıştır."
                ).classes(MUTED)

            # Özet metrik kartları
            with ui.grid(columns=3).classes(
                "w-full gap-4"
            ):

                with ui.card().classes(CARD):
                    ui.label("MÜŞTERİLER").classes(EYEBROW)

                    ui.label("12.482").classes(METRIC)

                    ui.label(
                        "Segmentasyona dahil edilen müşteri sayısı"
                    ).classes(MUTED)

                with ui.card().classes(CARD):
                    ui.label("KÜME SAYISI").classes(EYEBROW)

                    ui.label("5").classes(METRIC)

                    ui.label(
                        "Mevcut kümeleme yapılandırması"
                    ).classes(MUTED)

                with ui.card().classes(CARD):
                    ui.label("MODEL DURUMU").classes(EYEBROW)

                    ui.label("HAZIR").classes(
                        "text-3xl font-semibold text-emerald-400"
                    )

                    ui.label(
                        "Analiz başarıyla tamamlandı"
                    ).classes(MUTED)

            # Örnek analiz kartı
            with ui.card().classes(
                CARD_INTERACTIVE + " w-full"
            ):

                ui.label(
                    "Yüksek Değerli Aktif Müşteriler"
                ).classes(SECTION_TITLE)

                ui.label(
                    "Yakın zamanda işlem yapmış, satın alma "
                    "sıklığı ve harcama düzeyi ortalamanın "
                    "üzerinde olan müşteriler."
                ).classes(BODY)

                with ui.row().classes(
                    "items-center gap-3 mt-3"
                ):

                    ui.badge(
                        "YÜKSEK DEĞER",
                        color="primary",
                    )

                    ui.badge(
                        "AKTİF",
                        color="positive",
                    )

                    ui.badge(
                        "MÜŞTERİLERİN %18,4'Ü",
                        color="secondary",
                    )

            # Örnek butonlar
            with ui.row().classes("gap-3"):

                ui.button(
                    "Analizi Başlat",
                    icon="play_arrow",
                    on_click=lambda: ui.notify(
                        "Analiz başlatıldı"
                    ),
                ).props(
                    "unelevated"
                )

                ui.button(
                    "Ayarlar",
                    icon="tune",
                    on_click=lambda: ui.notify(
                        "Ayarlar açıldı"
                    ),
                ).props(
                    "outline color=primary"
                )