from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationAcademyGroupStudentWithRelationsRDTO
from app.adapters.dto.academy_group_student.academy_group_student_dto import AcademyGroupStudentWithRelationsRDTO
from app.adapters.filters.academy_group_student.academy_group_student_pagination_filter import AcademyGroupStudentPaginationFilter
from app.adapters.repository.academy_group_student.academy_group_student_repository import AcademyGroupStudentRepository
from app.use_case.base_case import BaseUseCase


class PaginateAcademyGroupStudentCase(BaseUseCase[PaginationAcademyGroupStudentWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = AcademyGroupStudentRepository(db)

    async def execute(self, filter: AcademyGroupStudentPaginationFilter) -> PaginationAcademyGroupStudentWithRelationsRDTO:
        pagination = await self.repository.paginate(
            dto=AcademyGroupStudentWithRelationsRDTO,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            page=filter.page,
            per_page=filter.per_page,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return PaginationAcademyGroupStudentWithRelationsRDTO(**pagination.dict())

    async def validate(self) -> None:
        pass