from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteAcademyGroupCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления группы академии.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - Сервис `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyGroupEntity | None): Удаляемая модель группы академии.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyGroupEntity | None = None

    async def execute(
        self, id: int, force_delete: bool = False, delete_image: bool = True
    ) -> bool:
        """
        Выполняет операцию удаления группы академии.

        Args:
            id (int): Идентификатор группы академии для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).
            delete_image (bool): Удалять ли связанное изображение (по умолчанию True).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, force_delete=force_delete)

        # Удаление связанного изображения (если требуется и изображение существует)
        if delete_image and self.model.image_id:
            await self.file_service.delete_file(file_id=self.model.image_id)

        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор группы академии для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_group_id_validation_error")
            )

        # Проверка существования группы академии
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_group_not_found")
            )

        # Бизнес-правила для удаления
        if not force_delete:
            # Проверка на существование связанных студентов
            # Проверка на существование активных расписаний
            # Другие бизнес-ограничения

            # Примеры проверок (можно реализовать через дополнительные запросы):
            # - Есть ли активные студенты в группе
            # - Есть ли будущие расписания занятий
            # - Другие связанные записи, которые могут препятствовать удалению

            # Пока заглушка - можно добавить конкретную логику
            pass

        self.model = model

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
