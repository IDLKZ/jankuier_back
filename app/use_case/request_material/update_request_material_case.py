from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_material.request_material_dto import (
    RequestMaterialUpdateDTO,
    RequestMaterialWithRelationsRDTO,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.request_material.request_material_repository import (
    RequestMaterialRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestMaterialEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateRequestMaterialCase(BaseUseCase[RequestMaterialWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RequestMaterialRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: RequestMaterialEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = (
            AppFileExtensionConstants.DOCUMENT_EXTENSIONS
            | AppFileExtensionConstants.IMAGE_EXTENSIONS
        )

    async def execute(
        self, id: int, dto: RequestMaterialUpdateDTO, file: UploadFile | None = None
    ) -> RequestMaterialWithRelationsRDTO:
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        await self.repository.update(self.model, dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return RequestMaterialWithRelationsRDTO.from_orm(self.model)

    async def validate(
        self, id: int, dto: RequestMaterialUpdateDTO, file: UploadFile | None = None
    ) -> None:
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_id")
            )

        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("request_material_not_found"))

        if dto.file_id:
            if not await self.file_repository.get(dto.file_id):
                raise AppExceptionResponse.bad_request(message=i18n.gettext("file_not_found"))

        if file:
            self.file_service.validate_file(file, self.extensions)

    async def transform(
        self, dto: RequestMaterialUpdateDTO, file: UploadFile | None = None
    ):
        self.upload_folder = AppFileExtensionConstants.request_material_directory(
            self.model.request_id, self.model.student_id
        )

        if file:
            if self.model.file_id:
                file_entity = await self.file_service.update_file(
                    file_id=self.model.file_id,
                    new_file=file,
                    uploaded_folder=self.upload_folder,
                    extensions=self.extensions,
                )
            else:
                file_entity = await self.file_service.save_file(
                    file, self.upload_folder, self.extensions
                )
            dto.file_id = file_entity.id
