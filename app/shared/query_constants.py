from datetime import datetime

from fastapi import Query

from app.shared.field_constants import FieldConstants
from app.shared.validation_constants import app_validation


class AppQueryConstants:
    """
    Системные значения в Query параметрах
    """

    @staticmethod
    def StandardPerPageQuery(
        description: str | None = "Количество элементов на странице",
    ) -> Query:
        return Query(
            gt=0,
            le=100,
            default=20,
            description=description,
        )

    @staticmethod
    def StandardPageQuery(description: str | None = "Номер страницы") -> Query:
        return Query(
            gt=0,
            default=1,
            description=description,
        )

    @staticmethod
    def StandardOptionalSearchQuery(
        description: str | None = "Поисковый запрос",
    ) -> Query:
        return Query(
            default=None,
            max_length=FieldConstants.STANDARD_LENGTH,
            min_length=2,
            description=description,
        )

    @staticmethod
    def StandardSortFieldQuery(
        description: str | None = "Поле для сортировки",
    ) -> Query:
        return Query(
            default=None,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardSortFieldQuery(  # noqa:F811
        description: str | None = "Сортировать по полю",
    ) -> Query:
        return Query(
            default="id",
            description=description,
        )

    @staticmethod
    def StandardSortDirectionQuery(
        description: str | None = "Направление сортировки (asc/desc)",
    ) -> Query:
        return Query(
            default="asc",
            regex="^(asc|desc)$",
            description=description,
        )

    @staticmethod
    def StandardOptionalIntegerQuery(
        description: str | None = "Опциональное числовое значение",
    ) -> Query:
        return Query(
            default=None,
            gt=0,
            description=description,
        )

    @staticmethod
    def StandardBooleanQuery(description: str | None = "Логическое значение") -> Query:
        return Query(
            default=False,
            description=description,
        )

    @staticmethod
    def StandardOptionalBooleanQuery(
        description: str | None = "Опциональное логическое значение",
    ) -> Query:
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardOptionalStringQuery(
        description: str | None = "Опциональная строка",
    ) -> Query:
        return Query(
            default=None,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardOptionalIINQuery(
        description: str | None = "Опциональная строка ИИН",
    ) -> Query:
        return Query(
            default=None,
            pattern=app_validation.IIN_REGEX,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardOptionalBINQuery(
        description: str | None = "Опциональная строка БИН",
    ) -> Query:
        return Query(
            default=None,
            pattern=app_validation.BIN_REGEX,
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardStringQuery(description: str | None = "Обязательная строка") -> Query:
        return Query(
            max_length=FieldConstants.STANDARD_LENGTH,
            description=description,
        )

    @staticmethod
    def StandardStringArrayQuery(description: str | None = "Массив строк") -> Query:
        return Query(
            default=[],
            description=description,
        )

    @staticmethod
    def StandardOptionalStringArrayQuery(
        description: str | None = "Опциональный массив строк",
    ) -> Query:
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardIntegerArrayQuery(description: str | None = "Массив чисел") -> Query:
        return Query(
            default=[],
            description=description,
        )

    @staticmethod
    def StandardOptionalIntegerArrayQuery(
        description: str | None = "Опциональный массив чисел",
    ) -> Query:
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardOptionalDateQuery(
        description: str | None = "Опциональный дата",
    ) -> Query:
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardOptionalDateTimeQuery(
        description: str | None = "Опциональный datetime",
    ) -> datetime | None:
        return Query(
            default=None,
            description=description,
        )

    @staticmethod
    def StandardForceDeleteQuery(
        description: str | None = "Удалить навсегда?",
    ) -> Query:
        return Query(
            default=None,
            description=description,
        )
