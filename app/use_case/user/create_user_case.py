from fastapi import UploadFile
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.user.user_dto import UserCDTO, UserWithRelationsRDTO
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.role.role_repository import RoleRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_password_hash
from app.entities import UserEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class CreateUserCase(BaseUseCase[UserWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
        self.file_service = FileService(db)
        self.file_repository = FileRepository(db)
        self.model: UserEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: UserCDTO, file: UploadFile | None = None
    ) -> UserWithRelationsRDTO:
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return UserWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: UserCDTO, file: UploadFile | None = None) -> None:
        user = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    func.lower(self.repository.model.username) == dto.username.lower(),
                    func.lower(self.repository.model.email) == dto.email.lower(),
                    func.lower(self.repository.model.phone) == dto.phone.lower(),
                    func.lower(self.repository.model.iin) == dto.iin.lower(),
                )
            ],
            include_deleted_filter=True
        )
        if user:
            if user.email.lower() == dto.email.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("email_exists")
                )
            if user.username.lower() == dto.username.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("username_exists")
                )
            if user.phone.lower() == dto.phone.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("phone_exists")
                )
            if user.iin.lower() == dto.iin.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("iin_exists")
                )
        if (await self.role_repository.get(dto.role_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("role_not_found_by_id")
            )
        if file:
            self.file_service.validate_file(file, self.extensions)

        if dto.image_id:
            if (await self.file_repository.get(dto.image_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(self, dto: UserCDTO, file: UploadFile | None = None):
        self.upload_folder = AppFileExtensionConstants.user_profile_photo_directory(
            dto.username
        )
        if dto.password_hash:
            dto.password_hash = get_password_hash(dto.password_hash)
        if file:
            file = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file.id

        self.model = UserEntity(**dto.dict())
