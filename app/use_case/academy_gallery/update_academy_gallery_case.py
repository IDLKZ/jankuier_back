from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_gallery.academy_gallery_dto import (
    AcademyGalleryUpdateDTO,
    AcademyGalleryWithRelationsRDTO,
)
from app.adapters.repository.academy_gallery.academy_gallery_repository import (
    AcademyGalleryRepository,
)
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateAcademyGalleryCase(BaseUseCase[AcademyGalleryWithRelationsRDTO]):
    """
    Класс Use Case для обновления изображения в галерее академии.

    Использует:
        - Репозиторий `AcademyGalleryRepository` для работы с базой данных.
        - Репозиторий `AcademyGroupRepository` для проверки существования группы.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyGalleryUpdateDTO` для входных данных.
        - DTO `AcademyGalleryWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGalleryRepository): Репозиторий для работы с галереей академий.
        group_repository (AcademyGroupRepository): Репозиторий для работы с группами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyGalleryEntity | None): Обновляемая модель галереи.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGalleryRepository(db)
        self.group_repository = AcademyGroupRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyGalleryEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, dto: AcademyGalleryUpdateDTO, file: UploadFile | None = None
    ) -> AcademyGalleryWithRelationsRDTO:
        """
        Выполняет операцию обновления изображения в галерее академии.

        Args:
            id (int): Идентификатор изображения галереи.
            dto (AcademyGalleryUpdateDTO): Данные для обновления изображения.
            file (UploadFile | None): Новый файл изображения.

        Returns:
            AcademyGalleryWithRelationsRDTO: Обновленное изображение галереи с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyGalleryWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: AcademyGalleryUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор изображения галереи.
            dto (AcademyGalleryUpdateDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования изображения галереи
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_gallery_not_found")
            )

        # Проверка существования новой группы (если изменяется)
        if dto.group_id is not None:
            if dto.group_id:  # Если не None и не 0
                group = await self.group_repository.get(dto.group_id)
                if not group:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("academy_group_not_found")
                    )

                # Проверка, что группа принадлежит той же академии
                if group.academy_id != model.academy_id:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("academy_group_not_found")
                    )

        # Проверка нового файла изображения (если загружается)
        if file:
            # Валидация типа и размера файла
            self.file_service.validate_file(file, self.extensions)

            # Дополнительная проверка на тип изображения
            if not any(file.filename.lower().endswith(ext) for ext in self.extensions):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("academy_gallery_invalid_file_type")
                )

        # Проверка существования нового файла по ID (если обновляется)
        if dto.file_id is not None and dto.file_id:
            existing_file = await self.file_repository.get(dto.file_id)
            if not existing_file:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found")
                )

            # Проверка на дублирование: этот файл уже не должен быть в галерее данной академии
            # (исключаем текущую запись)
            duplicate_gallery_item = await self.repository.get_first_with_filters(
                filters=[
                    self.repository.model.academy_id == model.academy_id,
                    self.repository.model.file_id == dto.file_id,
                    self.repository.model.id != id,  # Исключаем текущую запись
                ]
            )
            if duplicate_gallery_item:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("academy_gallery_duplicate_file")
                )

    async def transform(
        self, id: int, dto: AcademyGalleryUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор изображения галереи.
            dto (AcademyGalleryUpdateDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        self.model = await self.repository.get(id)

        # Обработка нового файла изображения
        if file:
            # Удаление старого файла (если есть)
            if self.model.file_id:
                await self.file_service.delete_file(file_id=self.model.file_id)

            # Определяем папку для загрузки на основе академии и группы
            academy_value = (
                self.model.academy.value
                if self.model.academy.value
                else str(self.model.academy_id)
            )

            # Определяем группу для папки (берем обновленную или текущую)
            target_group_id = (
                dto.group_id if dto.group_id is not None else self.model.group_id
            )

            if target_group_id:
                group = await self.group_repository.get(target_group_id)
                group_value = group.value if group.value else str(target_group_id)
                self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/academy_galleries/{academy_value}/groups/{group_value}"
            else:
                self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/academy_galleries/{academy_value}"

            # Сохраняем новый файл
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id
