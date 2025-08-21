from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import RequestToAcademyGroupUpdateDTO, RequestToAcademyGroupWithRelationsRDTO
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import RequestToAcademyGroupRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestToAcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateRequestToAcademyGroupCase(BaseUseCase[RequestToAcademyGroupWithRelationsRDTO]):
    """
    Класс Use Case для обновления заявки в академическую группу.

    Использует:
        - Репозиторий `RequestToAcademyGroupRepository` для работы с базой данных.
        - DTO `RequestToAcademyGroupUpdateDTO` для входных данных.
        - DTO `RequestToAcademyGroupWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (RequestToAcademyGroupRepository): Репозиторий для работы с заявками в академические группы.
        user_repository (UserRepository): Репозиторий для работы с пользователями.
        model (RequestToAcademyGroupEntity | None): Модель заявки в академическую группу для обновления.

    Методы:
        execute(id: int, dto: RequestToAcademyGroupUpdateDTO) -> RequestToAcademyGroupWithRelationsRDTO:
            Выполняет обновление заявки в академическую группу.
        validate(id: int, dto: RequestToAcademyGroupUpdateDTO):
            Валидирует данные перед обновлением.
        transform(dto: RequestToAcademyGroupUpdateDTO):
            Трансформирует данные перед обновлением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = RequestToAcademyGroupRepository(db)
        self.user_repository = UserRepository(db)
        self.model: RequestToAcademyGroupEntity | None = None

    async def execute(self, id: int, dto: RequestToAcademyGroupUpdateDTO) -> RequestToAcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию обновления заявки в академическую группу.

        Args:
            id (int): Идентификатор заявки в академическую группу для обновления.
            dto (RequestToAcademyGroupUpdateDTO): DTO с данными для обновления заявки в академическую группу.

        Returns:
            RequestToAcademyGroupWithRelationsRDTO: Обновленный объект заявки в академическую группу с отношениями.

        Raises:
            AppExceptionResponse: Если заявка не найдена, связанные сущности не найдены или валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return RequestToAcademyGroupWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: RequestToAcademyGroupUpdateDTO) -> None:
        """
        Валидирует данные перед обновлением заявки в академическую группу.

        Args:
            id (int): Идентификатор заявки в академическую группу для обновления.
            dto (RequestToAcademyGroupUpdateDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если заявка не найдена, связанные сущности не найдены или валидация не прошла.
        """
        # Проверка существования заявки в академическую группу
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования пользователя (если указан новый проверяющий)
        if dto.checked_by is not None:
            if (await self.user_repository.get(dto.checked_by)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("user_not_found_by_id")
                )

        # Валидация статуса заявки (если указан новый статус)
        if dto.status is not None and dto.status not in [-1, 0, 1]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_request_status")
            )

        # Бизнес-правило: нельзя сбросить статус с принятого/отклоненного на "не просмотрена" без снятия проверяющего
        if (dto.status is not None and dto.status == 0 and 
            self.model.status in [1, -1] and 
            dto.checked_by is None and self.model.checked_by is not None):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cannot_reset_checked_request_without_removing_checker")
            )

        # Бизнес-правило: при принятии или отклонении заявки должен быть указан проверяющий
        if (dto.status is not None and dto.status in [1, -1] and 
            dto.checked_by is None and self.model.checked_by is None):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("checker_required_for_status_change")
            )

    async def transform(self, dto: RequestToAcademyGroupUpdateDTO):
        """
        Трансформирует данные перед обновлением заявки в академическую группу.

        Args:
            dto (RequestToAcademyGroupUpdateDTO): DTO с данными для трансформации.
        """
        # Трансформация не требуется для этой сущности
        pass