from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.firebase_notification.firebase_notification_dto import (
    FirebaseNotificationCDTO,
    FirebaseNotificationWithRelationsRDTO, FirebaseNotificationClientCDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.firebase_notification.firebase_notification_repository import (
    FirebaseNotificationRepository,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FirebaseNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateOrUpdateClientFirebaseNotificationCase(BaseUseCase[FirebaseNotificationWithRelationsRDTO]):
    """
    Use Case для создания или обновления Firebase уведомления клиента.

    Логика работы:
    1. Проверяет, существует ли уже Firebase токен для данного пользователя
    2. Если токен существует - обновляет его статус is_active
    3. Если токена нет - удаляет все старые токены пользователя и создаёт новый

    Это гарантирует, что у пользователя всегда только один активный Firebase токен.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)
        self.model: FirebaseNotificationEntity | None = None
        self.dto: FirebaseNotificationClientCDTO | None = None
        self.user: UserWithRelationsRDTO | None = None

    async def execute(
            self,
            dto: FirebaseNotificationClientCDTO,
            user: UserWithRelationsRDTO
    ) -> FirebaseNotificationWithRelationsRDTO:
        """
        Главный метод выполнения use case.

        Args:
            dto: DTO с данными Firebase токена
            user: Текущий пользователь

        Returns:
            FirebaseNotificationWithRelationsRDTO: Созданное или обновлённое уведомление
        """
        self.dto = dto
        self.user = user
        await self.validate()
        await self.transform()
        return FirebaseNotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Raises:
            AppExceptionResponse: Если DTO или пользователь не предоставлены
        """
        if not self.dto or not self.user:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("invalid_data"))

    async def transform(self) -> None:
        """
        Трансформация данных и бизнес-логика создания/обновления токена.

        Логика:
        1. Ищет существующий токен по user_id и token
        2. Если найден - обновляет поле is_active
        3. Если не найден - удаляет все старые токены пользователя и создаёт новый
        """
        # Подготовка данных для создания
        data = self.dto.dict()
        data["user_id"] = self.user.id

        # Поиск существующего токена
        self.model = await self.repository.get_first_with_filters(
            filters=[
                self.repository.model.user_id == self.user.id,
                self.repository.model.token == self.dto.token,
            ],
            options=self.repository.default_relationships())

        # Если токен уже существует - обновляем статус
        if self.model:
            cdto = FirebaseNotificationCDTO.from_orm(self.model)
            cdto.is_active = self.dto.is_active
            self.model = await self.repository.update(obj=self.model, dto=cdto)
        else:
            # Если токен новый - удаляем все старые токены пользователя
            # Это гарантирует, что у пользователя только один активный токен
            old_models = await self.repository.get_with_filters(
                filters=[
                    self.repository.model.user_id == self.user.id,
                ],
            )
            for old_model in old_models:
                await self.repository.delete(old_model.id)

            # Создаём новый токен
            self.model = await self.repository.create(obj=FirebaseNotificationEntity(**data))



