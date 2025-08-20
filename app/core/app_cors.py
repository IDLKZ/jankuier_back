from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infrastructure.app_config import app_config


def set_up_cors(app: FastAPI):
    """
    Регистрирует CORS конфигурацию в приложении
    """
    if app_config.app_cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=app_config.cors_allowed_origins,
            allow_credentials=app_config.cors_allow_credentials,
            allow_methods=app_config.cors_allowed_methods,
            allow_headers=app_config.cors_allowed_headers,
        )
