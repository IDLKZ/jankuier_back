from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationStudentWithRelationsRDTO
from app.adapters.dto.student.student_dto import StudentWithRelationsRDTO
from app.adapters.filters.student.student_pagination_filter import StudentPaginationFilter
from app.adapters.repository.student.student_repository import StudentRepository
from app.use_case.base_case import BaseUseCase


class PaginateStudentCase(BaseUseCase[PaginationStudentWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка студентов.

    Использует:
        - Репозиторий `StudentRepository` для работы с базой данных.
        - DTO `StudentWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `StudentPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (StudentRepository): Репозиторий для работы со студентами.

    Методы:
        execute(filter: StudentPaginationFilter) -> PaginationStudentWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список студентов.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = StudentRepository(db)

    async def execute(self, filter: StudentPaginationFilter) -> PaginationStudentWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка студентов.

        Args:
            filter (StudentPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationStudentWithRelationsRDTO: Объект пагинации со студентами.
        """
        pagination = await self.repository.paginate(
            dto=StudentWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """