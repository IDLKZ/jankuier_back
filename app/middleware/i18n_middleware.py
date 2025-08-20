import os
from babel.support import Translations
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.i18n.i18n_wrapper import AppTranslationsWrapper

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRANSLATIONS_DIR = os.path.join(BASE_DIR, "app", "i18n", "translations")


class LocaleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.translations_dir = os.path.join(BASE_DIR, "app", "i18n", "translations")

    async def dispatch(self, request: Request, call_next) -> Response:
        lang = (
            request.headers.get("Accept-Language", "").split(",")[0].split("-")[0]
            or "ru"
        )

        # print(f"[i18n] Detected lang: {lang}")
        # print(f"[i18n] Looking in: {self.translations_dir}")

        try:
            translations = Translations.load(self.translations_dir, [lang])
            AppTranslationsWrapper.set_gettext(translations.gettext)
            request.state.gettext = translations.gettext
        except Exception as e:
            # print(f"[i18n] Failed to load translations: {e}")
            request.state.gettext = lambda x: x

        return await call_next(request)
