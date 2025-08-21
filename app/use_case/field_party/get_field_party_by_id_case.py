from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party.field_party_dto import FieldPartyWithRelationsRDTO
from app.adapters.repository.field_party.field_party_repository import FieldPartyRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFieldPartyByIdCase(BaseUseCase[FieldPartyWithRelationsRDTO]):
    """
    Класс Use Case для получения площадки поля по ID.

    Использует:
        - Репозиторий `FieldPartyRepository` для работы с базой данных.
        - DTO `FieldPartyWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyRepository): Репозиторий для работы с площадками полей.
        model (FieldPartyEntity | None): Найденная модель площадки поля.

    Методы:
        execute(id: int) -> FieldPartyWithRelationsRDTO:
            Выполняет поиск площадки поля по ID и возвращает DTO.
        validate(id: int):
            Проверяет существование площадки поля с указанным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyRepository(db)
        self.model: FieldPartyEntity | None = None

    async def execute(self, id: int) -> FieldPartyWithRelationsRDTO:
        """
        Выполняет операцию получения площадки поля по ID.

        Args:
            id (int): Идентификатор площадки поля.

        Returns:
            FieldPartyWithRelationsRDTO: Объект площадки поля с связями.

        Raises:
            AppExceptionResponse: Если площадка поля не найдена.
        """
        await self.validate(id=id)
        return FieldPartyWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор площадки поля для проверки.

        Raises:
            AppExceptionResponse: Если площадка поля не найдена.
        """
        self.model = await self.repository.get(
            id, 
            options=self.repository.default_relationships(),
            include_deleted_filter=True
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))