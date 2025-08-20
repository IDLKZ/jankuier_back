# 📌 Настройка статических файлов
import os
from starlette.staticfiles import StaticFiles
from app.infrastructure.app_config import app_config


def include_static_files(app):
    for static_path in [app_config.static_folder, app_config.template]:
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        clean_static_path = static_path.strip("/")  # удаляет начальный слэш
        app.mount(
            f"/{clean_static_path}",
            StaticFiles(directory=static_path),
            name=clean_static_path,
        )
