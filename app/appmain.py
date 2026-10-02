from multiprocessing import freeze_support
import secrets
from pathlib import Path
from nicegui import ui, app
import os
from dotenv import load_dotenv

from app.styles.theme import apply_theme
from app.state.auth_state import require_authentication

from app.pages.home import render_dashboard_content
from app.pages.segmentation import render_content
from app.pages.customers import render_customers
from app.pages.data_source import render_data
from app.pages.settings import render_set

from app.components.app_shell import render_app_shell
from app.pages.login import render_login

APP_ROUTES = {
        '/genel-bakis': render_dashboard_content,
        '/segmentasyon': render_content,
        '/musteriler': render_customers,
        '/veri-kaynagi': render_data,
        '/ayarlar': render_set,
}

# The final packaging command is python -m PyInstaller --onefile --noconfirm --clean --windowed  --name MusteriAnalitigi --icon=app\styles\process.ico  app\appmain.py

# @ui.page('/')
# def index() -> None:
    

#     if is_authenticated():
#         ui.navigate.to('/genel-bakis')
#     else:
#         ui.navigate.to('/giris')

@ui.page('/')
@ui.page('/{_:path}')
def application() -> None:
    if not require_authentication():
        return
    
    path = ui.context.client.request.url.path

    if path not in APP_ROUTES:
        ui.navigate.to('/genel-bakis')
        return
    apply_theme()

    render_app_shell(APP_ROUTES)


def get_storage_secret() -> str:
    env_secret = os.getenv('APP_STORAGE_SECRET')

    if env_secret:
        return env_secret

    config_dir = Path.home() / '.musteri_analitigi'
    config_dir.mkdir(exist_ok=True)

    secret_file = config_dir / 'storage_secret.txt'

    if secret_file.exists():
        return secret_file.read_text().strip()
    
    new_secret = secrets.token_urlsafe(32)
    secret_file.write_text(new_secret)

    return new_secret

if __name__ == '__main__':
    freeze_support()
    load_dotenv()
    storage_secret = get_storage_secret()
    app.native.window_args['maximized'] = True

    ui.run(
        title="Müşteri Analitiği",
        host="127.0.0.1",
        storage_secret=storage_secret,
        reload=False,
        native=True,
        favicon="./app/styles/process.ico"
    )