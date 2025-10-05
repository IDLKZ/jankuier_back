import logging
from fastapi import HTTPException, status
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config

class AppExceptionResponse:
    """Утилита для создания стандартных HTTP-исключений."""

    logger = logging.getLogger("AppExceptionResponse")

    @staticmethod
    def create_exception(
        status_code: int,
        message: str,
        extra: dict | None = None,
        is_custom: bool = True,
    ) -> HTTPException:
        detail = {"message": message, "is_custom": is_custom}
        if extra:
            detail.update(extra)

        # Лог в JSON-подобном формате
        AppExceptionResponse.logger.error({
            "status_code": status_code,
            "message": message,
            "extra": extra,
        })

        return HTTPException(status_code=status_code, detail=detail)

    @staticmethod
    def bad_request(message: str = i18n.gettext("bad_request"), extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_400_BAD_REQUEST, message=message, extra=extra
        )

    @staticmethod
    def unauthorized(message: str = i18n.gettext("unauthorized"), extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_401_UNAUTHORIZED, message=message, extra=extra
        )

    @staticmethod
    def forbidden(message: str = i18n.gettext("forbidden"), extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_403_FORBIDDEN, message=message, extra=extra
        )

    @staticmethod
    def not_found(message: str = i18n.gettext("not_found"), extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_404_NOT_FOUND, message=message, extra=extra
        )

    @staticmethod
    def conflict(message: str = i18n.gettext("conflict_occurred"), extra: dict | None = None):
        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_409_CONFLICT, message=message, extra=extra
        )

    @staticmethod
    def internal_error(
        message: str = i18n.gettext("internal_server_error"),
        extra: dict | None = None,
        is_custom: bool = False,
    ):
        if app_config.app_status.lower() == "production":
            if extra is None:
                extra = {}
            extra["details"] = "Ошибка сервиса"  # скрываем детали в проде

        return AppExceptionResponse.create_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            extra=extra,
            is_custom=is_custom,
        )
