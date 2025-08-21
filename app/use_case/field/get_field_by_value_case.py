from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field.field_dto import FieldWithRelationsRDTO
from app.adapters.repository.field.field_repository import FieldRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFieldByValueCase(BaseUseCase[FieldWithRelationsRDTO]):
    """
    Класс Use Case для получения поля по уникальному значению.

    Использует:
        - Репозиторий `FieldRepository` для работы с базой данных.
        - DTO `FieldWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldRepository): Репозиторий для работы с полями.
        model (FieldEntity | None): Найденная модель поля.

    Методы:
        execute(value: str) -> FieldWithRelationsRDTO:
            Выполняет поиск поля по значению и возвращает DTO.
        validate(value: str):
            Проверяет существование поля с указанным значением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldRepository(db)
        self.model: FieldEntity | None = None

    async def execute(self, value: str) -> FieldWithRelationsRDTO:
        """
        Выполняет операцию получения поля по значению.

        Args:
            value (str): Уникальное значение поля.

        Returns:
            FieldWithRelationsRDTO: Объект поля с связями.

        Raises:
            AppExceptionResponse: Если поле не найдено.
        """
        await self.validate(value=value)
        return FieldWithRelationsRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        """
        Валидация перед выполнением.

        Args:
            value (str): Уникальное значение поля для проверки.

        Raises:
            AppExceptionResponse: Если поле не найдено.
        """
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
