from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_student.academy_group_student_dto import (
    AcademyGroupStudentCDTO,
    AcademyGroupStudentWithRelationsRDTO,
)
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.adapters.repository.academy_group_student.academy_group_student_repository import (
    AcademyGroupStudentRepository,
)
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import (
    RequestToAcademyGroupRepository,
)
from app.adapters.repository.student.student_repository import StudentRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupStudentEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateAcademyGroupStudentCase(BaseUseCase[AcademyGroupStudentWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = AcademyGroupStudentRepository(db)
        self.student_repository = StudentRepository(db)
        self.group_repository = AcademyGroupRepository(db)
        self.request_repository = RequestToAcademyGroupRepository(db)
        self.model: AcademyGroupStudentEntity | None = None

    async def execute(
        self, dto: AcademyGroupStudentCDTO
    ) -> AcademyGroupStudentWithRelationsRDTO:
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return AcademyGroupStudentWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: AcademyGroupStudentCDTO) -> None:
        if not await self.student_repository.get(dto.student_id):
            raise AppExceptionResponse.bad_request(message=i18n.gettext("student_not_found"))

        if not await self.group_repository.get(dto.group_id):
            raise AppExceptionResponse.bad_request(message=i18n.gettext("academy_group_not_found"))

        if dto.request_id:
            if not await self.request_repository.get(dto.request_id):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("academy_group_application_not_found")
                )

        existing_student = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    AcademyGroupStudentEntity.student_id == dto.student_id,
                    AcademyGroupStudentEntity.group_id == dto.group_id,
                )
            ]
        )
        if existing_student:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("student_already_in_group")
            )

    async def transform(self, dto: AcademyGroupStudentCDTO):
        self.model = AcademyGroupStudentEntity(**dto.dict())
