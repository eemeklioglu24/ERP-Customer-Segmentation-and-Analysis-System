from nicegui import app

def is_authenticated() -> bool:
    return app.storage.user.get("authenticated")

def login() -> None:
    app.storage.user["authenticated"] = True

def logout() -> None:
    app.storage.user.clear()