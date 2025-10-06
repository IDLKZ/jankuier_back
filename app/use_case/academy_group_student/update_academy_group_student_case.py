from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_student.academy_group_student_dto import (
    AcademyGroupStudentUpdateDTO,
    AcademyGroupStudentWithRelationsRDTO,
)
from app.adapters.repository.academy_group_student.academy_group_student_repository import (
    AcademyGroupStudentRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupStudentEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateAcademyGroupStudentCase(BaseUseCase[AcademyGroupStudentWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = AcademyGroupStudentRepository(db)
        self.model: AcademyGroupStudentEntity | None = None

    async def execute(
        self, id: int, dto: AcademyGroupStudentUpdateDTO
    ) -> AcademyGroupStudentWithRelationsRDTO:
        await self.validate(id=id, dto=dto)
        await self.transform(dto=dto)
        await self.repository.update(self.model, dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return AcademyGroupStudentWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: AcademyGroupStudentUpdateDTO) -> None:
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_group_student_id_validation_error")
            )

        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("academy_group_student_not_found"))

    async def transform(self, dto: AcademyGroupStudentUpdateDTO):
        pass
