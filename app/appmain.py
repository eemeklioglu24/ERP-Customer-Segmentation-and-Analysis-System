from nicegui import ui

from app.pages.home import render_home
from app.styles.theme import apply_theme

from app.pages import customers
from app.pages import data_source
from app.pages import home
from app.pages import segmentation
from app.pages import settings

@ui.page('/')
def index() -> None:
    ui.navigate.to('/genel-bakis')


ui.run(
    title="Müşteri Analitiği",
    host="127.0.0.1"
)