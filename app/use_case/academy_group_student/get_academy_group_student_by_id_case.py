from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_student.academy_group_student_dto import AcademyGroupStudentWithRelationsRDTO
from app.adapters.repository.academy_group_student.academy_group_student_repository import AcademyGroupStudentRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_case.base_case import BaseUseCase


class GetAcademyGroupStudentByIdCase(BaseUseCase[AcademyGroupStudentWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = AcademyGroupStudentRepository(db)

    async def execute(self, id: int) -> AcademyGroupStudentWithRelationsRDTO:
        await self.validate(id)
        
        model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not model:
            raise AppExceptionResponse.not_found(message="Студент в группе не найден")
        
        return AcademyGroupStudentWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(message="ID должен быть положительным числом")