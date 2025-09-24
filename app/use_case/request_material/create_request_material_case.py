from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_material.request_material_dto import (
    RequestMaterialCDTO,
    RequestMaterialWithRelationsRDTO,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.request_material.request_material_repository import (
    RequestMaterialRepository,
)
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import (
    RequestToAcademyGroupRepository,
)
from app.adapters.repository.student.student_repository import StudentRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestMaterialEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class CreateRequestMaterialCase(BaseUseCase[RequestMaterialWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RequestMaterialRepository(db)
        self.request_repository = RequestToAcademyGroupRepository(db)
        self.student_repository = StudentRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: RequestMaterialEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = (
            AppFileExtensionConstants.DOCUMENT_EXTENSIONS
            | AppFileExtensionConstants.IMAGE_EXTENSIONS
        )

    async def execute(
        self, dto: RequestMaterialCDTO, file: UploadFile | None = None
    ) -> RequestMaterialWithRelationsRDTO:
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return RequestMaterialWithRelationsRDTO.from_orm(self.model)

    async def validate(
        self, dto: RequestMaterialCDTO, file: UploadFile | None = None
    ) -> None:
        if not await self.request_repository.get(dto.request_id):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_group_application_not_found")
            )

        if not await self.student_repository.get(dto.student_id):
            raise AppExceptionResponse.bad_request(message=i18n.gettext("student_not_found"))

        if dto.file_id:
            if not await self.file_repository.get(dto.file_id):
                raise AppExceptionResponse.bad_request(message=i18n.gettext("file_not_found"))

        if file:
            self.file_service.validate_file(file, self.extensions)

    async def transform(self, dto: RequestMaterialCDTO, file: UploadFile | None = None):
        self.upload_folder = AppFileExtensionConstants.request_material_directory(
            dto.request_id, dto.student_id
        )

        if file:
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id

        self.model = RequestMaterialEntity(**dto.dict())
