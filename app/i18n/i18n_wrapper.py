from contextvars import ContextVar
from typing import Callable

_current_gettext: ContextVar[Callable[[str], str]] = ContextVar(
    "current_gettext", default=lambda x: x
)


class AppTranslationsWrapper:
    @staticmethod
    def set_gettext(func: Callable[[str], str]) -> None:
        _current_gettext.set(func)

    @staticmethod
    def gettext(message: str) -> str:
        return _current_gettext.get()(message)


# alias for global _
_ = AppTranslationsWrapper.gettext
i18n = AppTranslationsWrapper
