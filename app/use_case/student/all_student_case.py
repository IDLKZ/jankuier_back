from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.student.student_dto import StudentWithRelationsRDTO
from app.adapters.filters.student.student_filter import StudentFilter
from app.adapters.repository.student.student_repository import StudentRepository
from app.use_case.base_case import BaseUseCase


class AllStudentCase(BaseUseCase[list[StudentWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех студентов.

    Использует:
        - Репозиторий `StudentRepository` для работы с базой данных.
        - DTO `StudentWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (StudentRepository): Репозиторий для работы со студентами.

    Методы:
        execute(filter: StudentFilter) -> list[StudentWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех студентов.
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

    async def execute(self, filter: StudentFilter) -> list[StudentWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех студентов.

        Args:
            filter (StudentFilter): Фильтр для поиска и сортировки студентов.

        Returns:
            list[StudentWithRelationsRDTO]: Список объектов студентов с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [StudentWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """