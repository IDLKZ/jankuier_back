from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.academy_group_student.academy_group_student_repository import (
    AcademyGroupStudentRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupStudentEntity
from app.shared.dto_constants import DTOConstant
from app.use_case.base_case import BaseUseCase


class DeleteAcademyGroupStudentCase(BaseUseCase[DTOConstant.StandardResponseDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = AcademyGroupStudentRepository(db)
        self.model: AcademyGroupStudentEntity | None = None

    async def execute(
        self, id: int, force_delete: bool = False
    ) -> DTOConstant.StandardResponseDTO:
        await self.validate(id)

        await self.repository.delete(id=id, force_delete=force_delete)

        return DTOConstant.StandardResponseDTO(
            message="Студент успешно исключен из группы"
        )

    async def validate(self, id: int) -> None:
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(
                message="ID должен быть положительным числом"
            )

        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message="Студент в группе не найден")
