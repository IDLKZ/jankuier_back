from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, List

from pydantic import EmailStr, Field

from app.shared.field_constants import FieldConstants
from app.shared.validation_constants import app_validation


class DTOConstant:
    """
    Системные константы для DTO моделей
    """

    @staticmethod
    def StandardID(description: str | None = "Уникальный идентификатор") -> Annotated:
        return Annotated[int, Field(description=description)]

    @staticmethod
    def StandardTitleField(description: str | None = "Наименование") -> Annotated:
        return Annotated[
            str,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description,
            ),
        ]

    @staticmethod
    def StandardUniqueValueField(description: str | None = None) -> Annotated:
        msg = f"Уникальное значение длиной {FieldConstants.STANDARD_VALUE_LENGTH}"
        return Annotated[
            str,
            Field(
                max_length=FieldConstants.STANDARD_VALUE_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableUniqueValueField(description: str | None = None) -> Annotated:
        msg = f"Уникальное значение длиной {FieldConstants.STANDARD_VALUE_LENGTH}"
        return Annotated[
            str | None,
            Field(
                default=None,
                max_length=FieldConstants.STANDARD_VALUE_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardVarcharField(description: str | None = None) -> Annotated:
        msg = f"Строковое поле до {FieldConstants.STANDARD_LENGTH} символов"
        return Annotated[
            str,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableVarcharField(description: str | None = None) -> Annotated:
        msg = f"Строковое поле до {FieldConstants.STANDARD_LENGTH} символов"
        return Annotated[
            str | None,
            Field(
                default=None,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardIntegerField(description: str | None = None) -> Annotated:
        msg = "Числовое поле"
        return Annotated[
            int,
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableIntegerField(description: str | None = None) -> Annotated:
        msg = "Опциональное числовое поле"
        return Annotated[
            int | None,
            Field(
                default=None,
                nullable=True,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardUnsignedIntegerField(description: str | None = None) -> Annotated:
        msg = "Числовое поле"
        return Annotated[
            int,
            Field(
                ge=0,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableUnsignedIntegerField(
        description: str | None = None,
    ) -> Annotated:
        msg = "Опциональное числовое поле"
        return Annotated[
            int | None,
            Field(
                default=None,
                ge=0,
                nullable=True,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardEmailField(description: str | None = None) -> Annotated:
        msg = "Уникальный адрес электронной почты"
        return Annotated[
            EmailStr,
            Field(
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardPhoneField(description: str | None = None) -> Annotated:
        msg = "Номер телефона"
        return Annotated[
            str,
            Field(
                # pattern=app_validation.KZ_MOBILE_REGEX,
                # max_length=FieldConstants.STANDARD_LENGTH,
                description=description
                or msg,
            ),
        ]

    @staticmethod
    def StandardLoginField(description: str | None = None) -> Annotated:
        msg = "Логин"
        return Annotated[
            str,
            Field(
                pattern=app_validation.LOGIN_REGEX,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardOptionalPasswordField(description: str | None = None) -> Annotated:
        msg = "Пароль (минимум 8 символов,хотя бы один спецсимвол из списка,хотя бы одна цифра,  хотя бы одна большая буква,хотя бы одна маленькая буква)"
        return Annotated[
            str | None,
            Field(
                nullable=True,
                pattern=app_validation.LOGIN_REGEX,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardPasswordField(description: str | None = None) -> Annotated:
        msg = "Пароль (минимум 8 символов, хотя бы один спецсимвол из списка,хотя бы одна цифра,  хотя бы одна большая буква,хотя бы одна маленькая буква)"
        return Annotated[
            str,
            Field(
                pattern=app_validation.LOGIN_REGEX,
                max_length=FieldConstants.STANDARD_LENGTH,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardBooleanTrueField(
        description: str | None = "Флаг активности (по умолчанию True)",
    ) -> Annotated:
        return Annotated[bool, Field(default=True, description=description)]

    @staticmethod
    def StandardBooleanFalseField(
        description: str | None = "Флаг активности (по умолчанию False)",
    ) -> Annotated:
        return Annotated[bool, Field(default=False, description=description)]

    @staticmethod
    def StandardNullableBooleanField(
        description: str | None = "Флаг активности",
    ) -> Annotated:
        return Annotated[bool | None, Field(description=description, default=None)]

    @staticmethod
    def StandardPriceField(description: str | None = None) -> Annotated:
        msg = f"Цена должна быть больше 0 с точностью до {FieldConstants.PRICE_SCALE} знаков"
        return Annotated[
            Decimal,
            Field(
                ge=0,
                decimal_places=FieldConstants.PRICE_SCALE,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullablePriceField(description: str | None = None) -> Annotated:
        msg = f"Опциональная цена больше 0 с точностью до {FieldConstants.PRICE_SCALE} знаков"
        return Annotated[
            Decimal | None,
            Field(
                default=None,
                decimal_places=FieldConstants.PRICE_SCALE,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardFloatField(description: str | None = None) -> Annotated:
        msg = f"Цена должна быть больше 0 с точностью до {FieldConstants.PRICE_SCALE} знаков"
        return Annotated[
            float,
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableFloatField(description: str | None = None) -> Annotated:
        msg = f"Опциональное дробное число"
        return Annotated[
            float | None,
            Field(
                default=None,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardTinyIntegerField(description: str | None = None) -> Annotated:
        msg = "Малое числовое поле (0-255)"
        return Annotated[
            int,
            Field(
                ge=0,
                le=255,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardIntegerDefaultZeroField(description: str | None = None) -> Annotated:
        msg = "Числовое поле со значением по умолчанию 0"
        return Annotated[
            int,
            Field(
                default=0,
                ge=0,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardDecimalField(description: str | None = None) -> Annotated:
        msg = f"Десятичное число с точностью до {FieldConstants.PRICE_SCALE} знаков"
        return Annotated[
            Decimal,
            Field(
                decimal_places=FieldConstants.PRICE_SCALE,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableDecimalField(description: str | None = None) -> Annotated:
        msg = f"Опциональное десятичное число с точностью до {FieldConstants.PRICE_SCALE} знаков"
        return Annotated[
            Decimal | None,
            Field(
                default=None,
                decimal_places=FieldConstants.PRICE_SCALE,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardZeroDecimalField(description: str | None = None) -> Annotated:
        msg = f"Десятичное число с значением по умолчанию 0 и точностью до {FieldConstants.PRICE_SCALE} знаков"
        return Annotated[
            Decimal,
            Field(
                default=0,
                ge=0,
                decimal_places=FieldConstants.PRICE_SCALE,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardJSONField(description: str | None = None) -> Annotated:
        msg = "JSON данные"
        return Annotated[
            dict,
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableJSONField(description: str | None = None) -> Annotated:
        msg = "Опциональные JSON данные"
        return Annotated[
            dict | None,
            Field(
                default=None,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardArrayIntegerField(description: str | None = None) -> Annotated:
        msg = "Массив целых чисел"
        return Annotated[
            List[int],
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardArrayDateField(description: str | None = None) -> Annotated:
        msg = "Массив из дат (гггг-мм-дд) "
        return Annotated[
            List[date],
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableArrayDateField(description: str | None = None) -> Annotated:
        msg = "Массив из дат (гггг-мм-дд) "
        return Annotated[
            List[date]|None,
            Field(
                description=description or msg,
            ),
        ]
    @staticmethod
    def StandardDateField(description: str | None = "Дата") -> Annotated:
        return Annotated[date, Field(description=description)]

    @staticmethod
    def StandardNullableDateField(
        description: str | None = "Опциональная дата",
    ) -> Annotated:
        return Annotated[date | None, Field(default=None, description=description)]

    @staticmethod
    def StandardTimeField(description: str | None = "Время") -> Annotated:
        return Annotated[time, Field(description=description)]

    @staticmethod
    def StandardNullableTimeField(
        description: str | None = "Опциональная время",
    ) -> Annotated:
        return Annotated[time | None, Field(default=None, description=description)]

    @staticmethod
    def StandardDateTimeField(description: str | None = "Дата и время") -> Annotated:
        return Annotated[datetime, Field(description=description)]

    @staticmethod
    def StandardNullableDateTimeField(
        description: str | None = "Опциональная дата и время",
    ) -> Annotated:
        return Annotated[datetime | None, Field(default=None, description=description)]

    @staticmethod
    def StandardNullableIINField(
        description: str | None = "Уникальный идентификатор ИИН",
    ) -> Annotated:
        msg = "Уникальный 12-значный ИИН"
        return Annotated[
            str | None,
            Field(
                nullable=True,
                pattern=app_validation.IIN_REGEX_STR,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardUniqueIINField(
        description: str | None = "Уникальный идентификатор ИИН",
    ) -> Annotated:
        msg = "Уникальный 12-значный ИИН"
        return Annotated[
            str,
            Field(
                pattern=app_validation.IIN_REGEX_STR,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardUniqueBINField(
        description: str | None = "Уникальный идентификатор БИН",
    ) -> Annotated:
        msg = "Уникальный 12-значный БИН"
        return Annotated[
            str,
            Field(
                pattern=app_validation.BIN_REGEX_STR,
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardTextField(description: str | None = "Текстовое описание") -> Annotated:
        return Annotated[str, Field(description=description)]

    @staticmethod
    def StandardNullableTextField(
        description: str | None = "Опциональное текстовое описание",
    ) -> Annotated:
        return Annotated[str | None, Field(default=None, description=description)]

    @staticmethod
    def ProtectedTextField(
        description: str | None = "Опциональное текстовое описание",
    ) -> Annotated:
        return Annotated[
            str | None,
            Field(
                default=None,
                description=description,
                max_length=FieldConstants.STANDARD_LENGTH,
                pattern=app_validation.ONLY_RUSSIAN_KAZAKH_REGEX,
            ),
        ]

    StandardCreatedAt = Annotated[
        datetime, Field(description="Дата создания", example="2024-01-01T12:00:00")
    ]

    StandardUpdatedAt = Annotated[
        datetime, Field(description="Дата обновления", example="2024-01-01T12:00:00")
    ]

    StandardDeletedAt = Annotated[
        datetime | None,
        Field(description="Дата удаления", example="2024-01-01T12:00:00"),
    ]

    @staticmethod
    def StandardStringArrayField(description: List[str]) -> Annotated:
        msg = f"Массив из текстовых данных"
        return Annotated[
            List[str],
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableStringArrayField(
        description: List[str] | None = "Опциональный строковый массив",
    ) -> Annotated:
        return Annotated[List[str] | None, Field(default=None, description=description)]

    @staticmethod
    def StandardIntegerArrayField(description: List[int]) -> Annotated:
        msg = f"Массив из числовых данных"
        return Annotated[
            List[int],
            Field(
                description=description or msg,
            ),
        ]

    @staticmethod
    def StandardNullableIntegerArrayField(
        description: List[int] | None = "Опциональный числовой массив",
    ) -> Annotated:
        return Annotated[List[int] | None, Field(default=None, description=description)]
