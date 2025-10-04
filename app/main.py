import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles
from app.core.app_cors import set_up_cors
from app.core.file_core import include_static_files
from app.core.role_docs import setup_role_documentation
from app.events import register_events
from app.infrastructure.app_config import app_config
from app.infrastructure.redis_client import check_redis_connection
from app.infrastructure.service.firebase_service.firebase_service import initialize_firebase
from app.middleware.auth_wrapper_core import AuthWrapper
from app.middleware.registry_middleware import registry_middleware
from app.routes.registry_route import enable_routes
from app.seeders.runner import run_seeders
import app.adapters.dto  # Инициализация DTO моделей
from app.adapters.dto.model_rebuilder import ensure_models_rebuilt

# Rebuild Pydantic models with forward references after all DTOs are loaded
ensure_models_rebuilt()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения.
    """
    await run_seeders()
    register_events()
    check_redis_connection()
    await initialize_firebase()
    yield


# Инициализация FastAPI приложения
app = FastAPI(
    title=app_config.app_name,
    description=app_config.app_description,
    version=app_config.app_version,
    lifespan=lifespan,
    debug=True,
    docs_url=app_config.app_docs_url,
    redoc_url=None,
    dependencies=[Depends(AuthWrapper())],
)

registry_middleware(app)
enable_routes(app)
include_static_files(app)

# 📌 Настройка статических файлов
for static_path in [app_config.static_folder, app_config.template]:
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    app.mount(
        f"/{static_path}",
        StaticFiles(directory=f"{static_path}"),
        name=f"{static_path}",
    )

# 🔐 Настройка ролевой системы
setup_role_documentation(app)
# 🌐 Настройка CORS
set_up_cors(app)
# 🚀 Запуск админ панели

async def main():
    print("Starting application ...")


# 🚀 Запуск сервера
if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(
        "main:app", host=app_config.app_host, port=app_config.app_port, reload=True
    )
