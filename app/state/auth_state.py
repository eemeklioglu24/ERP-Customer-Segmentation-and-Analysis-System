from nicegui import app
from nicegui import ui

def is_authenticated() -> bool:
    return app.storage.user.get("authenticated")

def login() -> None:
    app.storage.user["authenticated"] = True

def logout() -> None:
    app.storage.user.clear()

def require_authentication() -> bool:
    if is_authenticated():
        return True
    else:
        ui.navigate.to('/giris')
        return False