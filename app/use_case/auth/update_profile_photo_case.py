from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateProfilePhotoCase(BaseUseCase[UserWithRelationsRDTO]):
    """
    Use case для обновления фото профиля пользователя.

    Атрибуты:
        repository (UserRepository): Репозиторий для работы с пользователями.
        file_service (FileService): Сервис для работы с файлами.
        user_id (int): ID пользователя для обновления фото.
        model: Модель пользователя.
        upload_folder (str): Папка для загрузки фото профиля.
        extensions (dict): Допустимые расширения файлов.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)
        self.file_service = FileService(db)
        self.user_id: int | None = None
        self.model = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(self, user_id: int, file: UploadFile) -> UserWithRelationsRDTO:
        self.user_id = user_id
        await self.validate(file)
        dto = await self.transform(file)

        updated_model = await self.repository.update(obj=self.model, dto=dto)
        if updated_model:
            updated_model = await self.repository.get(
                id=updated_model.id,
                options=self.repository.default_relationships(),
                include_deleted_filter=True
            )
            return UserWithRelationsRDTO.from_orm(updated_model)

        raise AppExceptionResponse.internal_error(
            message=i18n.gettext("something_went_wrong")
        )

    async def validate(self, file: UploadFile) -> None:
        # Проверяем, что пользователь существует
        self.model = await self.repository.get(id=self.user_id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Проверяем файл, если он передан
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Формируем папку для загрузки на основе username пользователя
        self.upload_folder = AppFileExtensionConstants.user_profile_photo_directory(
            self.model.username
        )

    async def transform(self, file: UploadFile) -> dict:
        """
        Обрабатываем загрузку файла и возвращаем данные для обновления.

        :param file: Загружаемый файл
        :return: Словарь с данными для обновления пользователя
        """
        dto = {}

        if file:
            if self.model.image_id:
                # Обновляем существующий файл
                file_entity = await self.file_service.update_file(
                    file_id=self.model.image_id,
                    new_file=file,
                    uploaded_folder=self.upload_folder,
                    extensions=self.extensions,
                )
            else:
                # Создаем новый файл
                file_entity = await self.file_service.save_file(
                    file=file,
                    uploaded_folder=self.upload_folder,
                    extensions=self.extensions,
                )
            dto["image_id"] = file_entity.id

        return dto

    async def delete_photo(self, user_id: int) -> UserWithRelationsRDTO:
        """
        Удаляет фото профиля пользователя.

        :param user_id: ID пользователя
        :return: Обновленные данные пользователя
        """
        self.user_id = user_id

        # Проверяем, что пользователь существует
        self.model = await self.repository.get(id=self.user_id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Удаляем файл, если он есть
        if self.model.image_id:
            await self.file_service.delete_file(file_id=self.model.image_id)

            # Обновляем пользователя, убирая ссылку на файл
            updated_model = await self.repository.update(
                obj=self.model,
                dto={"image_id": None}
            )

            if updated_model:
                updated_model = await self.repository.get(
                    id=updated_model.id,
                    options=self.repository.default_relationships(),
                    include_deleted_filter=True
                )
                return UserWithRelationsRDTO.from_orm(updated_model)

        # Если файла нет, просто возвращаем данные пользователя
        return UserWithRelationsRDTO.from_orm(self.model)