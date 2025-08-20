from fastapi import FastAPI

from app.middleware.i18n_middleware import LocaleMiddleware
from app.middleware.logger_middleware import log_requests


def registry_middleware(app: FastAPI):
    app.add_middleware(LocaleMiddleware)
    app.middleware("http")(log_requests)
