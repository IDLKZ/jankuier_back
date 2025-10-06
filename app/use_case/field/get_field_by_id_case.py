from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field.field_dto import FieldWithRelationsRDTO
from app.adapters.repository.field.field_repository import FieldRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFieldByIdCase(BaseUseCase[FieldWithRelationsRDTO]):
    """
    Класс Use Case для получения поля по ID.

    Использует:
        - Репозиторий `FieldRepository` для работы с базой данных.
        - DTO `FieldWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldRepository): Репозиторий для работы с полями.
        model (FieldEntity | None): Найденная модель поля.

    Методы:
        execute(id: int) -> FieldWithRelationsRDTO:
            Выполняет поиск поля по ID и возвращает DTO.
        validate(id: int):
            Проверяет существование поля с указанным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldRepository(db)
        self.model: FieldEntity | None = None

    async def execute(self, id: int) -> FieldWithRelationsRDTO:
        """
        Выполняет операцию получения поля по ID.

        Args:
            id (int): Идентификатор поля.

        Returns:
            FieldWithRelationsRDTO: Объект поля с связями.

        Raises:
            AppExceptionResponse: Если поле не найдено.
        """
        await self.validate(id=id)
        return FieldWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор поля для проверки.

        Raises:
            AppExceptionResponse: Если поле не найдено.
        """
        self.model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
