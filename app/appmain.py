from nicegui import ui
import os
from dotenv import load_dotenv

from app.pages.home import render_home
from app.styles.theme import apply_theme
from app.state.auth_state import is_authenticated

from app.pages import customers
from app.pages import data_source
from app.pages import home
from app.pages import segmentation
from app.pages import settings
from app.pages import login

@ui.page('/')
def index() -> None:
    if is_authenticated():
        ui.navigate.to('/genel-bakis')
    else:
        ui.navigate.to('/giris')

load_dotenv()
storage_secret = os.getenv('APP_STORAGE_SECRET')
if not storage_secret:
    raise RuntimeError('APP_STORAGE_SECRET ortam değişkeni bulunamadı.')
ui.run(
    title="Müşteri Analitiği",
    host="127.0.0.1",
    storage_secret=storage_secret
)