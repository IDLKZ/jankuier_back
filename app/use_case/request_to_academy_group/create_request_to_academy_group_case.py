from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import (
    RequestToAcademyGroupCDTO,
    RequestToAcademyGroupWithRelationsRDTO,
)
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import (
    RequestToAcademyGroupRepository,
)
from app.adapters.repository.student.student_repository import StudentRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestToAcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateRequestToAcademyGroupCase(
    BaseUseCase[RequestToAcademyGroupWithRelationsRDTO]
):
    """
    Класс Use Case для создания новой заявки в академическую группу.

    Использует:
        - Репозиторий `RequestToAcademyGroupRepository` для работы с базой данных.
        - DTO `RequestToAcademyGroupCDTO` для входных данных.
        - DTO `RequestToAcademyGroupWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (RequestToAcademyGroupRepository): Репозиторий для работы с заявками в академические группы.
        student_repository (StudentRepository): Репозиторий для работы со студентами.
        academy_group_repository (AcademyGroupRepository): Репозиторий для работы с группами академий.
        user_repository (UserRepository): Репозиторий для работы с пользователями.
        model (RequestToAcademyGroupEntity | None): Модель заявки в академическую группу для создания.

    Методы:
        execute(dto: RequestToAcademyGroupCDTO) -> RequestToAcademyGroupWithRelationsRDTO:
            Выполняет создание заявки в академическую группу.
        validate(dto: RequestToAcademyGroupCDTO):
            Валидирует данные перед созданием.
        transform(dto: RequestToAcademyGroupCDTO):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = RequestToAcademyGroupRepository(db)
        self.student_repository = StudentRepository(db)
        self.academy_group_repository = AcademyGroupRepository(db)
        self.user_repository = UserRepository(db)
        self.model: RequestToAcademyGroupEntity | None = None

    async def execute(
        self, dto: RequestToAcademyGroupCDTO
    ) -> RequestToAcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию создания новой заявки в академическую группу.

        Args:
            dto (RequestToAcademyGroupCDTO): DTO с данными для создания заявки в академическую группу.

        Returns:
            RequestToAcademyGroupWithRelationsRDTO: Созданный объект заявки в академическую группу с отношениями.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены, заявка уже существует или валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return RequestToAcademyGroupWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: RequestToAcademyGroupCDTO) -> None:
        """
        Валидирует данные перед созданием заявки в академическую группу.

        Args:
            dto (RequestToAcademyGroupCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены или заявка уже существует.
        """
        # Проверка существования студента
        if (await self.student_repository.get(dto.student_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("student_not_found_by_id")
            )

        # Проверка существования группы академии
        if (await self.academy_group_repository.get(dto.group_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_group_not_found_by_id")
            )

        # Проверка существования пользователя (если указан проверяющий)
        if dto.checked_by is not None:
            if (await self.user_repository.get(dto.checked_by)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("user_not_found_by_id")
                )

        # Проверка на дублирование заявки (один студент не может подать несколько заявок в одну группу)
        existed = await self.repository.get_first_with_filters(
            filters=[
                self.repository.model.student_id == dto.student_id,
                self.repository.model.group_id == dto.group_id,
            ]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("request_to_academy_group_already_exists")
            )

        # Валидация статуса заявки
        if dto.status not in [-1, 0, 1]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_request_status")
            )

    async def transform(self, dto: RequestToAcademyGroupCDTO):
        """
        Трансформирует данные перед созданием заявки в академическую группу.

        Args:
            dto (RequestToAcademyGroupCDTO): DTO с данными для трансформации.
        """
        # Создание модели для сохранения
        self.model = RequestToAcademyGroupEntity(**dto.dict())
