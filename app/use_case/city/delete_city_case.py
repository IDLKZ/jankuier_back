from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.city.city_repository import CityRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CityEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteCityByIdCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления города по ID.

    Использует:
        - Репозиторий `CityRepository` для работы с базой данных.

    Атрибуты:
        repository (CityRepository): Репозиторий для работы с городами.
        model (CityEntity | None): Удаляемая модель города.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет город и возвращает результат операции.
        validate(id: int):
            Проверяет существование города.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CityRepository(db)
        self.model: CityEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления города.

        Args:
            id (int): Идентификатор города.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если город не найден.
        """
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)
        return result

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор города для проверки.

        Raises:
            AppExceptionResponse: Если город не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))