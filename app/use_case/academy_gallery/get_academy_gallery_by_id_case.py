from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_gallery.academy_gallery_dto import AcademyGalleryRDTO
from app.adapters.repository.academy_gallery.academy_gallery_repository import (
    AcademyGalleryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyGalleryByIdCase(BaseUseCase[AcademyGalleryRDTO]):
    """
    Класс Use Case для получения изображения галереи академии по ID.

    Использует:
        - Репозиторий `AcademyGalleryRepository` для работы с базой данных.
        - DTO `AcademyGalleryRDTO` для возврата данных.

    Атрибуты:
        repository (AcademyGalleryRepository): Репозиторий для работы с галереей академий.

    Методы:
        execute() -> AcademyGalleryRDTO:
            Выполняет запрос и возвращает изображение галереи по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGalleryRepository(db)

    async def execute(self, id: int) -> AcademyGalleryRDTO:
        """
        Выполняет операцию получения изображения галереи академии по ID.

        Args:
            id (int): ID изображения галереи.

        Returns:
            AcademyGalleryRDTO: Объект изображения галереи.

        Raises:
            AppExceptionResponse: Если изображение галереи не найдено.
        """
        await self.validate(id)

        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_gallery_not_found")
            )

        return AcademyGalleryRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID изображения галереи для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_gallery_id_validation_error")
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
