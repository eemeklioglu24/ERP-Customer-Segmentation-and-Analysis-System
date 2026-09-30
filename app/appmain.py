from multiprocessing import freeze_support
import secrets
from pathlib import Path
from nicegui import ui
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
        print('Using APP_STORAGE_SECRET from environment')
        return env_secret

    print('APP_STORAGE_SECRET not found; using local generated secret')

    config_dir = Path.home() / '.musteri_analitigi'
    config_dir.mkdir(exist_ok=True)

    secret_file = config_dir / 'storage_secret.txt'

    if secret_file.exists():
        print('Using previously generated local secret')
        return secret_file.read_text().strip()

    print('Creating new local secret')
    new_secret = secrets.token_urlsafe(32)
    secret_file.write_text(new_secret)

    return new_secret

if __name__ == '__main__':
    freeze_support()
    load_dotenv()
    storage_secret = os.getenv('APP_STORAGE_SECRET')

    if not storage_secret:
        raise RuntimeError('APP_STORAGE_SECRET ortam değişkeni bulunamadı.')
    ui.run(
        title="Müşteri Analitiği",
        host="127.0.0.1",
        storage_secret=storage_secret,
        reload=False
    )