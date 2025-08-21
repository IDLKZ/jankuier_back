from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_student.academy_group_student_dto import (
    AcademyGroupStudentWithRelationsRDTO,
)
from app.adapters.filters.academy_group_student.academy_group_student_filter import (
    AcademyGroupStudentFilter,
)
from app.adapters.repository.academy_group_student.academy_group_student_repository import (
    AcademyGroupStudentRepository,
)
from app.use_case.base_case import BaseUseCase


class AllAcademyGroupStudentCase(
    BaseUseCase[list[AcademyGroupStudentWithRelationsRDTO]]
):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = AcademyGroupStudentRepository(db)

    async def execute(
        self, filter: AcademyGroupStudentFilter
    ) -> list[AcademyGroupStudentWithRelationsRDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [
            AcademyGroupStudentWithRelationsRDTO.from_orm(model) for model in models
        ]

    async def validate(self) -> None:
        pass
