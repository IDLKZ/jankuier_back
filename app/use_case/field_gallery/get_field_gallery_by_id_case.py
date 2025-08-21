from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryRDTO
from app.adapters.repository.field_gallery.field_gallery_repository import (
    FieldGalleryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFieldGalleryByIdCase(BaseUseCase[FieldGalleryRDTO]):
    """
    Класс Use Case для получения изображения галереи поля по ID.

    Использует:
        - Репозиторий `FieldGalleryRepository` для работы с базой данных.
        - DTO `FieldGalleryRDTO` для возврата данных.

    Атрибуты:
        repository (FieldGalleryRepository): Репозиторий для работы с галереей полей.

    Методы:
        execute() -> FieldGalleryRDTO:
            Выполняет запрос и возвращает изображение галереи поля по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldGalleryRepository(db)

    async def execute(self, id: int) -> FieldGalleryRDTO:
        """
        Выполняет операцию получения изображения галереи поля по ID.

        Args:
            id (int): ID изображения галереи поля.

        Returns:
            FieldGalleryRDTO: Объект изображения галереи поля.

        Raises:
            AppExceptionResponse: Если изображение галереи поля не найдено.
        """
        await self.validate(id)

        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("field_gallery_not_found")
            )

        return FieldGalleryRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID изображения галереи поля для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("gallery_id_validation_error")
            )
