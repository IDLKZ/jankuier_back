from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_gallery.field_gallery_dto import (
    FieldGalleryUpdateDTO,
    FieldGalleryWithRelationsRDTO,
)
from app.adapters.repository.field_gallery.field_gallery_repository import (
    FieldGalleryRepository,
)
from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateFieldGalleryCase(BaseUseCase[FieldGalleryWithRelationsRDTO]):
    """
    Класс Use Case для обновления изображения в галерее поля.

    Использует:
        - Репозиторий `FieldGalleryRepository` для работы с базой данных.
        - Репозиторий `FieldPartyRepository` для проверки существования площадки.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `FieldGalleryUpdateDTO` для входных данных.
        - DTO `FieldGalleryWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldGalleryRepository): Репозиторий для работы с галереей.
        field_party_repository (FieldPartyRepository): Репозиторий для работы с площадками.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldGalleryEntity | None): Обновляемая модель изображения галереи.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldGalleryRepository(db)
        self.field_party_repository = FieldPartyRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: FieldGalleryEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, dto: FieldGalleryUpdateDTO, file: UploadFile | None = None
    ) -> FieldGalleryWithRelationsRDTO:
        """
        Выполняет операцию обновления изображения в галерее поля.

        Args:
            id (int): Идентификатор изображения галереи.
            dto (FieldGalleryUpdateDTO): Данные для обновления изображения галереи.
            file (UploadFile | None): Новый файл изображения для загрузки.

        Returns:
            FieldGalleryWithRelationsRDTO: Обновленное изображение галереи с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldGalleryWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: FieldGalleryUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор изображения галереи.
            dto (FieldGalleryUpdateDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования изображения галереи
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("field_gallery_not_found")
            )

        # Проверка существования площадки (если указана для обновления)
        if dto.party_id is not None:
            if dto.party_id:  # Если не None и не 0
                field_party = await self.field_party_repository.get(dto.party_id)
                if not field_party:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("field_party_not_found")
                    )

                # Проверяем, что площадка принадлежит тому же полю
                if field_party.field_id != model.field_id:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("field_party_not_found")
                    )

        # Валидация нового файла изображения (если загружается)
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID (если указан для обновления)
        if dto.file_id is not None and dto.file_id:
            file_entity = await self.file_repository.get(dto.file_id)
            if not file_entity:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found")
                )

            # Проверяем, что файл является изображением
            if not self._is_image_file(file_entity.filename):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("invalid_file_type_for_gallery")
                )

        # Проверка на дублирование (если обновляется file_id)
        if dto.file_id is not None and dto.file_id:
            await self._check_duplicate_image(id, model, dto)

    async def _check_duplicate_image(
        self, id: int, model: FieldGalleryEntity, dto: FieldGalleryUpdateDTO
    ) -> None:
        """
        Проверка на дублирование изображения в галерее.

        Args:
            id (int): ID текущего изображения галереи (исключаем из проверки).
            model (FieldGalleryEntity): Текущая модель изображения галереи.
            dto (FieldGalleryUpdateDTO): Данные для обновления.

        Raises:
            AppExceptionResponse: Если изображение уже добавлено в галерею.
        """
        # Определяем финальные значения после обновления
        party_id = dto.party_id if dto.party_id is not None else model.party_id
        file_id = dto.file_id if dto.file_id is not None else model.file_id

        existing_gallery = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    FieldGalleryEntity.id != id,  # Исключаем текущее изображение
                    FieldGalleryEntity.field_id == model.field_id,
                    FieldGalleryEntity.file_id == file_id,
                    FieldGalleryEntity.party_id == party_id,
                )
            ]
        )

        if existing_gallery:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("duplicate_gallery_image_error")
            )

    def _is_image_file(self, filename: str) -> bool:
        """
        Проверка, является ли файл изображением по расширению.

        Args:
            filename (str): Имя файла.

        Returns:
            bool: True если файл является изображением.
        """
        if not filename:
            return False

        # Получаем расширение файла
        extension = "." + filename.split(".")[-1].lower() if "." in filename else ""
        return extension in self.extensions

    async def transform(
        self, id: int, dto: FieldGalleryUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор изображения галереи.
            dto (FieldGalleryUpdateDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        self.model = await self.repository.get(id)

        # Сохранение нового файла изображения
        if file:
            # Удаление старого файла (если есть)
            if self.model.file_id:
                await self.file_service.delete_file(file_id=self.model.file_id)

            # Определяем папку для загрузки
            if (
                self.model.field
                and hasattr(self.model.field, "value")
                and self.model.field.value
            ):
                self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/gallery/{self.model.field.value}"
            else:
                self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/gallery/{self.model.field_id}"

            # Сохраняем новый файл
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id
