from nicegui import app
from nicegui import ui
from app.services.result_storage import service
from src.erp.db_connection import test_connection

def is_authenticated() -> bool:
    return app.storage.user.get("authenticated")

def login() -> None:
    app.storage.user["authenticated"] = True

def logout() -> None:
    app.storage.user.clear()
    service.reset_fake_data()

def require_authentication() -> bool:
    if service.has_fake_data:
        return True
    else:
        if not is_authenticated():
            ui.navigate.to('/giris')
            return False

        if service.db_config is None:
            service.is_connected = False
            logout()
            ui.navigate.to('/giris')
            return False

        if not test_connection(service.db_config):
            service.is_connected = False
            logout()
            ui.navigate.to('/giris')
            return False

    return True