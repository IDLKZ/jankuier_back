from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryCDTO, FieldGalleryWithRelationsRDTO
from app.adapters.repository.field_gallery.field_gallery_repository import FieldGalleryRepository
from app.adapters.repository.field.field_repository import FieldRepository
from app.adapters.repository.field_party.field_party_repository import FieldPartyRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class CreateFieldGalleryCase(BaseUseCase[FieldGalleryWithRelationsRDTO]):
    """
    Класс Use Case для создания нового изображения в галерее поля.

    Использует:
        - Репозиторий `FieldGalleryRepository` для работы с базой данных.
        - Репозиторий `FieldRepository` для проверки существования поля.
        - Репозиторий `FieldPartyRepository` для проверки существования площадки.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `FieldGalleryCDTO` для входных данных.
        - DTO `FieldGalleryWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldGalleryRepository): Репозиторий для работы с галереей.
        field_repository (FieldRepository): Репозиторий для работы с полями.
        field_party_repository (FieldPartyRepository): Репозиторий для работы с площадками.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldGalleryEntity | None): Созданная модель изображения галереи.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldGalleryRepository(db)
        self.field_repository = FieldRepository(db)
        self.field_party_repository = FieldPartyRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: FieldGalleryEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: FieldGalleryCDTO, file: UploadFile | None = None
    ) -> FieldGalleryWithRelationsRDTO:
        """
        Выполняет операцию создания изображения в галерее поля.

        Args:
            dto (FieldGalleryCDTO): Данные для создания изображения галереи.
            file (UploadFile | None): Файл изображения для загрузки.

        Returns:
            FieldGalleryWithRelationsRDTO: Созданное изображение галереи с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldGalleryWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: FieldGalleryCDTO, file: UploadFile | None = None) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (FieldGalleryCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования поля
        field = await self.field_repository.get(dto.field_id)
        if not field:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("field_not_found")
            )

        # Проверка существования площадки (если указана)
        if dto.party_id:
            field_party = await self.field_party_repository.get(dto.party_id)
            if not field_party:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("field_party_not_found")
                )

            # Проверяем, что площадка принадлежит указанному полю
            if field_party.field_id != dto.field_id:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("field_party_not_found")
                )

        # Валидация файла изображения (если загружается новый файл)
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID (если указан)
        if dto.file_id:
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

        # Проверка на дублирование (один файл не может быть добавлен дважды в галерею)
        if dto.file_id:
            await self._check_duplicate_image(dto)

    async def _check_duplicate_image(self, dto: FieldGalleryCDTO) -> None:
        """
        Проверка на дублирование изображения в галерее.

        Args:
            dto (FieldGalleryCDTO): Данные для проверки.

        Raises:
            AppExceptionResponse: Если изображение уже добавлено в галерею.
        """
        existing_gallery = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    FieldGalleryEntity.field_id == dto.field_id,
                    FieldGalleryEntity.file_id == dto.file_id,
                    FieldGalleryEntity.party_id == dto.party_id
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

    async def transform(self, dto: FieldGalleryCDTO, file: UploadFile | None = None) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (FieldGalleryCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Сохранение нового файла изображения
        if file:
            # Определяем папку для загрузки на основе поля
            field = await self.field_repository.get(dto.field_id)
            if field and hasattr(field, 'value') and field.value:
                self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/gallery/{field.value}"
            else:
                self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/gallery/{dto.field_id}"

            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id

        self.model = FieldGalleryEntity(**dto.dict())