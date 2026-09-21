from nicegui import ui

from app.pages.home import render_home
from app.styles.theme import apply_theme


def create_app() -> None:
    apply_theme()
    render_home()


create_app()

ui.run(
    title="Müşteri Analitiği",
    host="127.0.0.1"
)