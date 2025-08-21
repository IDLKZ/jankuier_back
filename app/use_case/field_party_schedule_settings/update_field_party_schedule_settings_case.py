from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import (
    FieldPartyScheduleSettingsUpdateDTO,
    FieldPartyScheduleSettingsWithRelationsRDTO,
)
from app.adapters.repository.field_party_schedule_settings.field_party_schedule_settings_repository import (
    FieldPartyScheduleSettingsRepository,
)
from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyScheduleSettingsEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateFieldPartyScheduleSettingsCase(
    BaseUseCase[FieldPartyScheduleSettingsWithRelationsRDTO]
):
    """
    Класс Use Case для обновления настроек расписания площадки.

    Использует:
        - Репозиторий `FieldPartyScheduleSettingsRepository` для работы с базой данных.
        - Репозиторий `FieldPartyRepository` для проверки существования площадки.
        - DTO `FieldPartyScheduleSettingsUpdateDTO` для входных данных.
        - DTO `FieldPartyScheduleSettingsWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleSettingsRepository): Репозиторий для работы с настройками расписания.
        field_party_repository (FieldPartyRepository): Репозиторий для работы с площадками.
        model (FieldPartyScheduleSettingsEntity | None): Обновляемая модель настроек расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleSettingsRepository(db)
        self.field_party_repository = FieldPartyRepository(db)
        self.model: FieldPartyScheduleSettingsEntity | None = None

    async def execute(
        self, id: int, dto: FieldPartyScheduleSettingsUpdateDTO
    ) -> FieldPartyScheduleSettingsWithRelationsRDTO:
        """
        Выполняет операцию обновления настроек расписания площадки.

        Args:
            id (int): Идентификатор настроек расписания.
            dto (FieldPartyScheduleSettingsUpdateDTO): Данные для обновления настроек расписания.

        Returns:
            FieldPartyScheduleSettingsWithRelationsRDTO: Обновленные настройки расписания с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldPartyScheduleSettingsWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: FieldPartyScheduleSettingsUpdateDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор настроек расписания.
            dto (FieldPartyScheduleSettingsUpdateDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования настроек расписания
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("field_party_schedule_settings_not_found")
            )

        # Валидация рабочих дней (должны быть от 1 до 7)
        if dto.working_days is not None:
            for day in dto.working_days:
                if not isinstance(day, int) or day < 1 or day > 7:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("working_days_validation_error")
                    )

        # Валидация исключенных дат
        if dto.excluded_dates is not None:
            for excluded_date in dto.excluded_dates:
                try:
                    if isinstance(excluded_date, str):
                        date.fromisoformat(excluded_date)
                except (ValueError, TypeError):
                    raise AppExceptionResponse.bad_request(
                        message=f"{i18n.gettext('excluded_dates_format_error')}: {excluded_date}"
                    )

        # Валидация периодов активности
        start_date = (
            dto.active_start_at
            if dto.active_start_at is not None
            else model.active_start_at
        )
        end_date = (
            dto.active_end_at if dto.active_end_at is not None else model.active_end_at
        )

        if start_date >= end_date:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("active_dates_validation_error")
            )

        # Валидация рабочего времени
        if dto.working_time is not None:
            self._validate_time_json(
                dto.working_time, "working_time", ["start_at", "end_at"]
            )

        # Валидация времени перерыва
        if dto.break_time is not None:
            self._validate_time_json(
                dto.break_time, "break_time", ["start_at", "end_at"]
            )

        # Валидация цен по времени
        if dto.price_per_time is not None:
            self._validate_price_time_json(dto.price_per_time)

        # Валидация числовых полей
        if dto.session_minute_int is not None and dto.session_minute_int <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("session_minute_validation_error")
            )

        if (
            dto.break_between_session_int is not None
            and dto.break_between_session_int < 0
        ):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("break_between_session_validation_error")
            )

        if dto.booked_limit is not None and dto.booked_limit <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("booked_limit_validation_error")
            )

    def _validate_time_json(
        self, time_data: any, field_name: str, required_fields: list[str]
    ) -> None:
        """
        Валидация JSON данных времени.

        Args:
            time_data: JSON данные для валидации.
            field_name (str): Название поля для сообщений об ошибках.
            required_fields (list[str]): Обязательные поля в JSON.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        if not isinstance(time_data, (list, dict)):
            raise AppExceptionResponse.bad_request(
                message=f"{field_name} {i18n.gettext('json_format_error')}"
            )

        time_list = time_data if isinstance(time_data, list) else [time_data]

        for item in time_list:
            if not isinstance(item, dict):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("json_object_error").format(
                        field_name=field_name
                    )
                )

            for field in required_fields:
                if field not in item:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("required_field_error").format(
                            field=field, field_name=field_name
                        )
                    )

                # Валидация формата времени (HH:MM)
                time_value = item[field]
                if not isinstance(time_value, str) or not self._is_valid_time_format(
                    time_value
                ):
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("time_format_error").format(
                            field_name=field_name, field=field, value=time_value
                        )
                    )

    def _validate_price_time_json(self, price_data: any) -> None:
        """
        Валидация JSON данных цен по времени.

        Args:
            price_data: JSON данные цен для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        if not isinstance(price_data, (list, dict)):
            raise AppExceptionResponse.bad_request(
                message=f"price_per_time {i18n.gettext('json_format_error')}"
            )

        price_list = price_data if isinstance(price_data, list) else [price_data]

        for item in price_list:
            if not isinstance(item, dict):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("json_object_error").format(
                        field_name="price_per_time"
                    )
                )

            required_fields = ["start_at", "end_at", "price"]
            for field in required_fields:
                if field not in item:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("required_field_error").format(
                            field=field, field_name="price_per_time"
                        )
                    )

            # Валидация времени
            if not self._is_valid_time_format(item["start_at"]):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("time_format_error").format(
                        field_name="price_per_time",
                        field="start_at",
                        value=item["start_at"],
                    )
                )

            if not self._is_valid_time_format(item["end_at"]):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("time_format_error").format(
                        field_name="price_per_time",
                        field="end_at",
                        value=item["end_at"],
                    )
                )

            # Валидация цены
            try:
                price = float(item["price"])
                if price < 0:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("negative_price_error")
                    )
            except (ValueError, TypeError):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("price_format_error").format(
                        price=item["price"]
                    )
                )

    def _is_valid_time_format(self, time_str: str) -> bool:
        """
        Проверка формата времени HH:MM.

        Args:
            time_str (str): Строка времени для проверки.

        Returns:
            bool: True если формат правильный, False иначе.
        """
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False

            hour, minute = parts
            hour_int = int(hour)
            minute_int = int(minute)

            return 0 <= hour_int <= 23 and 0 <= minute_int <= 59
        except (ValueError, AttributeError):
            return False

    async def transform(
        self, id: int, dto: FieldPartyScheduleSettingsUpdateDTO
    ) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор настроек расписания.
            dto (FieldPartyScheduleSettingsUpdateDTO): Данные для преобразования.
        """
        self.model = await self.repository.get(id)
